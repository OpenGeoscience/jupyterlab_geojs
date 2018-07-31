/*
 * Class for generating geomap based on geojs model received from Jupyter kernel.
 */

import { JSONObject } from '@phosphor/coreutils';


// Local interface definitions - do these need to be exported?
export interface IFeatureModel {
  data?: any;
  featureType: string;
  options?: JSONObject;
  url?: string;
}

export interface ILayerModel {
  features?: IFeatureModel[];
  layerType: string;
  options?: JSONObject;
}

export interface IMapModel {
  layers?: ILayerModel[];
  options?: JSONObject;
  viewpoint?: JSONObject;
}

interface IStringMap {
  [key: string] : any;
}


import { ColorFormat, ColorMap } from 'colorkit';
import * as geo from 'geojs'
console.debug(`Using geojs ${geo.version}`);

// Static var used to disable OSM layer renderer;
// For testing, so that we don't need to mock html canvas
let _disableOSMRenderer: boolean = false;


class GeoJSBuilder {
  // The GeoJS instance
  private _geoMap: any;

  // Hard code UI layer and tooltip logic
  private _tooltipLayer: any;
  private _tooltip: any;
  private _tooltipElem: HTMLElement;
  private _preElem: HTMLPreElement;

  private _colorMap: ColorMap;

  // Promise list used when building geojs map
  private _promiseList: Promise<void | {}>[];

  constructor() {
    this._geoMap = null;
    this._promiseList = null;  // for loading data

    this._tooltipLayer = null;
    this._tooltip = null;
    this._tooltipElem = null;
    this._preElem = null;

    this._colorMap = null;

    // let colormap = new ColorMap('rainbow');
    // for (let i=0; i<=10; ++i) {
    //   let x:number = 0.1 * i;
    //   let hex: string = colormap.interpolateColor(x, ColorFormat.HEX);
    //   console.log(`${i}. ${x.toFixed(1)} => ${hex}`);
    // }
  }

  // Sets static var
  static disableOSMRenderer(state: boolean): void {
    _disableOSMRenderer = state;
  }

  // Clears the current geo.map instance
  clear(): void {
    if (!!this._geoMap) {
      this._geoMap.exit();
      this._geoMap = null;
    }
  }

  // Returns PROMISE that resolves to geo.map instance
  // Note that caller is responsible for disposing the geo.map
  generate(node: HTMLElement, model: IMapModel={}): Promise<any> {
    console.log('GeoJSBuilder.generate() input model:')
    console.dir(model);
    if (!!this._geoMap) {
      console.warn('Deleting existing GeoJS instance');
      this.clear()
    }

    let options: JSONObject = model.options || {};
    // Add dom node to the map options
    const mapOptions = Object.assign(options, {node: node});
    this._geoMap = geo.map(mapOptions);

    this.update(model);
    const viewpoint: JSONObject = model.viewpoint;
    if (viewpoint) {
      switch (viewpoint.mode) {
        case 'bounds':
          // console.log('Input viewpoint bounds:');
          // console.dir(viewpoint.bounds);
          let spec = this._geoMap.zoomAndCenterFromBounds(viewpoint.bounds);
          // console.log('Computed viewpoint spec:')
          // console.dir(spec);
          this._geoMap.center(spec.center);
          this._geoMap.zoom(spec.zoom);
        break;

        default:
          console.warn(`Unrecognized viewpoint object ${model.viewpoint}`);
          console.dir(model.viewpoint);
      }
    }

    // Return promise that resolves to this._geoMap
    return new Promise((resolve, reject) => {
      Promise.all(this._promiseList)
        .then(() => resolve(this._geoMap), reject => console.error(reject))
        .catch(error => reject(error));
    });
  }  // generate()

  // Generates geomap layers
  // Note: Internal logic can push promise instances onto this._promiseList
  update(model: IMapModel={}): void {
    this._promiseList = [];
    let layerModels: ILayerModel[] = model.layers || [];
    for (let layerModel of layerModels) {
      let options: JSONObject = layerModel.options || {};
      let layerType: string = layerModel.layerType;
      //console.log(`layerType: ${layerType}`);
      if (_disableOSMRenderer && layerType == 'osm') {
        options.renderer = null;
      }
      let layer: any = this._geoMap.createLayer(layerType, options);
      //console.log(`Renderer is ${layer.rendererName()}`)
      if (layerModel.features) {
        this._createFeatures(layer, layerModel.features)
      }
    }  // for (layerModel)
  }  // update()


  // Creates features
  _createFeatures(layer: any, featureModels: IFeatureModel[]): void {
    for (let featureModel of featureModels) {
      //console.dir(featureModel);
      switch(featureModel.featureType) {
        case 'geojson':
          this._createGeoJSONFeature(layer, featureModel);
        break;

        case 'point':
        case 'quad':
          let feature: any = layer.createFeature(featureModel.featureType);
          let options: JSONObject = featureModel.options || {};
          if (options.data) {
            if (featureModel.featureType === 'quad') {
              // Copy the options.data array, because geojs might
              // attach a cached texture object, which won't serialze
              // when saving the associated notebook.
              let dataCopy: Array<Object> =
                (options.data as Array<Object>).map(obj => ({...obj}));
              //console.log(`Same? ${dataCopy[0] == (options.data as Array<Object>)[0]}`);
              feature.data(dataCopy);
            }
            else {
              feature.data(options.data);
            }
          }  // if (options.data)

          // If position array included, set position method
          if (options.position) {
            feature.position((dataItem: any, dataIndex: number) => {
              //console.debug(`dataIndex ${dataIndex}`);

              // Workaround undiagnosed problem where dataIndex
              // is sometimes undefined. It appears to be realted
              // to mousemove events.
              if (dataIndex === undefined) {
                // Check for Kitware workaround
                if ('__i' in dataItem) {
                  //console.debug('dataItem is undefined');
                  dataIndex = dataItem.__i;
                }
                else {
                  throw Error('dataIndex is undefined ')
                }
              }  // if
              let positions: any = options.position;
              let position: any = positions[dataIndex];
              // console.debug(`Position ${position}`);
              return position;
            });
          }

          // Other options that are simple properties
          const properties = ['bin', 'gcs', 'selectionAPI', 'visible']
          for (let property of properties) {
            if (options[property]) {
              feature[property](options[property]);
            }
          }

          // Handle style separately, since its components can be constant or array
          const styleProperties = options.style as IStringMap || {};
          let useStyle: IStringMap = {};
          for (let key in styleProperties) {
            let val: any = styleProperties[key]
            if (Array.isArray(val)) {
              useStyle[key] = function(d: IStringMap): any {
                let index = d.__i as number;
                return val[index];
              }
            }
            else {
              useStyle[key] = val;
            }
          }
          feature['style'](useStyle);

          // Events - note that we must explicitly bind to "this"
          if (options.enableTooltip) {
            // Add hover/tooltip - only click seems to work
            this._enableTooltipDisplay();
            feature.selectionAPI(true);
              feature.geoOn(geo.event.feature.mouseon, function(evt: any) {
                // console.debug('feature.mouseon');
                // console.dir(evt);
                this._tooltip.position(evt.mouse.geo);

                // Work from a copy of the event data
                let userData: any = Object.assign({}, evt.data);
                delete userData.__i;
                let jsData:string = JSON.stringify(
                  userData, Object.keys(userData).sort(), 2);
                // Strip off first and last lines (curly braces)
                let lines: string[] = jsData.split('\n');
                let innerLines: string[] = lines.slice(1, lines.length-1);
                this._preElem.innerHTML = innerLines.join('\n');
                this._tooltipElem.classList.remove('hidden');
              }.bind(this));
              feature.geoOn(geo.event.feature.mouseoff, function(evt: any) {
                //console.debug('featuremouseoff');
                this._preElem.textContent = '';
                this._tooltipElem.classList.add('hidden');
              }.bind(this));

              // feature.geoOn(geo.event.mouseclick, function(evt: any) {
              //   console.log('plain mouseclick, evt:');
              //   console.dir(evt);
              //   // this._tooltip.position(evt.geo);
              //   // this._tooltipElem.textContent = 'hello';
              //   // this._tooltipElem.classList.remove('hidden');
              // }.bind(this));

              //.geoOn(geo.event.zoom, resimplifyOnZoom);
          }  // if (options.data)

          if (options.colormap) {
            console.log('Using colormap');
            if (!this._colorMap) {
              this._colorMap = new ColorMap();
            }
            let colorOptions = options.colormap as JSONObject;
            let field = colorOptions.field as string;
            if (!field) {
              throw Error('colormap specified without field item');
            }
            if ('colorseries' in colorOptions) {
              this._colorMap.useColorSeries(colorOptions.colorseries as string);
            }
            if ('range' in colorOptions) {
              this._colorMap.setInputRange(colorOptions.range as number[]);
            }
            // Setup fillColor function
            feature.style({
              fillColor: function(dataItem: any): string {
                // console.log(`fillColor with dataItem:`);
                // console.log(dataItem);
                // console.log(`field: ${field}`);
                //return '#993399';
                let val = dataItem[field] as number;
                // console.log(`input value ${val}`)
                if (val) {
                  let color: string= this._colorMap.interpolateColor(val, ColorFormat.HEX);
                  // console.log(`color \"${color}\"`)
                  return color;
                }
                // (else)
                return 'red';
              }.bind(this)  // fillColor
            });  // feature.style()

          }  // if (options.color)
        break;

        default:
          throw `Unrecognized feature type ${featureModel.featureType}`;
      }  // switch
    }
  }  // _createFeatures()

  // Generates GeoJSON feature from feature model
  _createGeoJSONFeature(layer: any, featureModel: IFeatureModel): void {
    if (featureModel.data) {
      let p: Promise<void | {}> = this._loadGeoJSONObject(layer, featureModel.data);
      this._promiseList.push(p);
    }
    if (featureModel.url) {
      let p: Promise<void | {}> = this._downloadGeoJSONFile(layer, featureModel.url);
      this._promiseList.push(p);
    }
  }

  // Loads GeoJSON object
  _loadGeoJSONObject(layer:any, data: any): Promise<void> {
    // console.dir(layer);
    // console.dir(data);

    let reader: any = geo.createFileReader('jsonReader', {layer: layer});
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

  _downloadGeoJSONFile(layer: any, url: string): Promise<void> {
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

  // Initializes UI layer for tooltip display
  _enableTooltipDisplay(): void {
    if (this._tooltipLayer) {
      return;
    }

    // Initialize UI layer and tooltip
    console.log('Adding tooltip layer');
    this._tooltipLayer = this._geoMap.createLayer('ui', {zIndex: 9999});
    this._tooltip = this._tooltipLayer.createWidget('dom', {position: {x: 0, y:0}});
    this._tooltipElem = this._tooltip.canvas();
    //this._tooltipElem.id = 'tooltip';
    this._tooltipElem.classList.add('jp-TooltipGeoJS', 'hidden');
    this._preElem = document.createElement('pre');
    this._tooltipElem.appendChild(this._preElem);
  }

}  // GeoJSBuilder

export { GeoJSBuilder }
