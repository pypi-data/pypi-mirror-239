import { Button, Icon, MenuItem, Spinner, TextArea } from '@blueprintjs/core';
import { ItemRenderer, Select } from '@blueprintjs/select';
import { Cell, ICellModel } from '@jupyterlab/cells';
import { FileBrowser } from '@jupyterlab/filebrowser';
import { NotebookPanel } from '@jupyterlab/notebook';
import {
  ITranslator,
  TranslationBundle,
  nullTranslator
} from '@jupyterlab/translation';
import {
  caretDownEmptyIcon,
  closeIcon,
  stopIcon
} from '@jupyterlab/ui-components';
import { VDomRenderer } from '@jupyterlab/ui-components';
import { CommandRegistry } from '@lumino/commands';
import React from 'react';

import { executePromptCommand } from './commands';
import { einblickIcon } from './icons';
import { PromptModel } from './model';
import { IPromptMetadata } from './promptMetadata';

type PromptTypeItem = {
  value: PromptModel.PromptType;
  text: string;
};
const PROMPT_TYPE_ITEM_MAP: Record<PromptModel.PromptType, PromptTypeItem> = {
  [PromptModel.PromptType.GENERATE_CELL]: {
    value: PromptModel.PromptType.GENERATE_CELL,
    text: 'Generate'
  },
  [PromptModel.PromptType.MODIFY_CELL]: {
    value: PromptModel.PromptType.MODIFY_CELL,
    text: 'Modify'
  },
  [PromptModel.PromptType.FIX_CELL]: {
    value: PromptModel.PromptType.FIX_CELL,
    text: 'Fix'
  }
};

const PROMPT_TYPE_ITEMS = Object.values(PROMPT_TYPE_ITEM_MAP);

type PromptComponentProps = {
  type: PromptModel.PromptType;
  placeholder: string;
  isProcessing: boolean;
  trans: TranslationBundle;
  userInput: string;
  onPromptTypeChange: (type: PromptModel.PromptType) => void;
  onUserInputChange: (value: string) => void;
  onSubmit: () => void;
  onCancel: () => void;
  onClose: () => void;
  onEscape?: () => void;
};
const PromptComponent = (props: PromptComponentProps): JSX.Element => {
  const isFixPrompt = props.type === PromptModel.PromptType.FIX_CELL;

  const componentRef = React.useRef<HTMLDivElement | null>(null);
  const textAreaRef = React.useRef<HTMLTextAreaElement | null>(null);
  const submitButtonRef = React.useRef<HTMLButtonElement | null>(null);

  const [isActive, setIsActive] = React.useState(false);

  const getShouldBeActive = React.useCallback(
    () =>
      Boolean(
        document.activeElement instanceof HTMLElement &&
          componentRef.current &&
          componentRef.current.contains(document.activeElement)
      ),
    []
  );
  const updateActiveState = React.useCallback(() => {
    setIsActive(getShouldBeActive());
  }, [getShouldBeActive]);

  React.useEffect(() => {
    const ref =
      props.type === PromptModel.PromptType.FIX_CELL
        ? submitButtonRef
        : textAreaRef;
    ref.current?.focus();
    setIsActive(Boolean(ref.current && ref.current === document.activeElement));
  }, []);

  const maybeSyncHeightToScrollHeight = React.useCallback(() => {
    if (textAreaRef.current && textAreaRef.current.scrollHeight > 0) {
      const scrollHeight = textAreaRef.current.scrollHeight;
      textAreaRef.current.style.height = '0px';
      const newHeight =
        textAreaRef.current.scrollHeight > 0
          ? textAreaRef.current.scrollHeight
          : scrollHeight;
      textAreaRef.current.style.height = `${newHeight}px`;
    }
  }, []);

  React.useEffect(() => {
    maybeSyncHeightToScrollHeight();
  }, [maybeSyncHeightToScrollHeight]);

  const getIsUserInputValid = React.useCallback(
    (value: string): boolean => {
      return (
        props.type === PromptModel.PromptType.FIX_CELL ||
        value.trim().length > 0
      );
    },
    [props.type]
  );

  const [isUserInputValid, setIsUserInputValid] = React.useState(
    getIsUserInputValid(props.userInput)
  );

  const [value, setValue] = React.useState(props.userInput);
  React.useEffect(() => {
    setValue(props.userInput);
  }, [props.userInput]);

  const onPromptChange = React.useCallback(
    (evt: React.ChangeEvent<HTMLTextAreaElement>) => {
      maybeSyncHeightToScrollHeight();
      setValue(evt.target.value);
      props.onUserInputChange(evt.target.value);
      setIsUserInputValid(getIsUserInputValid(evt.target.value));
    },
    [props.onUserInputChange, maybeSyncHeightToScrollHeight]
  );

  const renderPromptTypeItem: ItemRenderer<PromptTypeItem> = React.useCallback(
    (promptTypeItem, { handleClick, handleFocus, modifiers, query }) => {
      if (!modifiers.matchesPredicate) {
        return null;
      }
      return (
        <MenuItem
          active={modifiers.active}
          disabled={modifiers.disabled}
          key={promptTypeItem.value}
          onClick={handleClick}
          onFocus={handleFocus}
          roleStructure="listoption"
          text={props.trans.__(promptTypeItem.text)}
        />
      );
    },
    [props.trans]
  );

  React.useEffect(() => {
    const handleEscape = (evt: KeyboardEvent) => {
      if (
        evt.keyCode === 27 &&
        document.activeElement instanceof HTMLElement &&
        getShouldBeActive()
      ) {
        evt.preventDefault();
        evt.stopPropagation();
        document.activeElement.blur();
        props.onEscape?.();
      }
    };
    document.addEventListener('keydown', handleEscape, { capture: true });
    return () => {
      document.removeEventListener('keydown', handleEscape, { capture: true });
    };
  }, [getShouldBeActive]);

  return (
    <div
      className={`c-prompt${isActive ? ' c-prompt--is-active' : ''}`}
      ref={componentRef}
    >
      <div className="c-prompt__type-select-container">
        <Select<PromptTypeItem>
          filterable={false}
          items={PROMPT_TYPE_ITEMS}
          itemRenderer={renderPromptTypeItem}
          popoverProps={{
            minimal: true
          }}
          menuProps={{
            className: 'c-prompt__type-select-listbox'
          }}
          popoverTargetProps={{
            className: 'c-prompt__type-select-popover-target'
          }}
          onItemSelect={promptTypeItem => {
            props.onPromptTypeChange(promptTypeItem.value);
          }}
        >
          <Button
            className="c-prompt__type-select-button"
            text={props.trans.__(PROMPT_TYPE_ITEM_MAP[props.type].text)}
            rightIcon={<caretDownEmptyIcon.react />}
            placeholder={props.trans.__('Select an action')}
          />
        </Select>
      </div>
      <div className="c-prompt__logo-container">
        <div className="c-prompt__logo">
          {props.isProcessing ? (
            <Spinner size={20} />
          ) : (
            <einblickIcon.react height="20px" width="20px" />
          )}
        </div>
      </div>
      {!isFixPrompt && (
        <TextArea
          value={value}
          className="c-prompt__input-textarea"
          inputRef={textAreaRef}
          placeholder={props.placeholder}
          fill
          disabled={props.isProcessing}
          onKeyDownCapture={evt => {
            if (evt.nativeEvent instanceof KeyboardEvent) {
              if (evt.keyCode === 13) {
                evt.stopPropagation();
                evt.preventDefault();
                if (isUserInputValid) {
                  if (evt.target === textAreaRef.current) {
                    textAreaRef.current.blur();
                  }
                  props.onSubmit();
                }
              }
            }
          }}
          onFocus={() => updateActiveState()}
          onBlur={() => updateActiveState()}
          onChange={onPromptChange}
        />
      )}
      {isFixPrompt && (
        <div className="c-prompt__message">Fix any errors in the cell.</div>
      )}
      <div className="c-prompt__button-container">
        <div className="c-prompt__buttons">
          {!props.isProcessing && (
            <Button
              minimal
              ref={submitButtonRef}
              className="c-prompt__submit-button"
              disabled={props.isProcessing || !isUserInputValid}
              onClick={props.onSubmit}
              icon={<Icon icon="send-message" size={12} />}
              onFocus={() => updateActiveState()}
              onBlur={() => updateActiveState()}
            />
          )}
          {props.isProcessing && (
            <Button
              minimal
              className="c-prompt__cancel-button"
              disabled={!props.isProcessing}
              onClick={props.onCancel}
              icon={<stopIcon.react />}
              onFocus={() => updateActiveState()}
              onBlur={() => updateActiveState()}
            />
          )}
          <Button
            minimal
            className="c-prompt__close-button"
            onClick={props.onClose}
            icon={<closeIcon.react />}
            onFocus={() => updateActiveState()}
            onBlur={() => updateActiveState()}
          />
        </div>
      </div>
    </div>
  );
};

export interface IPromptOptions {
  type: PromptModel.PromptType;
  cell: Cell<ICellModel>;
  notebook: NotebookPanel;
  commands: CommandRegistry;
  fileBrowser?: FileBrowser;
  translator?: ITranslator;
  metadata?: IPromptMetadata;
}

/**
 * A VDomRenderer widget for displaying the prompt.
 */
export class Prompt extends VDomRenderer<PromptModel.Model> {
  /**
   * Construct the prompt widget.
   */
  constructor(opts: IPromptOptions) {
    super(
      new PromptModel.Model(
        opts.type,
        opts.cell,
        opts.notebook,
        opts.fileBrowser,
        opts.translator,
        opts.metadata
      )
    );
    const translator = opts.translator || nullTranslator;
    this.commands = opts.commands;
    this.translator = translator;
    this.trans = this.translator.load('jupyterlab');
  }

  /**
   * Render the prompt component.
   */
  render(): JSX.Element | null {
    if (this.model === null) {
      return null;
    } else {
      return (
        <PromptComponent
          type={this.model.type}
          placeholder={this.model.placeholder}
          isProcessing={this.model.isProcessing}
          trans={this.trans}
          userInput={this.model.userInput}
          onUserInputChange={value => {
            this.model.userInput = value;
          }}
          onPromptTypeChange={type => this.changePromptType(type)}
          onSubmit={() => this.model.execute()}
          onCancel={() => this.cancel()}
          onClose={() => this.dispose()}
          onEscape={() => {
            this.model.notebook.activate();
          }}
        />
      );
    }
  }

  focus(): void {
    if (this.model.isProcessing && this.cancelButtonElement) {
      this.cancelButtonElement.focus();
      return;
    }

    if (this.model.type === PromptModel.PromptType.FIX_CELL) {
      this.submitButtonElement?.focus();
    } else {
      this.textAreaElement?.focus();
    }
  }

  get isFocused(): boolean {
    return Boolean(
      document.activeElement instanceof HTMLElement &&
        this.element?.contains(document.activeElement)
    );
  }

  cancel(): void {
    this.model.cancel();
  }

  dispose(): void {
    this.model?.cancel();
    super.dispose();
  }

  get element(): HTMLElement | null {
    const element = this.node.getElementsByClassName('c-prompt')[0];
    if (element instanceof HTMLElement) {
      return element;
    }
    return null;
  }

  get textAreaElement(): HTMLTextAreaElement | null {
    const textAreaElement = this.node.getElementsByClassName(
      'c-prompt__input-textarea'
    )[0];
    if (textAreaElement instanceof HTMLTextAreaElement) {
      return textAreaElement;
    }
    return null;
  }

  get submitButtonElement(): HTMLButtonElement | null {
    const submitButtonElement = this.node.getElementsByClassName(
      'c-prompt__submit-button'
    )[0];
    if (submitButtonElement instanceof HTMLButtonElement) {
      return submitButtonElement;
    }
    return null;
  }

  get closeButtonElement(): HTMLButtonElement | null {
    const closeButtonElement = this.node.getElementsByClassName(
      'c-prompt__close-button'
    )[0];
    if (closeButtonElement instanceof HTMLButtonElement) {
      return closeButtonElement;
    }
    return null;
  }

  get cancelButtonElement(): HTMLButtonElement | null {
    const cancelButtonElement = this.node.getElementsByClassName(
      'c-prompt__cancel-button'
    )[0];
    if (cancelButtonElement instanceof HTMLButtonElement) {
      return cancelButtonElement;
    }
    return null;
  }

  private changePromptType(type: PromptModel.PromptType): void {
    executePromptCommand(
      type,
      this.model.cell,
      this.model.notebook,
      this.commands
    );
  }

  commands: CommandRegistry;
  translator: ITranslator;
  trans: TranslationBundle;
}
