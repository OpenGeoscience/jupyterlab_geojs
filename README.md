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

[comment]: <> (To render a `.geojson` file simply open it:)
[comment]: <> ([File Renderer](http://g.recordit.co/cbf0xnQHKn.gif))


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
pip install -e .
# For JupyterLab
jupyter labextension link
jupyter lab --watch
# For Notebook
jupyter nbextension install --symlink --py --sys-prefix jupyterlab_geojs
jupyter nbextension enable --py --sys-prefix jupyterlab_geojs
```
