import { Cell, CodeCell, ICellHeader, ICellModel } from '@jupyterlab/cells';
import { FileBrowser } from '@jupyterlab/filebrowser';
import { NotebookPanel } from '@jupyterlab/notebook';
import { CommandRegistry } from '@lumino/commands';
import { Panel, PanelLayout, Widget } from '@lumino/widgets';

import { PromptModel } from './model';
import { Prompt } from './prompt';
import { IPromptMetadata } from './promptMetadata';

const CELL_OPENED_PROMPT_CLASS = 'jp-cell--prompt-opened';

/**
 * Extend the default implementation of an `IContentFactory`.
 */
export class PromptContentFactory extends NotebookPanel.ContentFactory {
  constructor(options: Cell.ContentFactory.IOptions) {
    super(options);
  }

  createCellHeader(): ICellHeader {
    return new PromptCellHeader();
  }

  createCodeCell(options: CodeCell.IOptions): CodeCell {
    return new PromptCodeCell(options);
  }
}

/**
 * Extend the default cell header
 */
export class PromptCellHeader extends Widget implements ICellHeader {
  constructor() {
    super();
    this.layout = new PanelLayout();
  }

  openPrompt(
    type: PromptModel.PromptType,
    commands: CommandRegistry,
    metadata?: IPromptMetadata
  ): void {
    if (!this.cell || !this.notebook || !(this.layout instanceof PanelLayout)) {
      return;
    }

    if (this._prompt && this._prompt.model.type === type) {
      this._prompt.focus();
      return;
    }

    this.closePrompt();
    this._prompt = new Prompt({
      type,
      commands,
      cell: this.cell,
      notebook: this.notebook,
      fileBrowser: this.fileBrowser ?? undefined,
      metadata
    });
    this._prompt.disposed.connect(this._onPromptDisposed);
    this.layout.addWidget(this._prompt);
    this.cell.addClass(CELL_OPENED_PROMPT_CLASS);
  }

  closePrompt(): void {
    const cell = this.cell;
    const notebook = this.notebook;
    if (this._prompt && this.layout) {
      const wasFocused = this._prompt.isFocused;
      this.layout.removeWidget(this._prompt);
      this._prompt.disposed.disconnect(this._onPromptDisposed);
      this._prompt.dispose();
      this._prompt = null;
      this.cell?.removeClass(CELL_OPENED_PROMPT_CLASS);

      if (wasFocused) {
        if (cell) {
          cell.activate();
        } else if (notebook) {
          notebook.activate();
        }
      }
    }
  }

  get promptTextAreaElement(): HTMLElement | null {
    return this._prompt?.textAreaElement ?? null;
  }

  get openedPromptType(): PromptModel.PromptType | null {
    return this._prompt?.model?.type ?? null;
  }

  private get cell(): Cell<ICellModel> | null {
    return this.parent instanceof Cell ? this.parent : null;
  }

  private get notebook(): NotebookPanel | null {
    return this.cell?.parent?.parent instanceof NotebookPanel
      ? this.cell.parent.parent
      : null;
  }

  private get fileBrowser(): FileBrowser | null {
    const mainPanel = this.notebook?.parent?.parent;
    if (mainPanel instanceof Panel) {
      const leftPanel = mainPanel.widgets.find(
        widget => widget.id === 'jp-left-stack'
      );
      if (leftPanel instanceof Panel) {
        return (
          (leftPanel.widgets.find(widget => widget instanceof FileBrowser) as
            | FileBrowser
            | undefined) ?? null
        );
      }
    }
    return null;
  }

  private _prompt: Prompt | null = null;
  private _onPromptDisposed = () => this.closePrompt();
}

export class PromptCodeCell extends CodeCell {
  constructor(opts: CodeCell.IOptions) {
    super(opts);
  }

  get promptCellHeader(): PromptCellHeader | null {
    if (this.layout instanceof PanelLayout) {
      const promptCelHeader = this.layout.widgets.find(
        widget => widget instanceof PromptCellHeader
      ) as PromptCellHeader | undefined;
      return promptCelHeader ?? null;
    }
    return null;
  }
}
