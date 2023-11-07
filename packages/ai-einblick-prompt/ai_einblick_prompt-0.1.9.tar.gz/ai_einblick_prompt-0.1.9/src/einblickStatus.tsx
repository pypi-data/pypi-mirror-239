import { Tooltip } from '@blueprintjs/core';
import { Popup, TextItem, showPopup } from '@jupyterlab/statusbar';
import {
  ITranslator,
  TranslationBundle,
  nullTranslator
} from '@jupyterlab/translation';
import {
  ReactWidget,
  VDomModel,
  VDomRenderer
} from '@jupyterlab/ui-components';
import * as React from 'react';

import { notConnectedIcon } from './icons';

/**
 * A pure function for rendering a Einblick status component.
 *
 * @param props: the props for rendering the component.
 *
 * @returns a tsx component for Einblick status.
 */
function EinblickStatusComponent(
  props: EinblickStatusComponent.IProps
): React.ReactElement<EinblickStatusComponent.IProps> {
  return (
    <div
      style={{
        padding: '0 5px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '5px'
      }}
    >
      {/* {props.isConnected ? (
        <connectedIcon.react tag="span" />
      ) : (
        <notConnectedIcon.react tag="span" />
      )} */}

      {!props.isConnected && <notConnectedIcon.react tag="span" />}

      <TextItem source={props.text} />
    </div>
  );
}

/**
 * A namespace for EinblickStatusComponent statics.
 */
namespace EinblickStatusComponent {
  /**
   * The props for the EinblickStatusComponent.
   */
  export interface IProps {
    text: string;
    isConnected: boolean;
    onClick?: () => void;
  }
}

/**
 * StatusBar item to display Einblick status.
 */
export class EinblickStatus extends VDomRenderer<EinblickStatus.Model> {
  protected translator: ITranslator;

  /**
   * Construct a new EinblickStatus status item.
   */
  constructor(appVersion: string, translator?: ITranslator) {
    super(new EinblickStatus.Model());

    // Uncomment this to make the button appear clickable
    // this.addClass('jp-mod-highlighted');

    this._appVersion = appVersion;
    this._appVersionParts = this._appVersion
      .split('.')
      .map((versionPart: string) => parseInt(versionPart, 10));

    this.translator = translator || nullTranslator;
    this._trans = this.translator.load('jupyterlab');
  }

  dispose(): void {
    if (this._popup) {
      this._popup.dispose();
    }
  }

  /**
   * Render the EinblickStatus status item.
   */
  render(): JSX.Element | null {
    if (!this.model) {
      return null;
    }

    let connected = true;
    let tooltipText: string | undefined = undefined;

    if (connected && this._appVersionParts[0] < 4) {
      connected = false;
      tooltipText = this._trans.__(
        'Version not supported, upgrade to >= %1',
        '4.0.0'
      );
    }

    return (
      <Tooltip compact disabled={!tooltipText} content={tooltipText}>
        <EinblickStatusComponent
          text={this._trans.__('Einblick AI')}
          isConnected={connected}
          onClick={this._handleClick}
        />
      </Tooltip>
    );
  }

  private _handleClick = () => {
    if (this._popup) {
      this._popup.dispose();
    }
    const body = ReactWidget.create(
      <div style={{ background: 'white', padding: '20px' }}>
        Login stuff here
      </div>
    );
    this._popup = showPopup({
      body: body,
      anchor: this,
      align: 'right'
    });
  };

  private _appVersion: string;
  private _appVersionParts: number[];
  private _popup: Popup | null = null;
  private _trans: TranslationBundle;
}

/**
 * A namespace for EinblickStatus statics.
 */
export namespace EinblickStatus {
  /**
   * A VDomModel for the EinblickStatus renderer.
   */
  export class Model extends VDomModel {}
}
