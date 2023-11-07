import { JupyterFrontEnd } from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { Cell, ICellModel } from '@jupyterlab/cells';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { CommandRegistry } from '@lumino/commands';
import { ReadonlyPartialJSONObject } from '@lumino/coreutils';

import { PromptCodeCell } from './contentFactory';
import { PromptModel, canExecuteFixCell } from './model';
import { IPromptMetadata } from './promptMetadata';

export const CONTEXTUAL_PROMPT_COMMAND_ID =
  'ai-einblick-prompt:contextual-prompt';
export const TOGGLE_CONTEXTUAL_PROMPT_COMMAND_ID =
  'ai-einblick-prompt:toggle-contextual-prompt';
export const GENERATE_COMMAND_ID = 'ai-einblick-prompt:generate';
export const MODIFY_COMMAND_ID = 'ai-einblick-prompt:modify';
export const FIX_COMMAND_ID = 'ai-einblick-prompt:fix';

export const EINBLICK_COMMAND_CATEGORY = 'Einblick';

export const executePromptCommand = (
  type: PromptModel.PromptType,
  cell: Cell<ICellModel>,
  notebook: NotebookPanel,
  commands: CommandRegistry
): void => {
  if (cell && notebook) {
    const newCommandArgs = {
      cell: cell.id,
      notebook: notebook.id
    };
    switch (type) {
      case PromptModel.PromptType.GENERATE_CELL:
        commands.execute(GENERATE_COMMAND_ID, newCommandArgs);
        break;
      case PromptModel.PromptType.MODIFY_CELL:
        commands.execute(MODIFY_COMMAND_ID, newCommandArgs);
        break;
      case PromptModel.PromptType.FIX_CELL:
        commands.execute(FIX_COMMAND_ID, newCommandArgs);
        break;
    }
  }
};

export const getContextualPromptType = (
  cell: PromptCodeCell,
  notebook: NotebookPanel
): PromptModel.PromptType => {
  let type: PromptModel.PromptType = PromptModel.PromptType.GENERATE_CELL;
  if (canExecuteFixCell(cell, notebook)) {
    type = PromptModel.PromptType.FIX_CELL;
  } else {
    const cellSource = cell.model.toJSON().source;
    const cellContent = Array.isArray(cellSource)
      ? cellSource.join('\n')
      : cellSource;
    if (cellContent.trim() !== '') {
      type = PromptModel.PromptType.MODIFY_CELL;
    }
  }
  return type;
};

export const registerCommands = (
  app: JupyterFrontEnd,
  palette: ICommandPalette,
  notebookTracker: INotebookTracker,
  translator: ITranslator | null,
  promptMetadata: IPromptMetadata | null
): void => {
  const trans = (translator ?? nullTranslator).load('jupyterlab');

  const formAndExecutePromptCommand = (
    args: ReadonlyPartialJSONObject,
    type: PromptModel.PromptType
  ) => {
    let cell: Cell<ICellModel> | null = null;
    let notebook: NotebookPanel | null = null;
    if (args.notebook) {
      if (notebookTracker.currentWidget?.id === args.notebook) {
        notebook = notebookTracker.currentWidget;
      }
    } else {
      notebook = notebookTracker.currentWidget;
    }
    if (args.cell) {
      cell = notebook?.content.widgets.find(c => c.id === args.cell) ?? null;
    } else {
      cell = notebookTracker.activeCell;
    }

    if (cell instanceof PromptCodeCell && notebook) {
      if (cell.promptCellHeader) {
        cell.promptCellHeader.openPrompt(
          type,
          app.commands,
          promptMetadata ?? undefined
        );
      }
    }
  };

  app.commands.addCommand(CONTEXTUAL_PROMPT_COMMAND_ID, {
    label: trans.__('Einblick AI: Prompt'),
    execute: () => {
      let cell: Cell<ICellModel> | null = null;
      let notebook: NotebookPanel | null = null;
      let type: PromptModel.PromptType = PromptModel.PromptType.GENERATE_CELL;

      cell = notebookTracker.activeCell;
      notebook = notebookTracker.currentWidget;

      if (cell instanceof PromptCodeCell && notebook) {
        type = getContextualPromptType(cell, notebook);
      }
      if (cell && notebook) {
        executePromptCommand(type, cell, notebook, app.commands);
      }
    }
  });
  palette.addItem({
    command: CONTEXTUAL_PROMPT_COMMAND_ID,
    category: EINBLICK_COMMAND_CATEGORY
  });

  app.commands.addCommand(TOGGLE_CONTEXTUAL_PROMPT_COMMAND_ID, {
    execute: args => {
      if (document.activeElement) {
        const notebook = notebookTracker.currentWidget;
        if (notebook) {
          const cellWithFocusedPrompt = notebook.content.widgets.find(cell => {
            if (!(cell instanceof PromptCodeCell)) {
              return false;
            }
            return (
              document.activeElement ===
              cell.promptCellHeader?.promptTextAreaElement
            );
          }) as PromptCodeCell | undefined;

          if (cellWithFocusedPrompt?.promptCellHeader) {
            cellWithFocusedPrompt.promptCellHeader.closePrompt();
            return;
          }
        }
      }
      app.commands.execute(CONTEXTUAL_PROMPT_COMMAND_ID, args);
    }
  });
  app.commands.addKeyBinding({
    command: TOGGLE_CONTEXTUAL_PROMPT_COMMAND_ID,
    args: {},
    keys: ['Accel K'],
    selector: '.jp-Notebook'
  });

  app.commands.addCommand(GENERATE_COMMAND_ID, {
    label: trans.__('Einblick AI: Generate'),
    execute: args => {
      formAndExecutePromptCommand(args, PromptModel.PromptType.GENERATE_CELL);
    }
  });
  palette.addItem({
    command: GENERATE_COMMAND_ID,
    category: EINBLICK_COMMAND_CATEGORY
  });

  app.commands.addCommand(MODIFY_COMMAND_ID, {
    label: trans.__('Einblick AI: Modify'),
    execute: args => {
      formAndExecutePromptCommand(args, PromptModel.PromptType.MODIFY_CELL);
    }
  });
  palette.addItem({
    command: MODIFY_COMMAND_ID,
    category: EINBLICK_COMMAND_CATEGORY
  });

  app.commands.addCommand(FIX_COMMAND_ID, {
    label: trans.__('Einblick AI: Fix'),
    execute: args => {
      formAndExecutePromptCommand(args, PromptModel.PromptType.FIX_CELL);
    }
  });
  palette.addItem({
    command: FIX_COMMAND_ID,
    category: EINBLICK_COMMAND_CATEGORY
  });
};
