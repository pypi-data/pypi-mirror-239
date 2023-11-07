import { Cell, ICellModel, isCodeCellModel } from '@jupyterlab/cells';
import { FileBrowser } from '@jupyterlab/filebrowser';
import { isError } from '@jupyterlab/nbformat';
import { NotebookPanel } from '@jupyterlab/notebook';
import {
  ITranslator,
  TranslationBundle,
  nullTranslator
} from '@jupyterlab/translation';
import { VDomModel } from '@jupyterlab/ui-components';
import Anser from 'anser';

import { CancelToken, CancellablePromiseRace } from './cancellablePromise';
import { IPromptMetadata } from './promptMetadata';
import { PromptContextModel, PromptContextUtil, apiHostName } from './utils';

const INPUT_CHARACTER_MAX = 2000;

export namespace PromptModel {
  export type PromptModel = {
    human: string;
    ai: {
      data: any;
      description: string;
    };
  };

  export type AIRefineModel = {
    Context: PromptContextModel;
    Prompt: string;
    Current: any;
    History: PromptModel[];
    ErrorMessage: string | null;
    Metadata?: Record<string, string>;
  };

  export const AskUserToolName = 'ask-user';
  export const FilterToolName = 'row-subset-tool';
  export const PythonToolName = 'generate-python-code';
  export type AIAgentToolName =
    | typeof AskUserToolName
    | typeof FilterToolName
    | typeof PythonToolName;

  export type AIAgentModel = {
    Context: PromptContextModel;
    Prompt: string;
    Tools: AIAgentToolName[];
    Metadata?: Record<string, string>;
  };

  export type BasePromptToolResponseModel<T = any> = {
    data: T | null;
    description: string;
    type: string;
    codeType?: string;
    isValid: boolean;
    error?: string;
    runId?: string;
  };

  export type PythonToolResult = string;

  export type PromptToolResponseModel<T> = BasePromptToolResponseModel<T>;

  export enum PromptType {
    GENERATE_CELL = 'generate-cell',
    MODIFY_CELL = 'modify-cell',
    FIX_CELL = 'fix-cell'
  }

  const getPlaceholders = (
    trans: TranslationBundle
  ): Record<PromptType, string> => {
    return {
      [PromptType.GENERATE_CELL]: trans.__('What do you want to add?'),
      [PromptType.MODIFY_CELL]: trans.__('What do you want to modify?'),
      [PromptType.FIX_CELL]: trans.__('')
    };
  };

  /**
   * A VDomModel for a Prompt.
   */
  export class Model extends VDomModel {
    constructor(
      type: PromptType,
      cell: Cell<ICellModel>,
      notebook: NotebookPanel,
      fileBrowser?: FileBrowser,
      translator?: ITranslator,
      metadata?: IPromptMetadata
    ) {
      super();

      this.translator = translator ?? nullTranslator;
      this._trans = this.translator.load('jupyterlab');

      this._type = type;
      this._cell = cell;
      this._notebook = notebook;
      this._fileBrowser = fileBrowser ?? null;
      this._metadata = metadata ?? null;

      this._placeholder = getPlaceholders(this._trans)[this._type];
      this._processingMessage = this._trans.__('Working on it...');
    }

    get type(): PromptType {
      return this._type;
    }

    get cell(): Cell<ICellModel> {
      return this._cell;
    }

    get notebook(): NotebookPanel {
      return this._notebook;
    }

    get placeholder(): string {
      return this._placeholder;
    }

    get processingMessage(): string {
      return this._processingMessage;
    }

    get errorMessage(): string | null {
      return this._errorMessage;
    }

    get userInput(): string {
      return this._userInput;
    }
    set userInput(value: string) {
      this._userInput = value;
      this.stateChanged.emit();
    }

    get isProcessing(): boolean {
      return this._cancelToken !== null;
    }

    get isErroneous(): boolean {
      return typeof this._errorMessage === 'string';
    }

    async execute(): Promise<void> {
      if (this._cancelToken) {
        return;
      }

      try {
        this._cancelToken = new CancelToken(Error('User cancelled'));
        this.stateChanged.emit();
        switch (this._type) {
          case PromptModel.PromptType.GENERATE_CELL:
            await this.generate(this._userInput, this._cancelToken);
            break;
          case PromptModel.PromptType.MODIFY_CELL:
            await this.modify(this._userInput, this._cancelToken);
            break;
          case PromptModel.PromptType.FIX_CELL:
            await this.fix(this._cancelToken);
            break;
        }
      } catch (error) {
        this._errorMessage =
          'There was an unexpected error executing the prompt.';
      } finally {
        this._cancelToken = null;
        this.stateChanged.emit();
      }
    }

    cancel(): void {
      if (this._cancelToken && !this._cancelToken.IsCancelled) {
        this._cancelToken?.Cancel();
      }
    }

    private _type: PromptType;
    private _cell: Cell<ICellModel>;
    private _notebook: NotebookPanel;
    private _fileBrowser: FileBrowser | null;
    private _metadata: IPromptMetadata | null = null;

    private readonly _placeholder: string = '';
    private readonly _processingMessage: string;

    private _userInput: string = '';
    private _errorMessage: string | null = null;

    protected translator: ITranslator;
    private _trans: TranslationBundle;

    private _cancelToken: CancelToken | null = null;

    private async getCellContext(): Promise<PromptContextModel> {
      const cellModel = this._cell.model;
      if (!cellModel || !isCodeCellModel(cellModel)) {
        throw Error('Need valid code cell model.');
      }

      const notebookModel = this._notebook.model;
      if (!notebookModel) {
        throw Error('Need valid notebook model.');
      }

      if (!this._cancelToken) {
        throw Error('Cancel token should not be null');
      }

      return PromptContextUtil.GetContextForActiveNotebookCellBasedOnRadius(
        this._cell,
        this._notebook,
        this._fileBrowser,
        1000,
        this._cancelToken
      );
    }

    private async generate(
      input: string,
      cancelToken: CancelToken
    ): Promise<void> {
      const context = await this.getCellContext();
      if (cancelToken.IsCancelled) {
        return;
      }

      const agentRequest: AIAgentModel = {
        Prompt: this.truncateEnd(input, INPUT_CHARACTER_MAX),
        Context: context,
        Tools: [PythonToolName]
      };
      if (this._metadata) {
        agentRequest.Metadata = { ...this._metadata };
      }

      const result = await CancellablePromiseRace(
        [
          fetch(`${apiHostName}/ai/prompt/python`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(agentRequest)
          })
        ],
        cancelToken
      );
      if (cancelToken.IsCancelled) {
        return;
      } else if (!result) {
        throw Error('Unable to process prompt');
      } else if (!result.ok) {
        throw Error(`${result.status}: ${result.statusText}`);
      }

      const resultJson: PromptToolResponseModel<PythonToolResult> | undefined =
        await CancellablePromiseRace([result.json()], cancelToken);
      if (cancelToken.IsCancelled) {
        return;
      } else if (!resultJson) {
        throw Error('Unable to process prompt');
      }

      const newCode = resultJson.data;

      if (resultJson.error) {
        throw Error(resultJson.error);
      }

      if (resultJson.isValid && typeof newCode === 'string') {
        this.replaceCellContent(newCode);
        this.cell.activate();
      }
      this.userInput = '';
    }

    private async modify(
      input: string,
      cancelToken: CancelToken
    ): Promise<void> {
      const context = await this.getCellContext();
      if (cancelToken.IsCancelled) {
        return;
      }
      const cellModel = this._cell.model;
      if (!cellModel) {
        throw new Error('Need valid cell model.');
      }

      const activeCodeCellSource = cellModel.toJSON().source;
      const activeCodeCellContent = Array.isArray(activeCodeCellSource)
        ? activeCodeCellSource.join('\n')
        : activeCodeCellSource;

      const refineRequest: AIRefineModel = {
        Prompt: this.truncateEnd(input, INPUT_CHARACTER_MAX),
        Context: context,
        Current: activeCodeCellContent,
        History: [],
        ErrorMessage: null
      };
      if (this._metadata) {
        refineRequest.Metadata = { ...this._metadata };
      }

      const result = await CancellablePromiseRace(
        [
          fetch(`${apiHostName}/ai/refinePrompt/python-notebook-cell`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(refineRequest)
          })
        ],
        cancelToken
      );
      if (cancelToken.IsCancelled) {
        return;
      } else if (!result) {
        throw Error('Unable to process prompt');
      } else if (!result.ok) {
        throw Error(`${result.status}: ${result.statusText}`);
      }

      const resultJson: BasePromptToolResponseModel | undefined =
        await CancellablePromiseRace([result.json()], cancelToken);
      if (cancelToken.IsCancelled) {
        return;
      } else if (!resultJson) {
        throw Error('Unable to process prompt');
      }

      const newCode = resultJson?.data;

      if (resultJson.error) {
        throw Error(resultJson.error);
      }

      if (resultJson.isValid && typeof newCode === 'string') {
        this.replaceCellContent(newCode);
        this.cell.activate();
      }
      this.userInput = '';
    }

    private async fix(cancelToken: CancelToken): Promise<void> {
      const cellModel = this._cell.model;
      if (!cellModel || !isCodeCellModel(cellModel)) {
        throw new Error('Need valid code cell model.');
      }

      const errorOutput = cellModel.outputs.toJSON().find(isError);
      if (!errorOutput) {
        return;
      }

      const traceback = Anser.ansiToText(errorOutput.traceback.join('\n'));
      await this.modify(
        this.truncateMiddle(
          `Please edit the code to fix the following error:\n${traceback}`,
          INPUT_CHARACTER_MAX
        ),
        cancelToken
      );
    }

    private truncateEnd(input: string, limit: number): string {
      return input.substring(0, limit);
    }

    private truncateMiddle(input: string, limit: number): string {
      const len = input.length;
      if (len <= limit) {
        return input;
      }

      const constructTruncated = (front: string, back: string): string =>
        `${front}...${back}`;

      const combinedSampleSize = Math.max(
        0,
        limit - constructTruncated('', '').length
      );

      const backSampleSize = Math.min(
        Math.floor(combinedSampleSize / 2),
        combinedSampleSize
      );
      const frontSampleSize = combinedSampleSize - backSampleSize;

      const frontSample = input.substring(0, frontSampleSize);
      const backSample = input.substring(
        frontSampleSize,
        frontSampleSize + backSampleSize
      );
      return constructTruncated(frontSample, backSample);
    }

    private replaceCellContent(newContent: string): void {
      const cellEditor = this._cell.editor;
      if (!cellEditor) {
        return;
      }
      const lastLineIndex = Math.max(0, cellEditor.lineCount - 1);
      const lastLine = cellEditor.getLine(lastLineIndex);
      if (typeof lastLine === 'string') {
        cellEditor.setSelection({
          start: { line: 0, column: 0 },
          end: {
            line: lastLineIndex,
            column: lastLine.length
          }
        });
      }
      cellEditor.replaceSelection?.(newContent);
    }
  }
}

function canGetCellContext(
  cell: Cell<ICellModel> | null,
  notebook: NotebookPanel | null
): boolean {
  if (!cell || !cell.model || !isCodeCellModel(cell.model)) {
    return false;
  }

  if (!notebook || !notebook.model) {
    return false;
  }

  return true;
}

export function canExecuteFixCell(
  cell: Cell<ICellModel> | null,
  notebook: NotebookPanel | null
): boolean {
  if (!canGetCellContext(cell, notebook)) {
    return false;
  }

  const cellModel = cell?.model;
  if (!cell || !cellModel || !isCodeCellModel(cellModel)) {
    return false;
  }

  if (!cellModel.outputs.toJSON().some(isError)) {
    return false;
  }

  return true;
}
