import { Cell, ICellModel, ICodeCellModel } from '@jupyterlab/cells';
import { FileBrowser } from '@jupyterlab/filebrowser';
import { NotebookPanel } from '@jupyterlab/notebook';
import { Kernel, KernelMessage } from '@jupyterlab/services';
import Parser, { Language } from 'web-tree-sitter';

import {
  CancelToken,
  CancellablePromise,
  CancellablePromiseRace
} from './cancellablePromise';

const CONTEXT_MAX_FILES = 100;

export const apiHostName = 'https://api.einblick.ai';
export const appHostName = 'https://app.einblick.ai';

export type PromptContextDataFrameColumn = {
  name: string;
  values: (string | number | boolean | null)[];
};

type KernelDataframeContext = {
  columns: string[];
  data: (string | boolean | number)[][];
  index: string[];
};

export type PromptContextDataFrameColumnDescription = {
  column: string;
  dataType: string;
  uniqueValues: string;
  missingValues: string;
  nonNullRows: string;
  mean: string;
  min: string;
  max: string;
  top3Common: string;
  percentile90th: string;
  percentile10th: string;
};

export type PromptContextDataFrame = {
  name: string;
  lastAccessed: number;
  distance: number; // 1M for root dataframes
  columns: PromptContextDataFrameColumn[];
  linkDistance: number | null;
  above: boolean;
  summary: PromptContextDataFrameColumnDescription[] | null;
};

export type PromptContextVariable = {
  name: string;
  lastAccessed: number;
  distance: number;
  type: string;
  linkDistance: number | null;
  above: boolean;
};

export type PromptContextCode = {
  type: string;
  code: string;
  lastAccessed: number;
  distance: number;
  linkDistance: number | null;
  above: boolean;
};

export type PromptContextModel = {
  dfs: PromptContextDataFrame[];
  vars: PromptContextVariable[];
  code: PromptContextCode[];
  dataConnectors: string[];
  tableInfo: string | null;
  filenames: { name: string; path: string }[];
};

const executeCode = (
  kernel: Kernel.IKernelConnection,
  code: string,
  ...cancelTokens: CancelToken[]
): Promise<string | undefined> => {
  const future = kernel.requestExecute({ code });
  return CancellablePromise(
    resolve => {
      future.onIOPub = message => {
        if (message.header.msg_type === 'stream') {
          const streamMessage = message as KernelMessage.IStreamMsg;
          if (streamMessage.content.name === 'stdout') {
            resolve(streamMessage.content.text);
          }
        }
      };
    },
    ...cancelTokens
  );
};

const getVariablesInKernel = async (
  kernel: Kernel.IKernelConnection,
  ...cancelTokens: CancelToken[]
): Promise<Record<string, string>> => {
  const output = await executeCode(
    kernel,
    'import json\nprint(json.dumps(list(map(lambda a: [a[0], str(type(a[1]))], [*(globals().items())]))))',
    ...cancelTokens
  );
  if (!output) {
    return {};
  }
  const entries = JSON.parse(output) as string[][];
  return Object.fromEntries(entries);
};

const getDataframeVariablesInKernel = async (
  kernel: Kernel.IKernelConnection,
  ...cancelTokens: CancelToken[]
): Promise<string[]> => {
  const output = await executeCode(
    kernel,
    [
      '!pip install --quiet --disable-pip-version-check pandas',
      'import pandas as pd',
      'import json',
      'import re',
      "global_variables = [k for k in globals() if not re.match('^_+[0-9]*$', k)]",
      'dfs = [v for v in global_variables if isinstance(globals()[v], pd.DataFrame)]',
      'print(json.dumps(dfs))'
    ].join('\n'),
    ...cancelTokens
  );
  if (!output) {
    return [];
  }
  const entries = JSON.parse(output) as string[];
  return entries ?? [];
};

const getContextForDataframe = async (
  kernel: Kernel.IKernelConnection,
  dataframeName: string,
  numRows = 3,
  ...cancelTokens: CancelToken[]
): Promise<PromptContextDataFrame | null> => {
  const output = await executeCode(
    kernel,
    `if '${dataframeName}' in globals():
   print(${dataframeName}.head(${numRows}).to_json(orient="split"))`,
    ...cancelTokens
  );
  if (!output) {
    return null;
  }

  const kernelDataframeContext = JSON.parse(output) as KernelDataframeContext;
  if (!kernelDataframeContext) {
    return null;
  }

  return {
    name: dataframeName,
    lastAccessed: 0,
    distance: 0,
    columns: kernelDataframeContext.columns.map((col, index) => {
      return {
        name: col,
        values: kernelDataframeContext.data.map(data => {
          const value = data[index];
          if (typeof value === 'string') {
            return value.substring(0, 200);
          }
          return value;
        })
      };
    }),
    linkDistance: null,
    above: true,
    summary: null
  };
};

// Taken from https://docs.python.org/3/library/functions.html
const GLOBAL_IDENTIFIERS = new Set<string>([
  'abs',
  'aiter',
  'all',
  'any',
  'anext',
  'ascii',
  'bin',
  'bool',
  'breakpoint',
  'bytearray',
  'bytes',
  'callable',
  'chr',
  'classmethod',
  'compile',
  'complex',
  'delattr',
  'dict',
  'dir',
  'divmod',
  'enumerate',
  'eval',
  'exec',
  'filter',
  'float',
  'format',
  'frozenset',
  'getattr',
  'globals',
  'hasattr',
  'hash',
  'help',
  'hex',
  'id',
  'input',
  'int',
  'isinstance',
  'issubclass',
  'iter',
  'len',
  'list',
  'locals',
  'map',
  'max',
  'memoryview',
  'min',
  'next',
  'object',
  'oct',
  'open',
  'ord',
  'pow',
  'print',
  'property',
  'range',
  'repr',
  'reversed',
  'round',
  'set',
  'setattr',
  'slice',
  'sorted',
  'staticmethod',
  'str',
  'sum',
  'super',
  'tuple',
  'type',
  'vars',
  'zip',
  '__import__'
]);

type TreeAnalysisResult = {
  variablesUsed: Set<string>;
  variablesAssigned: Set<string>;
};

type TreeAnalysisSettings = {
  ignoreImports: boolean;
};

/**
 * Analyzes the tree and returns the variables used and assigned in the script
 *
 * @see https://github.com/tree-sitter/tree-sitter-python/blob/master/src/node-types.json
 * This is a list of all the node types that can be returned by the parser, as well as the fields that each node type has.
 */
function analyzeTree(
  node: Parser.SyntaxNode | null,
  settings: TreeAnalysisSettings,
  isAssigning = false
): TreeAnalysisResult {
  const variablesUsed = new Set<string>();
  const variablesAssigned = new Set<string>();
  if (!node || !node.isNamed) {
    return {
      variablesUsed,
      variablesAssigned
    };
  }

  function addResult(
    result: TreeAnalysisResult,
    ignoreIfAssigned = true
  ): void {
    result.variablesUsed.forEach(v => {
      // Only add variables to the used set if they haven't been assigned earlier in this scope
      if (!(variablesAssigned.has(v) && ignoreIfAssigned)) {
        variablesUsed.add(v);
      }
    });
    result.variablesAssigned.forEach(v => variablesAssigned.add(v));
  }

  switch (node.type) {
    case 'assignment': {
      // Do right before left so that we can check if the variable is used before it's assigned
      const right = node.childForFieldName('right');
      addResult(analyzeTree(right, settings, isAssigning));

      const left = node.childForFieldName('left');
      addResult(analyzeTree(left, settings, true)); // Set assignment flag to true in left side

      break;
    }
    case 'call': {
      const func = node.childForFieldName('function');
      addResult(analyzeTree(func, settings, isAssigning));
      const args = node.childForFieldName('arguments');
      addResult(analyzeTree(args, settings, isAssigning));
      break;
    }
    case 'aliased_import': {
      if (!settings.ignoreImports) {
        const importedItem = node.childForFieldName('alias');
        addResult(analyzeTree(importedItem, settings, true)); // Imports are always "assignments" (sources)
      }
      break;
    }
    case 'import_from_statement': {
      if (!settings.ignoreImports) {
        const importedItem = node.childForFieldName('name');
        addResult(analyzeTree(importedItem, settings, true)); // Imports are always "assignments" (sources)

        let sibling = importedItem?.nextNamedSibling;
        while (sibling) {
          // `childForFieldName("name")` only returns the first named child, so we need to iterate through all the siblings
          if (!settings.ignoreImports) {
            addResult(analyzeTree(sibling, settings, true));
          }
          sibling = sibling.nextNamedSibling;
        }
      }
      break;
    }
    case 'import_statement': {
      const importedItem = node.childForFieldName('name');
      addResult(analyzeTree(importedItem, settings, true)); // Imports are always "assignments" (sources)
      break;
    }
    case 'type':
      break;
    case 'subscript': {
      // If we are assigning a value subscript, we also define it as a dependency (even if it's defined in the same block)
      const value = node.childForFieldName('value');
      addResult(analyzeTree(value, settings, isAssigning), false);
      if (isAssigning) {
        addResult(analyzeTree(value, settings, false), false);
      }

      const subscript = node.childForFieldName('subscript');
      addResult(analyzeTree(subscript, settings, false)); // Subscripts are never assignments
      break;
    }
    case 'attribute': {
      // Only look at the object, since the attribute is just a property accessor
      const object = node.childForFieldName('object');
      addResult(analyzeTree(object, settings, isAssigning));
      break;
    }
    case 'dotted_name': {
      // Only look at first identifier, since the rest are just property accessors
      const first = node.firstNamedChild;
      addResult(analyzeTree(first, settings, isAssigning));
      break;
    }
    case 'keyword_argument': {
      // For keyword arguments, only check value, ignore the name field
      const value = node.childForFieldName('value');
      addResult(analyzeTree(value, settings, false)); // Keyword arguments should reset the assignment flag
      break;
    }
    case 'set_comprehension':
    case 'dictionary_comprehension':
    case 'list_comprehension': {
      const body = node.childForFieldName('body');
      const bodyResult = analyzeTree(body, settings, false);

      if (body) {
        const forInClause = body.nextNamedSibling;
        const forInResult = analyzeTree(forInClause, settings, false);
        // Delete the variables assigned in the for-in clause from the variables used in the body
        forInResult.variablesAssigned.forEach(variable =>
          bodyResult.variablesUsed.delete(variable)
        );
        addResult({
          variablesUsed: new Set([
            ...bodyResult.variablesUsed,
            ...forInResult.variablesUsed
          ]), // merge variables used in the body and the for-in clause
          variablesAssigned: bodyResult.variablesAssigned // ignore variables assigned in the for-in clause
        });
      }
      break;
    }
    case 'for_in_clause': {
      // Special case, only happens in list/dict/set comprehensions
      const left = node.childForFieldName('left');
      addResult(analyzeTree(left, settings, true)); // Set assignment flag to true in left side, however this will be removed by the list comprehension
      const right = node.childForFieldName('right');
      addResult(analyzeTree(right, settings, isAssigning));
      break;
    }
    case 'for_statement': {
      const left = node.childForFieldName('left');
      const leftResult = analyzeTree(left, settings, true); // Temp variable in for loop
      const right = node.childForFieldName('right');
      const rightResult = analyzeTree(right, settings, false); // Right side of for loop
      const body = node.childForFieldName('body');
      const bodyResult = analyzeTree(body, settings, false); // Body of for loop
      // Delete the variables assigned in the for loop from the variables used in the body
      leftResult.variablesAssigned.forEach(variable =>
        bodyResult.variablesUsed.delete(variable)
      );
      addResult({
        variablesUsed: new Set([
          ...bodyResult.variablesUsed,
          ...rightResult.variablesUsed
        ]), // merge variables used in the body and the right side
        variablesAssigned: bodyResult.variablesAssigned // ignore variables assigned in the for loop
      });
      break;
    }
    case 'identifier':
      if (isAssigning) {
        variablesAssigned.add(node.text);
      } else {
        variablesUsed.add(node.text);
      }
      break;
    case 'function_definition':
      // Function name is a assigned dependency
      addResult(analyzeTree(node.childForFieldName('name'), settings, true));
      break;
    default: {
      node.namedChildren.forEach((child: Parser.SyntaxNode) => {
        addResult(analyzeTree(child, settings, isAssigning));
      });
    }
  }

  return {
    variablesUsed,
    variablesAssigned
  };
}

export function getDependencies(tree: Parser.Tree): TreeAnalysisResult {
  const result = analyzeTree(tree.rootNode, { ignoreImports: true });
  const filteredAssignments = new Set<string>();
  result.variablesAssigned.forEach(variable => {
    if (!GLOBAL_IDENTIFIERS.has(variable)) {
      filteredAssignments.add(variable);
    }
  });
  const filteredVariablesUsed = new Set<string>();
  result.variablesUsed.forEach(variable => {
    if (!GLOBAL_IDENTIFIERS.has(variable)) {
      filteredVariablesUsed.add(variable);
    }
  });
  return {
    variablesAssigned: filteredAssignments,
    variablesUsed: filteredVariablesUsed
  };
}

let pythonParser: Parser | null = null;
let language: Language | null = null;

const loadPythonParser = async (
  ...cancelTokens: CancelToken[]
): Promise<Parser | undefined> => {
  if (pythonParser && language) {
    return pythonParser;
  }

  try {
    await CancellablePromiseRace(
      [
        Parser.init({
          locateFile: (fileName: string) => {
            return `${appHostName}/assets/tree-sitter-v0.20.8/${fileName}`;
          }
        })
      ],
      ...cancelTokens
    );
    if (cancelTokens.some(token => token.IsCancelled)) {
      return undefined;
    }

    pythonParser = new Parser();
    const languageWasmFileResponse = await CancellablePromiseRace(
      [
        fetch(
          `${appHostName}/assets/tree-sitter-v0.20.8/tree-sitter-python.wasm`
        )
      ],
      ...cancelTokens
    );
    if (cancelTokens.some(token => token.IsCancelled)) {
      return undefined;
    }

    if (!languageWasmFileResponse || !languageWasmFileResponse.ok) {
      console.error('Unable to load language file!');
      throw Error('Unable to load language file!');
    }

    const arrayBuffer = await CancellablePromiseRace(
      [languageWasmFileResponse.arrayBuffer()],
      ...cancelTokens
    );
    if (cancelTokens.some(token => token.IsCancelled)) {
      return undefined;
    } else if (!arrayBuffer) {
      throw Error('Unable to load language file!');
    }
    const languageFileBinary = new Uint8Array(arrayBuffer);

    language =
      (await CancellablePromiseRace(
        [Parser.Language.load(languageFileBinary)],
        ...cancelTokens
      )) ?? null;
    if (cancelTokens.some(token => token.IsCancelled)) {
      return undefined;
    } else if (!language) {
      throw Error('Unable to load language file!');
    }

    pythonParser.setLanguage(language);
    return pythonParser;
  } catch (error) {
    console.error(`Failed to load python parser\n${error}`);
    throw error;
  }
};

export class PromptContextUtil {
  public static async GetContextForActiveNotebookCellBasedOnRadius(
    activeCell: Cell<ICellModel>,
    notebookPanel: NotebookPanel,
    browser: FileBrowser | null = null,
    radius = 1000,
    ...cancelTokens: CancelToken[]
  ): Promise<PromptContextModel> {
    const context: PromptContextModel = {
      dfs: [],
      vars: [],
      code: [],
      dataConnectors: [],
      tableInfo: null,
      filenames: []
    };

    const nearbyCellParitalContexts: Array<{
      cell: Cell<ICellModel>;
      distance: number;
      linkDistance: number | null;
      above: boolean;
      lastAccessed: number;
    }> = [];

    const notebookCells = notebookPanel.content.widgets;
    const activeCellIndex = notebookCells.indexOf(activeCell);
    const kernel = notebookPanel.sessionContext.session?.kernel;
    if (activeCellIndex < 0 || activeCell.model.type !== 'code' || !kernel) {
      return context;
    }

    // Get client rects for all cells in the notebook
    const cellBoundingClientRects = notebookCells.map(cell =>
      cell.node.getBoundingClientRect()
    );
    const activeCellRect = cellBoundingClientRects[activeCellIndex];

    // Adding cells based on radius
    let cellIndex = 0;
    for (const cell of notebookCells) {
      const notebookCellRect = cellBoundingClientRects[cellIndex];

      let distance = Number.POSITIVE_INFINITY;
      if (cellIndex < activeCellIndex) {
        distance = activeCellRect.top - notebookCellRect.bottom;
      } else if (cellIndex > activeCellIndex) {
        distance = notebookCellRect.top - activeCellRect.bottom;
      }

      if (distance <= radius) {
        nearbyCellParitalContexts.push({
          cell,
          distance,
          linkDistance: Math.abs(cellIndex - activeCellIndex),
          above: cellIndex < activeCellIndex,
          lastAccessed: 0
        });
      }

      cellIndex++;
    }

    const pythonParser = await loadPythonParser(...cancelTokens);
    if (cancelTokens.some(token => token.IsCancelled)) {
      return context;
    } else if (!pythonParser) {
      throw Error('Unable to get python parser when loading context');
    }

    const variablesInKernel = await getVariablesInKernel(
      kernel,
      ...cancelTokens
    );
    if (cancelTokens.some(token => token.IsCancelled)) {
      return context;
    }

    const dataframeVariablesInKernel = await getDataframeVariablesInKernel(
      kernel,
      ...cancelTokens
    );
    if (cancelTokens.some(token => token.IsCancelled)) {
      return context;
    }

    for (const nearbyCellPartialContext of nearbyCellParitalContexts) {
      if (nearbyCellPartialContext.cell.model.type !== 'code') {
        continue;
      }

      const codeCell = nearbyCellPartialContext.cell as Cell<ICodeCellModel>;
      const codeCellSource = codeCell.model.toJSON().source;
      const codeCellContent = Array.isArray(codeCellSource)
        ? codeCellSource.join('\n')
        : codeCellSource;
      const codeCellDependenciesResult = getDependencies(
        pythonParser.parse(codeCellContent)
      );
      const usedCodeCellVariables = Array.from(
        codeCellDependenciesResult.variablesUsed.values()
      );
      const assignedCodeCellVariables = Array.from(
        codeCellDependenciesResult.variablesAssigned.values()
      );
      const combined = [...usedCodeCellVariables, ...assignedCodeCellVariables];

      for (const usedCodeCellVariable of combined) {
        if (dataframeVariablesInKernel.includes(usedCodeCellVariable)) {
          const dfContext = await getContextForDataframe(
            kernel,
            usedCodeCellVariable,
            3,
            ...cancelTokens
          );
          if (cancelTokens.some(token => token.IsCancelled)) {
            return context;
          } else if (dfContext) {
            context.dfs.push(dfContext);
          }
        } else {
          context.vars.push({
            distance: nearbyCellPartialContext.distance,
            lastAccessed: nearbyCellPartialContext.lastAccessed,
            linkDistance: nearbyCellPartialContext.linkDistance,
            above: nearbyCellPartialContext.above,
            name: usedCodeCellVariable,
            type: variablesInKernel[usedCodeCellVariable] ?? ''
          });
        }
      }

      context.code.push({
        distance: nearbyCellPartialContext.distance,
        lastAccessed: nearbyCellPartialContext.lastAccessed,
        linkDistance: nearbyCellPartialContext.linkDistance,
        above: nearbyCellPartialContext.above,
        type: 'python',
        code: codeCellContent
      });
    }

    if (browser) {
      const dataFiles = Array.from(browser.model.items()).filter(
        item =>
          item.type === 'file' &&
          (item.path.endsWith('.csv') || item.path.endsWith('.tsv'))
      );
      for (const file of dataFiles) {
        if (context.filenames.length < CONTEXT_MAX_FILES) {
          context.filenames.push({
            name: file.name,
            path: file.path
          });
        }
      }
    }

    return context;
  }
}
