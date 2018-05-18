/*
 * Class for generating geomap based on geojs model received from Jupyter kernel.
 */


import geo from 'geojs';

class GeoJSBuilder {
  constructor() {
      this._geoMap = null;
  }

  // Returns geo.map instance
  // Note that caller is responsible for disposing geomap
  generate(node, model={}) {
    if (!!this._geoMap) {
      console.warn('Deleting existing GeoJS instance');
      this._geoMap.exit();  // safety first
    }

    let options = model.options || {};
    // Add dom node to the map options
    const mapOptions = Object.assign(options, {node: node});
    this._geoMap = geo.map(mapOptions);
    this.update(model);
    return this._geoMap;
  }  // generate()


  // Generates geomap layers
  update(model) {
    let layerModels = model.layers || [];
    for (let layerModel of layerModels) {
      switch(layerModel.layerType) {
        case 'feature':
          this._createLayer(layerModel);
          console.log('Feature layer todo');
        break;

        case 'osm':
          this._createLayer(layerModel);
        break;

        default:
          console.error(`Unrecognized layer type ${layerModel.layerType}`)
      }  // switch (layerType)
    }
  }  // update()


  // Creates layer
  _createLayer(layerModel) {
    let options = layerModel.options || {};
    let layer = this._geoMap.createLayer(layerModel.layerType, options);
    return layer;
  }  // _createLayer()

}  // GeoJSBuilder

export { GeoJSBuilder }
