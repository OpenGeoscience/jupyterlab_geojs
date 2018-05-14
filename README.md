# jupyterlab_geojs

A JupyterLab and Jupyter Notebook extension for rendering GeoJS

![output renderer](http://g.recordit.co/QAsC7YULcY.gif)

## Prerequisites

* JupyterLab ^0.28.0 and/or Notebook >=4.3.0

## Usage

To render GeoJS output in IPython:

```python
from jupyterlab_geojs import GeoJS

GeoJS({
    "string": "string",
    "array": [1, 2, 3],
    "bool": True,
    "object": {
        "foo": "bar"
    }
})
```To render a `.geojson` file as a tree, simply open it:

![file renderer](http://g.recordit.co/cbf0xnQHKn.gif)


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
