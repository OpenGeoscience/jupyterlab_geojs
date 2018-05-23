/*
 * Class for generating geomap based on geojs model received from Jupyter kernel.
 */


import geo from 'geojs';
console.debug(`Using geojs ${geo.version}`);

class GeoJSBuilder {
  constructor() {
    this._geoMap = null;
    this._promiseList = null;  // for loading data
  }

  // Clears the current geo.map instance
  clear() {
    if (!!this._geoMap) {
      this._geoMap.exit();
      this._geoMap = null;
    }
  }

  // Returns PROMISE that resolves to geo.map instance
  // Note that caller is responsible for disposing the geo.map
  generate(node, model={}) {
    if (!!this._geoMap) {
      console.warn('Deleting existing GeoJS instance');
      this.clear()
    }

    let options = model.options || {};
    // Add dom node to the map options
    const mapOptions = Object.assign(options, {node: node});
    this._geoMap = geo.map(mapOptions);
    this.update(model);

    // Return promise that resolves to this._geoMap
    return new Promise((resolve, reject) => {
      Promise.all(this._promiseList)
        .then(() => resolve(this._geoMap), reject => console.error(reject))
        .catch(error => reject(error));
    });
  }  // generate()

  // Generates geomap layers
  // Note: Internal logic can push promise instances onto this._promiseList
  update(model) {
    this._promiseList = [];
    let layerModels = model.layers || [];
    for (let layerModel of layerModels) {
      let options = layerModel.options || {};
      let layerType = layerModel.layerType;
      //console.log(`layerType: ${layerType}`);
      let layer = this._geoMap.createLayer(layerType, options);
      //console.log(`Renderer is ${layer.rendererName()}`)
      if (layerModel.features) {
        this._createFeatures(layer, layerModel.features)
      }
    }  // for (layerModel)
  }  // update()


  // Creates features
  _createFeatures(layer, featureModels) {
    for (let featureModel of featureModels) {
      switch(featureModel.featureType) {
        case 'geojson':
          this._createGeoJSONFeature(layer, featureModel);
        break;

        default:
          console.error(`Unrecognized feature type ${featureModel.featureType}`);
        break;
      }  // switch
    }
  }  // _createFeatures()

  // Generates GeoJSON feature from feature model
  _createGeoJSONFeature(layer, featureModel) {
    if (featureModel.data) {
      let p = this._loadGeoJSONObject(layer, featureModel.data);
      this._promiseList.push(p);
    }
    if (featureModel.url) {
      let p = this._downloadGeoJSONFile(layer, featureModel.url);
      this._promiseList.push(p);
    }
  }

  // Loads GeoJSON object
  _loadGeoJSONObject(layer, data) {
    // console.dir(layer);
    // console.dir(data);

    let reader = geo.createFileReader('jsonReader', {layer: layer});
    return new Promise((resolve, reject) => {
      try {
        reader.read(data, resolve);
      }
      catch (error) {
        console.error(error);
        reject(error);
      }
    })  // new Promise()
  }  // loadGeoJSONData()

  _downloadGeoJSONFile(layer, url) {
    //console.log(`_downloadGeoJSONFile: ${url}`);
    return new Promise(function(resolve, reject) {
      fetch(url)
        .then(response => response.text())
        .then(text => {
          let reader = geo.createFileReader('jsonReader', {layer: layer});
          reader.read(text, resolve);
        })
        .catch(error => {
          console.error(error);
          reject(error)
        })
    })  // new Promise()
  }  // _downloadGeoJSONFile()

}  // GeoJSBuilder

export { GeoJSBuilder }
