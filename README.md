# jupyterlab_geojs

A JupyterLab and Jupyter Notebook extension for rendering geospatial
data using the GeoJS front end library

![Example Screenshot](./docs/BasicScreenshot.png)

## Prerequisites

* JupyterLab ^0.28.0 and/or Notebook >=4.3.0

## Usage

To render GeoJS output in IPython:

```python
from jupyterlab_geojs import GeoJSMap
geomap = GeoJSMap()
geomap.createLayer('osm')
geomap

```

The notebooks folder contains examples.


## Install

```bash
pip install jupyterlab_geojs
# For JupyterLab
jupyter lab build
# For Notebook
jupyter nbextension enable --py --sys-prefix jupyterlab_geojs
```

## Development

```bash
# Install dependencies
jlpm
# Build Typescript source
jlpm build
# Link your development version of the extension with JupyterLab
jupyter labextension link .
# Rebuild Typescript source after making changes
jlpm build
# Rebuild JupyterLab after making any changes
jupyter lab build
```
