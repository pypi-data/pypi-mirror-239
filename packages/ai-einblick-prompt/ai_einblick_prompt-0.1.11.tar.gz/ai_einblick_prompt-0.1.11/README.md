# ai-einblick-prompt

`ai-einblick-prompt` empowers JupyterLab users with a domain-specific AI agent that can generate, modify, and fix code for data science workflows. Einblick's extension is the easiest and only context-aware way to augment the data workflow with generative AI.

## [Einblick Prompt AI](https://www.einblick.ai/ai-einblick-prompt/)

Einblick is the AI-native data notebook that can write and fix code, create beautiful charts, build models, and much more. This is made possible via our domain-specific AI agent, Einblick Prompt. Visit our [homepage](https://www.einblick.ai/) to learn more about Einblick.

## Usage

[Watch a quick video tutorial.](https://cdn.sanity.io/files/1xvnv7n3/production/3af4d02af053694730f15c9be93234470dfa4e4e.mp4)

### Quick Start

1. Start JupyterLab and install `ai-einblick-prompt` via the Extension Manager in the left panel.
2. Read in a dataset.
3. Click the Einblick logo icon in the top-right side of any Python cell, and select “Generate.”
4. Ask Einblick Prompt AI to write code.

### Example Prompts

1. “Create a box plot of col_3.”
2. “Filter for cat_1, cat_2, and cat_3.”
3. “Create a scatter plot of col_1 vs. col_2, color by col_4.”

### Keyboard shortcut

`Command (⌘) + K` / `Ctrl + K` - Toggle prompt widget on active cell.

### Commands

The following commands are executable from the Jupyterlab command palette (`Command (⌘) + Shift + C` / `Ctrl + Shift + C`)

- **Einblick AI: Prompt**: Toggle prompt widget on active cell.
- **Einblcik AI: Generate**: Toggle "Generate" prompt on active cell to create new code for the cell.
- **Einblcik AI: Generate**: Toggle "Fix" prompt on active cell to fix errors in the cell.
- **Einblcik AI: Generate**: Toggle "Modify" prompt on active cell to change existing code in the cell.

## Installation Steps

### Requirements

- JupyterLab >= 4.0.0

### Install

**Method 1** Search `ai-einblick-prompt` in JupyterLab's Extension Manager, and click Install

**Method 2** Execute:

```bash
pip install ai-einblick-prompt
```

### Uninstall

To remove the extension, execute:

```bash
pip uninstall ai-einblick-prompt
```
