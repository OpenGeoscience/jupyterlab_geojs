/*
 * Class for generating geomap based on geojs model received from Jupyter kernel.
 */


import geo from 'geojs';

class GeoJSBuilder {
  constructor() {
    this._geoMap = null;
    this._promiseList = null;  // for loading data
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
    this._promiseList = [];
    let layerModels = model.layers || [];
    for (let layerModel of layerModels) {
      let options = layerModel.options || {};
      let layerType = layerModel.layerType;
      //console.log(`layerType: ${layerType}`);
      let layer = this._geoMap.createLayer(layerType, options);
      if (layerModel.features) {
        this._createFeatures(layer, layerModel.features)
      }
    }  // for (layerModel)

    // Wait for any promises to resolve, then draw
    Promise.all(this._promiseList)
      .then(() => {
        this._geoMap.draw();
        let layer = this._geoMap.layers()[0]
        //console.dir(layer);
      })
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
    //console.dir(data);
    return new Promise(function(resolve, reject) {
      // Unfortunately, must re-serialize the data in order
      // to use the geojs file reader
      let text = JSON.stringify(data);
      let reader = geo.createFileReader('jsonReader', {layer: layer});
      try {
        reader.read(text, resolve);
      }
      catch (error) {
        console.log('ERROR');
        console.error(error);
        reject(error);
      }
    })  // new Promise()
  }  // loadGeoJSONData()

  _downloadGeoJSONFile(layer, url) {
    console.log(`_downloadGeoJSONFile: ${url}`);
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
