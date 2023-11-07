"use strict";
(self["webpackChunkai_einblick_prompt"] = self["webpackChunkai_einblick_prompt"] || []).push([["lib_index_js"],{

/***/ "./lib/cancellablePromise.js":
/*!***********************************!*\
  !*** ./lib/cancellablePromise.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CancelToken: () => (/* binding */ CancelToken),
/* harmony export */   CancellablePromise: () => (/* binding */ CancellablePromise),
/* harmony export */   CancellablePromiseRace: () => (/* binding */ CancellablePromiseRace)
/* harmony export */ });
/**
 * This class represents a way to cancel a promise for a specific reason provided in the constructor.
 * The promise will be rejected without throwing so anything awaiting that promise immediately continues.
 */
class CancelToken {
    constructor(Reason) {
        this.Reason = Reason;
        this._rejects = [];
        this._isCancelled = false;
    }
    /**
     * Register a reject call from a Promise.
     * The reject function will be called using this CancelToken's reason when its Cancel function is called
     * @param reject
     */
    Register(reject) {
        this._rejects.push(reject);
    }
    /**
     * Unregister a reject call from a Promise.
     * The reject function will no longer be called using this CancelToken's reason when its Cancel function is called
     * @param reject
     */
    Unregister(reject) {
        const rejectionIndex = this._rejects.indexOf(reject);
        if (rejectionIndex >= 0) {
            this._rejects.splice(rejectionIndex, 1);
        }
    }
    get IsCancelled() {
        return this._isCancelled;
    }
    /**
     * Cancels any relevant CancellablePromise by cleanly rejecting it
     */
    Cancel() {
        if (this._isCancelled) {
            return;
        }
        for (const reject of this._rejects) {
            reject(this.Reason);
        }
        this._isCancelled = true;
    }
}
/**
 * Function to construct a Promise with a CancelToken that can be used to cancel the promise
 * @param executor Regular executor to be passed into Promise
 * @param cancelToken CancelToken used to cancel the promise
 * @returns
 */
async function CancellablePromise(executor, ...cancelTokens) {
    let cancel = null;
    try {
        return await new Promise((resolve, reject) => {
            cancel = reject;
            for (const cancelToken of cancelTokens) {
                cancelToken.Register(cancel);
            }
            if (cancelTokens.some(cancelToken => cancelToken.IsCancelled)) {
                reject();
            }
            else {
                executor(resolve, reject);
            }
        });
    }
    catch (error) {
        if (!cancelTokens.some(cancelToken => error === cancelToken.Reason)) {
            throw error;
        }
    }
    finally {
        if (cancel) {
            for (const cancelToken of cancelTokens) {
                cancelToken.Unregister(cancel);
            }
        }
    }
    return undefined;
}
/**
 * Function to construct a Promise race with a CancelToken that can be used to cancel the outer promise
 * @param promises Promises to race
 * @param cancelToken CancelToken used to cancel the promise
 * @returns
 */
async function CancellablePromiseRace(promises, ...cancelTokens) {
    let cancel = null;
    try {
        return await Promise.race([
            ...promises,
            new Promise((_, reject) => {
                cancel = reject;
                for (const cancelToken of cancelTokens) {
                    cancelToken.Register(cancel);
                }
                if (cancelTokens.some(cancelToken => cancelToken.IsCancelled)) {
                    reject();
                }
            })
        ]);
    }
    catch (error) {
        if (!cancelTokens.some(cancelToken => error === cancelToken.Reason)) {
            throw error;
        }
    }
    finally {
        if (cancel) {
            for (const cancelToken of cancelTokens) {
                cancelToken.Unregister(cancel);
            }
        }
    }
    return undefined;
}


/***/ }),

/***/ "./lib/commands.js":
/*!*************************!*\
  !*** ./lib/commands.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CONTEXTUAL_PROMPT_COMMAND_ID: () => (/* binding */ CONTEXTUAL_PROMPT_COMMAND_ID),
/* harmony export */   EINBLICK_COMMAND_CATEGORY: () => (/* binding */ EINBLICK_COMMAND_CATEGORY),
/* harmony export */   FIX_COMMAND_ID: () => (/* binding */ FIX_COMMAND_ID),
/* harmony export */   GENERATE_COMMAND_ID: () => (/* binding */ GENERATE_COMMAND_ID),
/* harmony export */   MODIFY_COMMAND_ID: () => (/* binding */ MODIFY_COMMAND_ID),
/* harmony export */   TOGGLE_CONTEXTUAL_PROMPT_COMMAND_ID: () => (/* binding */ TOGGLE_CONTEXTUAL_PROMPT_COMMAND_ID),
/* harmony export */   executePromptCommand: () => (/* binding */ executePromptCommand),
/* harmony export */   getContextualPromptType: () => (/* binding */ getContextualPromptType),
/* harmony export */   registerCommands: () => (/* binding */ registerCommands)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _contentFactory__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./contentFactory */ "./lib/contentFactory.js");
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./model */ "./lib/model.js");



const CONTEXTUAL_PROMPT_COMMAND_ID = 'ai-einblick-prompt:contextual-prompt';
const TOGGLE_CONTEXTUAL_PROMPT_COMMAND_ID = 'ai-einblick-prompt:toggle-contextual-prompt';
const GENERATE_COMMAND_ID = 'ai-einblick-prompt:generate';
const MODIFY_COMMAND_ID = 'ai-einblick-prompt:modify';
const FIX_COMMAND_ID = 'ai-einblick-prompt:fix';
const EINBLICK_COMMAND_CATEGORY = 'Einblick';
const executePromptCommand = (type, cell, notebook, commands) => {
    if (cell && notebook) {
        const newCommandArgs = {
            cell: cell.id,
            notebook: notebook.id
        };
        switch (type) {
            case _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.GENERATE_CELL:
                commands.execute(GENERATE_COMMAND_ID, newCommandArgs);
                break;
            case _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.MODIFY_CELL:
                commands.execute(MODIFY_COMMAND_ID, newCommandArgs);
                break;
            case _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.FIX_CELL:
                commands.execute(FIX_COMMAND_ID, newCommandArgs);
                break;
        }
    }
};
const getContextualPromptType = (cell, notebook) => {
    let type = _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.GENERATE_CELL;
    if ((0,_model__WEBPACK_IMPORTED_MODULE_1__.canExecuteFixCell)(cell, notebook)) {
        type = _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.FIX_CELL;
    }
    else {
        const cellSource = cell.model.toJSON().source;
        const cellContent = Array.isArray(cellSource)
            ? cellSource.join('\n')
            : cellSource;
        if (cellContent.trim() !== '') {
            type = _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.MODIFY_CELL;
        }
    }
    return type;
};
const registerCommands = (app, palette, notebookTracker, translator, promptMetadata) => {
    const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator).load('jupyterlab');
    const formAndExecutePromptCommand = (args, type) => {
        var _a, _b;
        let cell = null;
        let notebook = null;
        if (args.notebook) {
            if (((_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.id) === args.notebook) {
                notebook = notebookTracker.currentWidget;
            }
        }
        else {
            notebook = notebookTracker.currentWidget;
        }
        if (args.cell) {
            cell = (_b = notebook === null || notebook === void 0 ? void 0 : notebook.content.widgets.find(c => c.id === args.cell)) !== null && _b !== void 0 ? _b : null;
        }
        else {
            cell = notebookTracker.activeCell;
        }
        if (cell instanceof _contentFactory__WEBPACK_IMPORTED_MODULE_2__.PromptCodeCell && notebook) {
            if (cell.promptCellHeader) {
                cell.promptCellHeader.openPrompt(type, app.commands, promptMetadata !== null && promptMetadata !== void 0 ? promptMetadata : undefined);
            }
        }
    };
    app.commands.addCommand(CONTEXTUAL_PROMPT_COMMAND_ID, {
        label: trans.__('Einblick AI: Prompt'),
        execute: () => {
            let cell = null;
            let notebook = null;
            let type = _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.GENERATE_CELL;
            cell = notebookTracker.activeCell;
            notebook = notebookTracker.currentWidget;
            if (cell instanceof _contentFactory__WEBPACK_IMPORTED_MODULE_2__.PromptCodeCell && notebook) {
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
                        var _a;
                        if (!(cell instanceof _contentFactory__WEBPACK_IMPORTED_MODULE_2__.PromptCodeCell)) {
                            return false;
                        }
                        return (document.activeElement ===
                            ((_a = cell.promptCellHeader) === null || _a === void 0 ? void 0 : _a.promptTextAreaElement));
                    });
                    if (cellWithFocusedPrompt === null || cellWithFocusedPrompt === void 0 ? void 0 : cellWithFocusedPrompt.promptCellHeader) {
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
            formAndExecutePromptCommand(args, _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.GENERATE_CELL);
        }
    });
    palette.addItem({
        command: GENERATE_COMMAND_ID,
        category: EINBLICK_COMMAND_CATEGORY
    });
    app.commands.addCommand(MODIFY_COMMAND_ID, {
        label: trans.__('Einblick AI: Modify'),
        execute: args => {
            formAndExecutePromptCommand(args, _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.MODIFY_CELL);
        }
    });
    palette.addItem({
        command: MODIFY_COMMAND_ID,
        category: EINBLICK_COMMAND_CATEGORY
    });
    app.commands.addCommand(FIX_COMMAND_ID, {
        label: trans.__('Einblick AI: Fix'),
        execute: args => {
            formAndExecutePromptCommand(args, _model__WEBPACK_IMPORTED_MODULE_1__.PromptModel.PromptType.FIX_CELL);
        }
    });
    palette.addItem({
        command: FIX_COMMAND_ID,
        category: EINBLICK_COMMAND_CATEGORY
    });
};


/***/ }),

/***/ "./lib/contentFactory.js":
/*!*******************************!*\
  !*** ./lib/contentFactory.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PromptCellHeader: () => (/* binding */ PromptCellHeader),
/* harmony export */   PromptCodeCell: () => (/* binding */ PromptCodeCell),
/* harmony export */   PromptContentFactory: () => (/* binding */ PromptContentFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _prompt__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./prompt */ "./lib/prompt.js");





const CELL_OPENED_PROMPT_CLASS = 'jp-cell--prompt-opened';
/**
 * Extend the default implementation of an `IContentFactory`.
 */
class PromptContentFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookPanel.ContentFactory {
    constructor(options) {
        super(options);
    }
    createCellHeader() {
        return new PromptCellHeader();
    }
    createCodeCell(options) {
        return new PromptCodeCell(options);
    }
}
/**
 * Extend the default cell header
 */
class PromptCellHeader extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor() {
        super();
        this._prompt = null;
        this._onPromptDisposed = () => this.closePrompt();
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.PanelLayout();
    }
    openPrompt(type, commands, metadata) {
        var _a;
        if (!this.cell || !this.notebook || !(this.layout instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.PanelLayout)) {
            return;
        }
        if (this._prompt && this._prompt.model.type === type) {
            this._prompt.focus();
            return;
        }
        this.closePrompt();
        this._prompt = new _prompt__WEBPACK_IMPORTED_MODULE_4__.Prompt({
            type,
            commands,
            cell: this.cell,
            notebook: this.notebook,
            fileBrowser: (_a = this.fileBrowser) !== null && _a !== void 0 ? _a : undefined,
            metadata
        });
        this._prompt.disposed.connect(this._onPromptDisposed);
        this.layout.addWidget(this._prompt);
        this.cell.addClass(CELL_OPENED_PROMPT_CLASS);
    }
    closePrompt() {
        var _a;
        const cell = this.cell;
        const notebook = this.notebook;
        if (this._prompt && this.layout) {
            const wasFocused = this._prompt.isFocused;
            this.layout.removeWidget(this._prompt);
            this._prompt.disposed.disconnect(this._onPromptDisposed);
            this._prompt.dispose();
            this._prompt = null;
            (_a = this.cell) === null || _a === void 0 ? void 0 : _a.removeClass(CELL_OPENED_PROMPT_CLASS);
            if (wasFocused) {
                if (cell) {
                    cell.activate();
                }
                else if (notebook) {
                    notebook.activate();
                }
            }
        }
    }
    get promptTextAreaElement() {
        var _a, _b;
        return (_b = (_a = this._prompt) === null || _a === void 0 ? void 0 : _a.textAreaElement) !== null && _b !== void 0 ? _b : null;
    }
    get openedPromptType() {
        var _a, _b, _c;
        return (_c = (_b = (_a = this._prompt) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.type) !== null && _c !== void 0 ? _c : null;
    }
    get cell() {
        return this.parent instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.Cell ? this.parent : null;
    }
    get notebook() {
        var _a, _b;
        return ((_b = (_a = this.cell) === null || _a === void 0 ? void 0 : _a.parent) === null || _b === void 0 ? void 0 : _b.parent) instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookPanel
            ? this.cell.parent.parent
            : null;
    }
    get fileBrowser() {
        var _a, _b, _c;
        const mainPanel = (_b = (_a = this.notebook) === null || _a === void 0 ? void 0 : _a.parent) === null || _b === void 0 ? void 0 : _b.parent;
        if (mainPanel instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Panel) {
            const leftPanel = mainPanel.widgets.find(widget => widget.id === 'jp-left-stack');
            if (leftPanel instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Panel) {
                return ((_c = leftPanel.widgets.find(widget => widget instanceof _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.FileBrowser)) !== null && _c !== void 0 ? _c : null);
            }
        }
        return null;
    }
}
class PromptCodeCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell {
    constructor(opts) {
        super(opts);
    }
    get promptCellHeader() {
        if (this.layout instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.PanelLayout) {
            const promptCelHeader = this.layout.widgets.find(widget => widget instanceof PromptCellHeader);
            return promptCelHeader !== null && promptCelHeader !== void 0 ? promptCelHeader : null;
        }
        return null;
    }
}


/***/ }),

/***/ "./lib/einblickStatus.js":
/*!*******************************!*\
  !*** ./lib/einblickStatus.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   EinblickStatus: () => (/* binding */ EinblickStatus)
/* harmony export */ });
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @blueprintjs/core */ "webpack/sharing/consume/default/@blueprintjs/core/@blueprintjs/core?f973");
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");






/**
 * A pure function for rendering a Einblick status component.
 *
 * @param props: the props for rendering the component.
 *
 * @returns a tsx component for Einblick status.
 */
function EinblickStatusComponent(props) {
    return (react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", { style: {
            padding: '0 5px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '5px'
        } },
        !props.isConnected && react__WEBPACK_IMPORTED_MODULE_4__.createElement(_icons__WEBPACK_IMPORTED_MODULE_5__.notConnectedIcon.react, { tag: "span" }),
        react__WEBPACK_IMPORTED_MODULE_4__.createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { source: props.text })));
}
/**
 * StatusBar item to display Einblick status.
 */
class EinblickStatus extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.VDomRenderer {
    /**
     * Construct a new EinblickStatus status item.
     */
    constructor(appVersion, translator) {
        super(new EinblickStatus.Model());
        this._handleClick = () => {
            if (this._popup) {
                this._popup.dispose();
            }
            const body = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", { style: { background: 'white', padding: '20px' } }, "Login stuff here"));
            this._popup = (0,_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.showPopup)({
                body: body,
                anchor: this,
                align: 'right'
            });
        };
        this._popup = null;
        // Uncomment this to make the button appear clickable
        // this.addClass('jp-mod-highlighted');
        this._appVersion = appVersion;
        this._appVersionParts = this._appVersion
            .split('.')
            .map((versionPart) => parseInt(versionPart, 10));
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
    }
    dispose() {
        if (this._popup) {
            this._popup.dispose();
        }
    }
    /**
     * Render the EinblickStatus status item.
     */
    render() {
        if (!this.model) {
            return null;
        }
        let connected = true;
        let tooltipText = undefined;
        if (connected && this._appVersionParts[0] < 4) {
            connected = false;
            tooltipText = this._trans.__('Version not supported, upgrade to >= %1', '4.0.0');
        }
        return (react__WEBPACK_IMPORTED_MODULE_4__.createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Tooltip, { compact: true, disabled: !tooltipText, content: tooltipText },
            react__WEBPACK_IMPORTED_MODULE_4__.createElement(EinblickStatusComponent, { text: this._trans.__('Einblick AI'), isConnected: connected, onClick: this._handleClick })));
    }
}
/**
 * A namespace for EinblickStatus statics.
 */
(function (EinblickStatus) {
    /**
     * A VDomModel for the EinblickStatus renderer.
     */
    class Model extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.VDomModel {
    }
    EinblickStatus.Model = Model;
})(EinblickStatus || (EinblickStatus = {}));


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   connectedIcon: () => (/* binding */ connectedIcon),
/* harmony export */   einblickIcon: () => (/* binding */ einblickIcon),
/* harmony export */   notConnectedIcon: () => (/* binding */ notConnectedIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _static_icons_connected_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../static/icons/connected.svg */ "./static/icons/connected.svg");
/* harmony import */ var _static_icons_einblick_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../static/icons/einblick.svg */ "./static/icons/einblick.svg");
/* harmony import */ var _static_icons_notConnected_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../static/icons/notConnected.svg */ "./static/icons/notConnected.svg");




const connectedIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'ai-einblick-prompt:connected',
    svgstr: _static_icons_connected_svg__WEBPACK_IMPORTED_MODULE_1__
});
const einblickIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'ai-einblick-prompt:einblick',
    svgstr: _static_icons_einblick_svg__WEBPACK_IMPORTED_MODULE_2__
});
const notConnectedIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'ai-einblick-prompt:not-connected',
    svgstr: _static_icons_notConnected_svg__WEBPACK_IMPORTED_MODULE_3__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   connectedIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_8__.connectedIcon),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   einblickIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_8__.einblickIcon),
/* harmony export */   notConnectedIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_8__.notConnectedIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var _contentFactory__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./contentFactory */ "./lib/contentFactory.js");
/* harmony import */ var _einblickStatus__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./einblickStatus */ "./lib/einblickStatus.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");











const CONTENT_FACTORY_PLUGIN_ID = 'ai-einblick-prompt:factory';
const NOTEBOOK_PLUGIN_ID = 'ai-einblick-prompt:notebook';

/**
 * The content factory provider.
 */
const contentFactory = {
    id: CONTENT_FACTORY_PLUGIN_ID,
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookPanel.IContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new _contentFactory__WEBPACK_IMPORTED_MODULE_9__.PromptContentFactory({ editorFactory });
    }
};
async function loadPromptMetadata(app, state) {
    let jupyterlabHash;
    const jupyterlabVersion = app.version;
    await app.restored;
    const existingState = await state.fetch(NOTEBOOK_PLUGIN_ID);
    if (existingState) {
        jupyterlabHash = existingState['jupyterlabHash'];
    }
    else {
        jupyterlabHash = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_7__.UUID.uuid4();
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
const einblickAiPromptExtension = {
    id: NOTEBOOK_PLUGIN_ID,
    description: 'Generative AI tool made for data tasks. Generate, modify, and fix code.',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_4__.IStateDB],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry, _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__.IStatusBar, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    activate: (app, palette, notebookTracker, state, settingRegistry, statusBar, translator) => {
        try {
            const versionParts = app.version.split('.');
            const majorVersion = parseInt(versionParts[0], 10);
            if (majorVersion >= 4) {
                loadPromptMetadata(app, state)
                    .then(promptMetadata => {
                    (0,_commands__WEBPACK_IMPORTED_MODULE_10__.registerCommands)(app, palette, notebookTracker, translator, promptMetadata);
                })
                    .catch(reason => {
                    console.error('Failed to load prompt metadata for Einblick AI Prompt notebook plugin.', reason);
                });
                if (settingRegistry) {
                    settingRegistry
                        .load(NOTEBOOK_PLUGIN_ID)
                        .then(settings => {
                        console.log('Einblick AI Prompt notebook plugin settings loaded:', settings);
                    })
                        .catch(reason => {
                        console.error('Failed to load settings for Einblick AI Prompt notebook plugin.', reason);
                    });
                }
            }
            if (statusBar) {
                statusBar.registerStatusItem('einblick-extension', {
                    item: new _einblickStatus__WEBPACK_IMPORTED_MODULE_11__.EinblickStatus(app.version, translator !== null && translator !== void 0 ? translator : undefined),
                    align: 'right',
                    rank: 6
                });
            }
            console.log('Einblick AI Prompt extension is activated!');
        }
        catch (error) {
            console.error('Error activating Einblick AI Prompt extension', error);
        }
    }
};
/**
 * Export this plugins as default.
 */
const plugins = [
    einblickAiPromptExtension,
    contentFactory
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/model.js":
/*!**********************!*\
  !*** ./lib/model.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PromptModel: () => (/* binding */ PromptModel),
/* harmony export */   canExecuteFixCell: () => (/* binding */ canExecuteFixCell)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/nbformat */ "webpack/sharing/consume/default/@jupyterlab/nbformat");
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var anser__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! anser */ "webpack/sharing/consume/default/anser/anser");
/* harmony import */ var anser__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(anser__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _cancellablePromise__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./cancellablePromise */ "./lib/cancellablePromise.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");







const INPUT_CHARACTER_MAX = 2000;
var PromptModel;
(function (PromptModel) {
    PromptModel.AskUserToolName = 'ask-user';
    PromptModel.FilterToolName = 'row-subset-tool';
    PromptModel.PythonToolName = 'generate-python-code';
    let PromptType;
    (function (PromptType) {
        PromptType["GENERATE_CELL"] = "generate-cell";
        PromptType["MODIFY_CELL"] = "modify-cell";
        PromptType["FIX_CELL"] = "fix-cell";
    })(PromptType = PromptModel.PromptType || (PromptModel.PromptType = {}));
    const getPlaceholders = (trans) => {
        return {
            [PromptType.GENERATE_CELL]: trans.__('What do you want to add?'),
            [PromptType.MODIFY_CELL]: trans.__('What do you want to modify?'),
            [PromptType.FIX_CELL]: trans.__('')
        };
    };
    /**
     * A VDomModel for a Prompt.
     */
    class Model extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.VDomModel {
        constructor(type, cell, notebook, fileBrowser, translator, metadata) {
            super();
            this._metadata = null;
            this._placeholder = '';
            this._userInput = '';
            this._errorMessage = null;
            this._cancelToken = null;
            this.translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
            this._trans = this.translator.load('jupyterlab');
            this._type = type;
            this._cell = cell;
            this._notebook = notebook;
            this._fileBrowser = fileBrowser !== null && fileBrowser !== void 0 ? fileBrowser : null;
            this._metadata = metadata !== null && metadata !== void 0 ? metadata : null;
            this._placeholder = getPlaceholders(this._trans)[this._type];
            this._processingMessage = this._trans.__('Working on it...');
        }
        get type() {
            return this._type;
        }
        get cell() {
            return this._cell;
        }
        get notebook() {
            return this._notebook;
        }
        get placeholder() {
            return this._placeholder;
        }
        get processingMessage() {
            return this._processingMessage;
        }
        get errorMessage() {
            return this._errorMessage;
        }
        get userInput() {
            return this._userInput;
        }
        set userInput(value) {
            this._userInput = value;
            this.stateChanged.emit();
        }
        get isProcessing() {
            return this._cancelToken !== null;
        }
        get isErroneous() {
            return typeof this._errorMessage === 'string';
        }
        async execute() {
            if (this._cancelToken) {
                return;
            }
            try {
                this._cancelToken = new _cancellablePromise__WEBPACK_IMPORTED_MODULE_5__.CancelToken(Error('User cancelled'));
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
            }
            catch (error) {
                this._errorMessage =
                    'There was an unexpected error executing the prompt.';
            }
            finally {
                this._cancelToken = null;
                this.stateChanged.emit();
            }
        }
        cancel() {
            var _a;
            if (this._cancelToken && !this._cancelToken.IsCancelled) {
                (_a = this._cancelToken) === null || _a === void 0 ? void 0 : _a.Cancel();
            }
        }
        async getCellContext() {
            const cellModel = this._cell.model;
            if (!cellModel || !(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.isCodeCellModel)(cellModel)) {
                throw Error('Need valid code cell model.');
            }
            const notebookModel = this._notebook.model;
            if (!notebookModel) {
                throw Error('Need valid notebook model.');
            }
            if (!this._cancelToken) {
                throw Error('Cancel token should not be null');
            }
            return _utils__WEBPACK_IMPORTED_MODULE_6__.PromptContextUtil.GetContextForActiveNotebookCellBasedOnRadius(this._cell, this._notebook, this._fileBrowser, 1000, this._cancelToken);
        }
        async generate(input, cancelToken) {
            const context = await this.getCellContext();
            if (cancelToken.IsCancelled) {
                return;
            }
            const agentRequest = {
                Prompt: this.truncateEnd(input, INPUT_CHARACTER_MAX),
                Context: context,
                Tools: [PromptModel.PythonToolName]
            };
            if (this._metadata) {
                agentRequest.Metadata = { ...this._metadata };
            }
            const result = await (0,_cancellablePromise__WEBPACK_IMPORTED_MODULE_5__.CancellablePromiseRace)([
                fetch(`${_utils__WEBPACK_IMPORTED_MODULE_6__.apiHostName}/ai/prompt/python`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(agentRequest)
                })
            ], cancelToken);
            if (cancelToken.IsCancelled) {
                return;
            }
            else if (!result) {
                throw Error('Unable to process prompt');
            }
            else if (!result.ok) {
                throw Error(`${result.status}: ${result.statusText}`);
            }
            const resultJson = await (0,_cancellablePromise__WEBPACK_IMPORTED_MODULE_5__.CancellablePromiseRace)([result.json()], cancelToken);
            if (cancelToken.IsCancelled) {
                return;
            }
            else if (!resultJson) {
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
        async modify(input, cancelToken) {
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
            const refineRequest = {
                Prompt: this.truncateEnd(input, INPUT_CHARACTER_MAX),
                Context: context,
                Current: activeCodeCellContent,
                History: [],
                ErrorMessage: null
            };
            if (this._metadata) {
                refineRequest.Metadata = { ...this._metadata };
            }
            const result = await (0,_cancellablePromise__WEBPACK_IMPORTED_MODULE_5__.CancellablePromiseRace)([
                fetch(`${_utils__WEBPACK_IMPORTED_MODULE_6__.apiHostName}/ai/refinePrompt/python-notebook-cell`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(refineRequest)
                })
            ], cancelToken);
            if (cancelToken.IsCancelled) {
                return;
            }
            else if (!result) {
                throw Error('Unable to process prompt');
            }
            else if (!result.ok) {
                throw Error(`${result.status}: ${result.statusText}`);
            }
            const resultJson = await (0,_cancellablePromise__WEBPACK_IMPORTED_MODULE_5__.CancellablePromiseRace)([result.json()], cancelToken);
            if (cancelToken.IsCancelled) {
                return;
            }
            else if (!resultJson) {
                throw Error('Unable to process prompt');
            }
            const newCode = resultJson === null || resultJson === void 0 ? void 0 : resultJson.data;
            if (resultJson.error) {
                throw Error(resultJson.error);
            }
            if (resultJson.isValid && typeof newCode === 'string') {
                this.replaceCellContent(newCode);
                this.cell.activate();
            }
            this.userInput = '';
        }
        async fix(cancelToken) {
            const cellModel = this._cell.model;
            if (!cellModel || !(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.isCodeCellModel)(cellModel)) {
                throw new Error('Need valid code cell model.');
            }
            const errorOutput = cellModel.outputs.toJSON().find(_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1__.isError);
            if (!errorOutput) {
                return;
            }
            const traceback = anser__WEBPACK_IMPORTED_MODULE_4___default().ansiToText(errorOutput.traceback.join('\n'));
            await this.modify(this.truncateMiddle(`Please edit the code to fix the following error:\n${traceback}`, INPUT_CHARACTER_MAX), cancelToken);
        }
        truncateEnd(input, limit) {
            return input.substring(0, limit);
        }
        truncateMiddle(input, limit) {
            const len = input.length;
            if (len <= limit) {
                return input;
            }
            const constructTruncated = (front, back) => `${front}...${back}`;
            const combinedSampleSize = Math.max(0, limit - constructTruncated('', '').length);
            const backSampleSize = Math.min(Math.floor(combinedSampleSize / 2), combinedSampleSize);
            const frontSampleSize = combinedSampleSize - backSampleSize;
            const frontSample = input.substring(0, frontSampleSize);
            const backSample = input.substring(frontSampleSize, frontSampleSize + backSampleSize);
            return constructTruncated(frontSample, backSample);
        }
        replaceCellContent(newContent) {
            var _a;
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
            (_a = cellEditor.replaceSelection) === null || _a === void 0 ? void 0 : _a.call(cellEditor, newContent);
        }
    }
    PromptModel.Model = Model;
})(PromptModel || (PromptModel = {}));
function canGetCellContext(cell, notebook) {
    if (!cell || !cell.model || !(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.isCodeCellModel)(cell.model)) {
        return false;
    }
    if (!notebook || !notebook.model) {
        return false;
    }
    return true;
}
function canExecuteFixCell(cell, notebook) {
    if (!canGetCellContext(cell, notebook)) {
        return false;
    }
    const cellModel = cell === null || cell === void 0 ? void 0 : cell.model;
    if (!cell || !cellModel || !(0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.isCodeCellModel)(cellModel)) {
        return false;
    }
    if (!cellModel.outputs.toJSON().some(_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_1__.isError)) {
        return false;
    }
    return true;
}


/***/ }),

/***/ "./lib/prompt.js":
/*!***********************!*\
  !*** ./lib/prompt.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Prompt: () => (/* binding */ Prompt)
/* harmony export */ });
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @blueprintjs/core */ "webpack/sharing/consume/default/@blueprintjs/core/@blueprintjs/core?f973");
/* harmony import */ var _blueprintjs_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _blueprintjs_select__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @blueprintjs/select */ "webpack/sharing/consume/default/@blueprintjs/select/@blueprintjs/select");
/* harmony import */ var _blueprintjs_select__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_blueprintjs_select__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./model */ "./lib/model.js");









const PROMPT_TYPE_ITEM_MAP = {
    [_model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.GENERATE_CELL]: {
        value: _model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.GENERATE_CELL,
        text: 'Generate'
    },
    [_model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.MODIFY_CELL]: {
        value: _model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.MODIFY_CELL,
        text: 'Modify'
    },
    [_model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.FIX_CELL]: {
        value: _model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.FIX_CELL,
        text: 'Fix'
    }
};
const PROMPT_TYPE_ITEMS = Object.values(PROMPT_TYPE_ITEM_MAP);
const PromptComponent = (props) => {
    const isFixPrompt = props.type === _model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.FIX_CELL;
    const componentRef = react__WEBPACK_IMPORTED_MODULE_4___default().useRef(null);
    const textAreaRef = react__WEBPACK_IMPORTED_MODULE_4___default().useRef(null);
    const submitButtonRef = react__WEBPACK_IMPORTED_MODULE_4___default().useRef(null);
    const [isActive, setIsActive] = react__WEBPACK_IMPORTED_MODULE_4___default().useState(false);
    const getShouldBeActive = react__WEBPACK_IMPORTED_MODULE_4___default().useCallback(() => Boolean(document.activeElement instanceof HTMLElement &&
        componentRef.current &&
        componentRef.current.contains(document.activeElement)), []);
    const updateActiveState = react__WEBPACK_IMPORTED_MODULE_4___default().useCallback(() => {
        setIsActive(getShouldBeActive());
    }, [getShouldBeActive]);
    react__WEBPACK_IMPORTED_MODULE_4___default().useEffect(() => {
        var _a;
        const ref = props.type === _model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.FIX_CELL
            ? submitButtonRef
            : textAreaRef;
        (_a = ref.current) === null || _a === void 0 ? void 0 : _a.focus();
        setIsActive(Boolean(ref.current && ref.current === document.activeElement));
    }, []);
    const maybeSyncHeightToScrollHeight = react__WEBPACK_IMPORTED_MODULE_4___default().useCallback(() => {
        if (textAreaRef.current && textAreaRef.current.scrollHeight > 0) {
            const scrollHeight = textAreaRef.current.scrollHeight;
            textAreaRef.current.style.height = '0px';
            const newHeight = textAreaRef.current.scrollHeight > 0
                ? textAreaRef.current.scrollHeight
                : scrollHeight;
            textAreaRef.current.style.height = `${newHeight}px`;
        }
    }, []);
    react__WEBPACK_IMPORTED_MODULE_4___default().useEffect(() => {
        maybeSyncHeightToScrollHeight();
    }, [maybeSyncHeightToScrollHeight]);
    const getIsUserInputValid = react__WEBPACK_IMPORTED_MODULE_4___default().useCallback((value) => {
        return (props.type === _model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.FIX_CELL ||
            value.trim().length > 0);
    }, [props.type]);
    const [isUserInputValid, setIsUserInputValid] = react__WEBPACK_IMPORTED_MODULE_4___default().useState(getIsUserInputValid(props.userInput));
    const [value, setValue] = react__WEBPACK_IMPORTED_MODULE_4___default().useState(props.userInput);
    react__WEBPACK_IMPORTED_MODULE_4___default().useEffect(() => {
        setValue(props.userInput);
    }, [props.userInput]);
    const onPromptChange = react__WEBPACK_IMPORTED_MODULE_4___default().useCallback((evt) => {
        maybeSyncHeightToScrollHeight();
        setValue(evt.target.value);
        props.onUserInputChange(evt.target.value);
        setIsUserInputValid(getIsUserInputValid(evt.target.value));
    }, [props.onUserInputChange, maybeSyncHeightToScrollHeight]);
    const renderPromptTypeItem = react__WEBPACK_IMPORTED_MODULE_4___default().useCallback((promptTypeItem, { handleClick, handleFocus, modifiers, query }) => {
        if (!modifiers.matchesPredicate) {
            return null;
        }
        return (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.MenuItem, { active: modifiers.active, disabled: modifiers.disabled, key: promptTypeItem.value, onClick: handleClick, onFocus: handleFocus, roleStructure: "listoption", text: props.trans.__(promptTypeItem.text) }));
    }, [props.trans]);
    react__WEBPACK_IMPORTED_MODULE_4___default().useEffect(() => {
        const handleEscape = (evt) => {
            var _a;
            if (evt.keyCode === 27 &&
                document.activeElement instanceof HTMLElement &&
                getShouldBeActive()) {
                evt.preventDefault();
                evt.stopPropagation();
                document.activeElement.blur();
                (_a = props.onEscape) === null || _a === void 0 ? void 0 : _a.call(props);
            }
        };
        document.addEventListener('keydown', handleEscape, { capture: true });
        return () => {
            document.removeEventListener('keydown', handleEscape, { capture: true });
        };
    }, [getShouldBeActive]);
    return (react__WEBPACK_IMPORTED_MODULE_4___default().createElement("div", { className: `c-prompt${isActive ? ' c-prompt--is-active' : ''}`, ref: componentRef },
        react__WEBPACK_IMPORTED_MODULE_4___default().createElement("div", { className: "c-prompt__type-select-container" },
            react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_blueprintjs_select__WEBPACK_IMPORTED_MODULE_1__.Select, { filterable: false, items: PROMPT_TYPE_ITEMS, itemRenderer: renderPromptTypeItem, popoverProps: {
                    minimal: true
                }, menuProps: {
                    className: 'c-prompt__type-select-listbox'
                }, popoverTargetProps: {
                    className: 'c-prompt__type-select-popover-target'
                }, onItemSelect: promptTypeItem => {
                    props.onPromptTypeChange(promptTypeItem.value);
                } },
                react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { className: "c-prompt__type-select-button", text: props.trans.__(PROMPT_TYPE_ITEM_MAP[props.type].text), rightIcon: react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.caretDownEmptyIcon.react, null), placeholder: props.trans.__('Select an action') }))),
        react__WEBPACK_IMPORTED_MODULE_4___default().createElement("div", { className: "c-prompt__logo-container" },
            react__WEBPACK_IMPORTED_MODULE_4___default().createElement("div", { className: "c-prompt__logo" }, props.isProcessing ? (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Spinner, { size: 20 })) : (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_6__.einblickIcon.react, { height: "20px", width: "20px" })))),
        !isFixPrompt && (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.TextArea, { value: value, className: "c-prompt__input-textarea", inputRef: textAreaRef, placeholder: props.placeholder, fill: true, disabled: props.isProcessing, onKeyDownCapture: evt => {
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
            }, onFocus: () => updateActiveState(), onBlur: () => updateActiveState(), onChange: onPromptChange })),
        isFixPrompt && (react__WEBPACK_IMPORTED_MODULE_4___default().createElement("div", { className: "c-prompt__message" }, "Fix any errors in the cell.")),
        react__WEBPACK_IMPORTED_MODULE_4___default().createElement("div", { className: "c-prompt__button-container" },
            react__WEBPACK_IMPORTED_MODULE_4___default().createElement("div", { className: "c-prompt__buttons" },
                !props.isProcessing && (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { minimal: true, ref: submitButtonRef, className: "c-prompt__submit-button", disabled: props.isProcessing || !isUserInputValid, onClick: props.onSubmit, icon: react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Icon, { icon: "send-message", size: 12 }), onFocus: () => updateActiveState(), onBlur: () => updateActiveState() })),
                props.isProcessing && (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { minimal: true, className: "c-prompt__cancel-button", disabled: !props.isProcessing, onClick: props.onCancel, icon: react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.stopIcon.react, null), onFocus: () => updateActiveState(), onBlur: () => updateActiveState() })),
                react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_blueprintjs_core__WEBPACK_IMPORTED_MODULE_0__.Button, { minimal: true, className: "c-prompt__close-button", onClick: props.onClose, icon: react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.closeIcon.react, null), onFocus: () => updateActiveState(), onBlur: () => updateActiveState() })))));
};
/**
 * A VDomRenderer widget for displaying the prompt.
 */
class Prompt extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.VDomRenderer {
    /**
     * Construct the prompt widget.
     */
    constructor(opts) {
        super(new _model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.Model(opts.type, opts.cell, opts.notebook, opts.fileBrowser, opts.translator, opts.metadata));
        const translator = opts.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this.commands = opts.commands;
        this.translator = translator;
        this.trans = this.translator.load('jupyterlab');
    }
    /**
     * Render the prompt component.
     */
    render() {
        if (this.model === null) {
            return null;
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(PromptComponent, { type: this.model.type, placeholder: this.model.placeholder, isProcessing: this.model.isProcessing, trans: this.trans, userInput: this.model.userInput, onUserInputChange: value => {
                    this.model.userInput = value;
                }, onPromptTypeChange: type => this.changePromptType(type), onSubmit: () => this.model.execute(), onCancel: () => this.cancel(), onClose: () => this.dispose(), onEscape: () => {
                    this.model.notebook.activate();
                } }));
        }
    }
    focus() {
        var _a, _b;
        if (this.model.isProcessing && this.cancelButtonElement) {
            this.cancelButtonElement.focus();
            return;
        }
        if (this.model.type === _model__WEBPACK_IMPORTED_MODULE_5__.PromptModel.PromptType.FIX_CELL) {
            (_a = this.submitButtonElement) === null || _a === void 0 ? void 0 : _a.focus();
        }
        else {
            (_b = this.textAreaElement) === null || _b === void 0 ? void 0 : _b.focus();
        }
    }
    get isFocused() {
        var _a;
        return Boolean(document.activeElement instanceof HTMLElement &&
            ((_a = this.element) === null || _a === void 0 ? void 0 : _a.contains(document.activeElement)));
    }
    cancel() {
        this.model.cancel();
    }
    dispose() {
        var _a;
        (_a = this.model) === null || _a === void 0 ? void 0 : _a.cancel();
        super.dispose();
    }
    get element() {
        const element = this.node.getElementsByClassName('c-prompt')[0];
        if (element instanceof HTMLElement) {
            return element;
        }
        return null;
    }
    get textAreaElement() {
        const textAreaElement = this.node.getElementsByClassName('c-prompt__input-textarea')[0];
        if (textAreaElement instanceof HTMLTextAreaElement) {
            return textAreaElement;
        }
        return null;
    }
    get submitButtonElement() {
        const submitButtonElement = this.node.getElementsByClassName('c-prompt__submit-button')[0];
        if (submitButtonElement instanceof HTMLButtonElement) {
            return submitButtonElement;
        }
        return null;
    }
    get closeButtonElement() {
        const closeButtonElement = this.node.getElementsByClassName('c-prompt__close-button')[0];
        if (closeButtonElement instanceof HTMLButtonElement) {
            return closeButtonElement;
        }
        return null;
    }
    get cancelButtonElement() {
        const cancelButtonElement = this.node.getElementsByClassName('c-prompt__cancel-button')[0];
        if (cancelButtonElement instanceof HTMLButtonElement) {
            return cancelButtonElement;
        }
        return null;
    }
    changePromptType(type) {
        (0,_commands__WEBPACK_IMPORTED_MODULE_7__.executePromptCommand)(type, this.model.cell, this.model.notebook, this.commands);
    }
}


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PromptContextUtil: () => (/* binding */ PromptContextUtil),
/* harmony export */   apiHostName: () => (/* binding */ apiHostName),
/* harmony export */   appHostName: () => (/* binding */ appHostName),
/* harmony export */   getDependencies: () => (/* binding */ getDependencies)
/* harmony export */ });
/* harmony import */ var web_tree_sitter__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! web-tree-sitter */ "webpack/sharing/consume/default/web-tree-sitter/web-tree-sitter");
/* harmony import */ var web_tree_sitter__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(web_tree_sitter__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _cancellablePromise__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./cancellablePromise */ "./lib/cancellablePromise.js");


const CONTEXT_MAX_FILES = 100;
const apiHostName = 'https://api.einblick.ai';
const appHostName = 'https://app.einblick.ai';
const executeCode = (kernel, code, ...cancelTokens) => {
    const future = kernel.requestExecute({ code });
    return (0,_cancellablePromise__WEBPACK_IMPORTED_MODULE_1__.CancellablePromise)(resolve => {
        future.onIOPub = message => {
            if (message.header.msg_type === 'stream') {
                const streamMessage = message;
                if (streamMessage.content.name === 'stdout') {
                    resolve(streamMessage.content.text);
                }
            }
        };
    }, ...cancelTokens);
};
const getVariablesInKernel = async (kernel, ...cancelTokens) => {
    const output = await executeCode(kernel, 'import json\nprint(json.dumps(list(map(lambda a: [a[0], str(type(a[1]))], [*(globals().items())]))))', ...cancelTokens);
    if (!output) {
        return {};
    }
    const entries = JSON.parse(output);
    return Object.fromEntries(entries);
};
const getDataframeVariablesInKernel = async (kernel, ...cancelTokens) => {
    const output = await executeCode(kernel, [
        '!pip install --quiet --disable-pip-version-check pandas',
        'import pandas as pd',
        'import json',
        'import re',
        "global_variables = [k for k in globals() if not re.match('^_+[0-9]*$', k)]",
        'dfs = [v for v in global_variables if isinstance(globals()[v], pd.DataFrame)]',
        'print(json.dumps(dfs))'
    ].join('\n'), ...cancelTokens);
    if (!output) {
        return [];
    }
    const entries = JSON.parse(output);
    return entries !== null && entries !== void 0 ? entries : [];
};
const getContextForDataframe = async (kernel, dataframeName, numRows = 3, ...cancelTokens) => {
    const output = await executeCode(kernel, `if '${dataframeName}' in globals():
   print(${dataframeName}.head(${numRows}).to_json(orient="split"))`, ...cancelTokens);
    if (!output) {
        return null;
    }
    const kernelDataframeContext = JSON.parse(output);
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
const GLOBAL_IDENTIFIERS = new Set([
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
/**
 * Analyzes the tree and returns the variables used and assigned in the script
 *
 * @see https://github.com/tree-sitter/tree-sitter-python/blob/master/src/node-types.json
 * This is a list of all the node types that can be returned by the parser, as well as the fields that each node type has.
 */
function analyzeTree(node, settings, isAssigning = false) {
    const variablesUsed = new Set();
    const variablesAssigned = new Set();
    if (!node || !node.isNamed) {
        return {
            variablesUsed,
            variablesAssigned
        };
    }
    function addResult(result, ignoreIfAssigned = true) {
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
                let sibling = importedItem === null || importedItem === void 0 ? void 0 : importedItem.nextNamedSibling;
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
                forInResult.variablesAssigned.forEach(variable => bodyResult.variablesUsed.delete(variable));
                addResult({
                    variablesUsed: new Set([
                        ...bodyResult.variablesUsed,
                        ...forInResult.variablesUsed
                    ]),
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
            leftResult.variablesAssigned.forEach(variable => bodyResult.variablesUsed.delete(variable));
            addResult({
                variablesUsed: new Set([
                    ...bodyResult.variablesUsed,
                    ...rightResult.variablesUsed
                ]),
                variablesAssigned: bodyResult.variablesAssigned // ignore variables assigned in the for loop
            });
            break;
        }
        case 'identifier':
            if (isAssigning) {
                variablesAssigned.add(node.text);
            }
            else {
                variablesUsed.add(node.text);
            }
            break;
        case 'function_definition':
            // Function name is a assigned dependency
            addResult(analyzeTree(node.childForFieldName('name'), settings, true));
            break;
        default: {
            node.namedChildren.forEach((child) => {
                addResult(analyzeTree(child, settings, isAssigning));
            });
        }
    }
    return {
        variablesUsed,
        variablesAssigned
    };
}
function getDependencies(tree) {
    const result = analyzeTree(tree.rootNode, { ignoreImports: true });
    const filteredAssignments = new Set();
    result.variablesAssigned.forEach(variable => {
        if (!GLOBAL_IDENTIFIERS.has(variable)) {
            filteredAssignments.add(variable);
        }
    });
    const filteredVariablesUsed = new Set();
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
let pythonParser = null;
let language = null;
const loadPythonParser = async (...cancelTokens) => {
    var _a;
    if (pythonParser && language) {
        return pythonParser;
    }
    try {
        await (0,_cancellablePromise__WEBPACK_IMPORTED_MODULE_1__.CancellablePromiseRace)([
            web_tree_sitter__WEBPACK_IMPORTED_MODULE_0___default().init({
                locateFile: (fileName) => {
                    return `${appHostName}/assets/tree-sitter-v0.20.8/${fileName}`;
                }
            })
        ], ...cancelTokens);
        if (cancelTokens.some(token => token.IsCancelled)) {
            return undefined;
        }
        pythonParser = new (web_tree_sitter__WEBPACK_IMPORTED_MODULE_0___default())();
        const languageWasmFileResponse = await (0,_cancellablePromise__WEBPACK_IMPORTED_MODULE_1__.CancellablePromiseRace)([
            fetch(`${appHostName}/assets/tree-sitter-v0.20.8/tree-sitter-python.wasm`)
        ], ...cancelTokens);
        if (cancelTokens.some(token => token.IsCancelled)) {
            return undefined;
        }
        if (!languageWasmFileResponse || !languageWasmFileResponse.ok) {
            console.error('Unable to load language file!');
            throw Error('Unable to load language file!');
        }
        const arrayBuffer = await (0,_cancellablePromise__WEBPACK_IMPORTED_MODULE_1__.CancellablePromiseRace)([languageWasmFileResponse.arrayBuffer()], ...cancelTokens);
        if (cancelTokens.some(token => token.IsCancelled)) {
            return undefined;
        }
        else if (!arrayBuffer) {
            throw Error('Unable to load language file!');
        }
        const languageFileBinary = new Uint8Array(arrayBuffer);
        language =
            (_a = (await (0,_cancellablePromise__WEBPACK_IMPORTED_MODULE_1__.CancellablePromiseRace)([web_tree_sitter__WEBPACK_IMPORTED_MODULE_0___default().Language.load(languageFileBinary)], ...cancelTokens))) !== null && _a !== void 0 ? _a : null;
        if (cancelTokens.some(token => token.IsCancelled)) {
            return undefined;
        }
        else if (!language) {
            throw Error('Unable to load language file!');
        }
        pythonParser.setLanguage(language);
        return pythonParser;
    }
    catch (error) {
        console.error(`Failed to load python parser\n${error}`);
        throw error;
    }
};
class PromptContextUtil {
    static async GetContextForActiveNotebookCellBasedOnRadius(activeCell, notebookPanel, browser = null, radius = 1000, ...cancelTokens) {
        var _a, _b;
        const context = {
            dfs: [],
            vars: [],
            code: [],
            dataConnectors: [],
            tableInfo: null,
            filenames: []
        };
        const nearbyCellParitalContexts = [];
        const notebookCells = notebookPanel.content.widgets;
        const activeCellIndex = notebookCells.indexOf(activeCell);
        const kernel = (_a = notebookPanel.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (activeCellIndex < 0 || activeCell.model.type !== 'code' || !kernel) {
            return context;
        }
        // Get client rects for all cells in the notebook
        const cellBoundingClientRects = notebookCells.map(cell => cell.node.getBoundingClientRect());
        const activeCellRect = cellBoundingClientRects[activeCellIndex];
        // Adding cells based on radius
        let cellIndex = 0;
        for (const cell of notebookCells) {
            const notebookCellRect = cellBoundingClientRects[cellIndex];
            let distance = Number.POSITIVE_INFINITY;
            if (cellIndex < activeCellIndex) {
                distance = activeCellRect.top - notebookCellRect.bottom;
            }
            else if (cellIndex > activeCellIndex) {
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
        }
        else if (!pythonParser) {
            throw Error('Unable to get python parser when loading context');
        }
        const variablesInKernel = await getVariablesInKernel(kernel, ...cancelTokens);
        if (cancelTokens.some(token => token.IsCancelled)) {
            return context;
        }
        const dataframeVariablesInKernel = await getDataframeVariablesInKernel(kernel, ...cancelTokens);
        if (cancelTokens.some(token => token.IsCancelled)) {
            return context;
        }
        for (const nearbyCellPartialContext of nearbyCellParitalContexts) {
            if (nearbyCellPartialContext.cell.model.type !== 'code') {
                continue;
            }
            const codeCell = nearbyCellPartialContext.cell;
            const codeCellSource = codeCell.model.toJSON().source;
            const codeCellContent = Array.isArray(codeCellSource)
                ? codeCellSource.join('\n')
                : codeCellSource;
            const codeCellDependenciesResult = getDependencies(pythonParser.parse(codeCellContent));
            const usedCodeCellVariables = Array.from(codeCellDependenciesResult.variablesUsed.values());
            const assignedCodeCellVariables = Array.from(codeCellDependenciesResult.variablesAssigned.values());
            const combined = [...usedCodeCellVariables, ...assignedCodeCellVariables];
            for (const usedCodeCellVariable of combined) {
                if (dataframeVariablesInKernel.includes(usedCodeCellVariable)) {
                    const dfContext = await getContextForDataframe(kernel, usedCodeCellVariable, 3, ...cancelTokens);
                    if (cancelTokens.some(token => token.IsCancelled)) {
                        return context;
                    }
                    else if (dfContext) {
                        context.dfs.push(dfContext);
                    }
                }
                else {
                    context.vars.push({
                        distance: nearbyCellPartialContext.distance,
                        lastAccessed: nearbyCellPartialContext.lastAccessed,
                        linkDistance: nearbyCellPartialContext.linkDistance,
                        above: nearbyCellPartialContext.above,
                        name: usedCodeCellVariable,
                        type: (_b = variablesInKernel[usedCodeCellVariable]) !== null && _b !== void 0 ? _b : ''
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
            const dataFiles = Array.from(browser.model.items()).filter(item => item.type === 'file' &&
                (item.path.endsWith('.csv') || item.path.endsWith('.tsv')));
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


/***/ }),

/***/ "./static/icons/connected.svg":
/*!************************************!*\
  !*** ./static/icons/connected.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" viewBox=\"0 0 24 24\">\n    <path class=\"jp-icon3\" fill=\"#616161\" d=\"M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z\"/>\n</svg>";

/***/ }),

/***/ "./static/icons/einblick.svg":
/*!***********************************!*\
  !*** ./static/icons/einblick.svg ***!
  \***********************************/
/***/ ((module) => {

module.exports = "<svg\n    id=\"Layer_2\"\n    xmlns=\"http://www.w3.org/2000/svg\"\n    viewBox=\"0 0 413.05 412.58\"\n>\n    <g id=\"Layer_1-2\">\n    <g>\n        <g>\n        <polygon\n            fill=\"#081b24\"\n            points=\"413.05 0 413.05 390.7 332.53 310.52 332.53 79.82 79.82 79.82 79.82 311.34 0 390.7 0 0 413.05 0\"\n        />\n        <polygon\n            fill=\"#081b24\"\n            points=\"311.69 332.64 391.98 412.58 21.3 412.58 101.71 332.64 311.69 332.64\"\n        />\n        </g>\n        <g>\n        <polygon\n            fill=\"#21bd75\"\n            points=\"413.05 0 413.05 390.7 332.53 310.52 332.53 79.82 79.82 79.82 79.82 311.34 0 390.7 0 0 413.05 0\"\n        />\n        <polygon\n            fill=\"#081b24\"\n            points=\"311.69 332.64 391.98 412.58 21.3 412.58 101.71 332.64 311.69 332.64\"\n        />\n        </g>\n    </g>\n    </g>\n</svg>";

/***/ }),

/***/ "./static/icons/notConnected.svg":
/*!***************************************!*\
  !*** ./static/icons/notConnected.svg ***!
  \***************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"14\" height=\"14\" viewBox=\"0 0 24 24\">\n    <rect class=\"jp-icon3\" fill=\"#fff\" height=\"18\" width=\"2\" x=\"11\" y=\"3\" transform=\"rotate(315, 12, 12)\"/>\n    <rect class=\"jp-icon3\" fill=\"#fff\" height=\"18\" width=\"2\" x=\"11\" y=\"3\" transform=\"rotate(45, 12, 12)\"/>\n</svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.311f74433a822e47b4a7.js.map