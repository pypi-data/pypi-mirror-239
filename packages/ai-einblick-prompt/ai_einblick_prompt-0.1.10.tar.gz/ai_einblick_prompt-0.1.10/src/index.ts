import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { IEditorServices } from '@jupyterlab/codeeditor';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IStateDB } from '@jupyterlab/statedb';
import { IStatusBar } from '@jupyterlab/statusbar';
import { ITranslator } from '@jupyterlab/translation';
import { ReadonlyJSONObject, UUID } from '@lumino/coreutils';

import { registerCommands } from './commands';
import { PromptContentFactory } from './contentFactory';
import { EinblickStatus } from './einblickStatus';
import { IPromptMetadata } from './promptMetadata';

const CONTENT_FACTORY_PLUGIN_ID = 'ai-einblick-prompt:factory';
const NOTEBOOK_PLUGIN_ID = 'ai-einblick-prompt:notebook';

export * from './icons';

/**
 * The content factory provider.
 */
const contentFactory: JupyterFrontEndPlugin<NotebookPanel.IContentFactory> = {
  id: CONTENT_FACTORY_PLUGIN_ID,
  provides: NotebookPanel.IContentFactory,
  requires: [IEditorServices],
  autoStart: true,
  activate: (app: JupyterFrontEnd, editorServices: IEditorServices) => {
    const editorFactory = editorServices.factoryService.newInlineEditor;
    return new PromptContentFactory({ editorFactory });
  }
};

async function loadPromptMetadata(
  app: JupyterFrontEnd,
  state: IStateDB
): Promise<IPromptMetadata> {
  let jupyterlabHash: string;
  const jupyterlabVersion = app.version;

  await app.restored;
  const existingState = await state.fetch(NOTEBOOK_PLUGIN_ID);
  if (existingState) {
    jupyterlabHash = (existingState as ReadonlyJSONObject)[
      'jupyterlabHash'
    ] as string;
  } else {
    jupyterlabHash = UUID.uuid4();
    await state.save(NOTEBOOK_PLUGIN_ID, {
      jupyterlabHash
    });
  }

  return {
    jupyterlabHash,
    jupyterlabVersion
  };
}

/**
 * Initialization data for the ai-einblick-prompt extension.
 */
const einblickAiPromptExtension: JupyterFrontEndPlugin<void> = {
  id: NOTEBOOK_PLUGIN_ID,
  description:
    'Generative AI tool made for data tasks. Generate, modify, and fix code.',
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker, IStateDB],
  optional: [ISettingRegistry, IStatusBar, ITranslator],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    notebookTracker: INotebookTracker,
    state: IStateDB,
    settingRegistry: ISettingRegistry | null,
    statusBar: IStatusBar | null,
    translator: ITranslator | null
  ) => {
    try {
      const versionParts = app.version.split('.');
      const majorVersion = parseInt(versionParts[0], 10);
      if (majorVersion >= 4) {
        loadPromptMetadata(app, state)
          .then(promptMetadata => {
            registerCommands(
              app,
              palette,
              notebookTracker,
              translator,
              promptMetadata
            );
          })
          .catch(reason => {
            console.error(
              'Failed to load prompt metadata for Einblick AI Prompt notebook plugin.',
              reason
            );
          });

        if (settingRegistry) {
          settingRegistry
            .load(NOTEBOOK_PLUGIN_ID)
            .then(settings => {
              console.log(
                'Einblick AI Prompt notebook plugin settings loaded:',
                settings
              );
            })
            .catch(reason => {
              console.error(
                'Failed to load settings for Einblick AI Prompt notebook plugin.',
                reason
              );
            });
        }
      }

      if (statusBar) {
        statusBar.registerStatusItem('einblick-extension', {
          item: new EinblickStatus(app.version, translator ?? undefined),
          align: 'right',
          rank: 6
        });
      }
      console.log('Einblick AI Prompt extension is activated!');
    } catch (error) {
      console.error('Error activating Einblick AI Prompt extension', error);
    }
  }
};

/**
 * Export this plugins as default.
 */
const plugins: JupyterFrontEndPlugin<any>[] = [
  einblickAiPromptExtension,
  contentFactory
];

export default plugins;
