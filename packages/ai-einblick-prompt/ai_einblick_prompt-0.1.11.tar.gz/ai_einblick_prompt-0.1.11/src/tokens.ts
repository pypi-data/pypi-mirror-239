import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { Token } from '@lumino/coreutils';
import { Widget } from '@lumino/widgets';

export interface IPromptPanel extends Widget {
  isOpen: boolean;
  notebook: NotebookPanel;
  notebookTracker: INotebookTracker;
}
export const IPromptPanel = new Token<IPromptPanel>(
  'ai-einblick-prompt:IPromptPanel',
  'A service for the prompt panel.'
);
