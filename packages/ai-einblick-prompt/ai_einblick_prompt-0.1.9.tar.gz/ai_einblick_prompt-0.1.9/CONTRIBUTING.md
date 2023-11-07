# Contributing

## Development install

### Install conda using miniconda

Open a new terminal and run the following code to install miniconda:

```bash
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

Next run this to initialize miniconda for zsh:

```bash
~/miniconda3/bin/conda init zsh
```

Restart the terminal, then run the following to ensure that you have properly installed conda:

```bash
conda
```

If you have trouble, you may want to look at the [miniconda installation page](https://docs.conda.io/projects/miniconda/en/latest/index.html#quick-command-line-install)

### Create a new conda environment for working on the jupyterlab extension

This only needs to be done once as a setup step. We're going to create a conda environment called `jupyter-ext` in which we can do dev work on the extension.

```bash
conda create -n jupyterlab-ext --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=4 nodejs=18 git copier=7 jinja2-time
```

### Activate the conda environment

In the terminal where you will be working on the jupyterlab extension (perhaps in the VS code terminal for example), you will need to activate the conda environment. Once you do this, all the packages we install will be set up for this environment we created. This should help prevent conflicts with existing version/installations you are using elsewhere on your machine.

```bash
conda activate jupyterlab-ext
```

### Install **jupyterlab**

Easiest to install using `pip`. Once again, make sure you're running this in a terminal where you activated the `jupyerlab-ext` environment.

```bash
pip install jupyterlab
```

### Start up jupterlab

Open a new terminal to start up jupyterlab locally in the new conda environment.

Note that it's important to activate the same conda environment again here. That way, it uses the version/instance of jupyterlab that we just installed.

```bash
conda activate jupyterlab-ext
jupyter lab
```

### Build and install the extension for development

Switch back to the terminal where you will be developing the extension - it should be in the root directory of this project, and the same terminal in which you activated the `jupyter-ext` conda environment earlier.

Run this to download the project's dependencies:

```bash
jlpm
```

Note: The `jlpm` command is JupyterLab's pinned version of [yarn](https://yarnpkg.com/) that is installed with JupyterLab.

Now we can use these commands to create a connection between this terminal (in which we're building the extension) and the instance of JupyterLab running in the other terminal.

```bash
pip install -ve .
jupyter labextension develop --overwrite .
```

Now to build the extension, you have two options. The following will build it once:

```bash
jlpm run build
```

Or you can run the following to rebuild when changes are detected:

```bash
jlpm run watch
```

Note that either way, you will need to refresh the page in JupyterLab after new changes are rebuilt.

#### Check that the extension is linked to your local jupyterlab instance

Navigate to JupyterLab in your browser, open the dev console, and refresh the page. You should see the following logs:

```
Einblick AI Prompt extension is activated!
```

## Packaging the extension

See [RELEASE](RELEASE.md)
