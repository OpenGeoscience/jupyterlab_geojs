# JupyterLab GeoJS Renderer

[GeoJS](https://github.com/opengeoscience/geojs) rendering extension to [JupyterLab](https://github.com/jupyterlab/jupyterlab) for visualization of GeoJSON data formats.

## Install

* geojson-extension: `jupyter labextension install @jupyterlab/geojson-extension`


### Developer install

```
git clone https://github.com/gnestor/jupyter-renderers.git
cd jupyter-renderers
npm install
npm run build
```

### Link extensions with JupyterLab

Link geojson-extension:

```
jupyter labextension link packages/geojson-extension
```

### Rebuilding extensions

After making changes to the source of the extension or renderer packages, the packages must be rebuilt:

```
# Rebuild the source
npm run build

# Rebuild the JupyterLab staging directory
jupyter lab build
```
