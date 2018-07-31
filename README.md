# jupyterlab_geojs

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/OpenGeoscience/jupyterlab_geojs/master)

A JupyterLab notebook extension for rendering geospatial
data using the GeoJS front end library

![Example Screenshot](./docs/BasicScreenshot.png)

## Prerequisites

* JupyterLab ^0.32.1 and Notebook >=5.5.0

## Usage

To render GeoJS output in JupyterLab:

```python
from jupyterlab_geojs import Scene
scene = Scene()
scene.create_layer('osm')
scene

```

The notebooks folder contains examples.


## Install

```bash
# Install this lab extension
jupyter labextension install @johnkit/jupyterlab_geojs

# Also need to install the widget-manager extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager

# Install the python package
pip install jupyterlab_geojs

```

## Development

```bash
# Install python package
pip install -e .

# Install widget-manager extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager


# Install js dependencies
npm install
# Build Typescript source
jlpm build
# Link your development version of the extension with JupyterLab
jupyter labextension link .
# Run
jupyter lab


# Rebuild Typescript source after making changes
jlpm build
# Rebuild JupyterLab after making any changes
jupyter lab build
```

For testing, see README.md in test/ folder.
