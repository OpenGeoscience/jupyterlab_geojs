// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
// TODO: Fix this
// https://stackoverflow.com/questions/39496267/module-not-found-error-cant-resolve-hammerjs

import {
  Widget
} from '@phosphor/widgets';

import {
  IRenderMime
} from '@jupyterlab/rendermime-interfaces';

//import * as Hammer from 'geojs/geo.ext.js';

//declare function require(name:string);
//var Hammer = require('hammerjs/hammer.js');

import * as geojs from 'geojs';

// import 'leaflet/dist/leaflet.css';

import '../style/index.css';


/**
 * The CSS class to add to the GeoJSON Widget.
 */
const CSS_CLASS = 'jp-RenderedGeoJSON';

/**
 * The CSS class for a GeoJSON icon.
 */
const CSS_ICON_CLASS = 'jp-MaterialIcon jp-GeoJSONIcon';

/**
 * The MIME type for Vega.
 *
 * #### Notes
 * The version of this follows the major version of Vega.
 */
export
const MIME_TYPE = 'application/geo+json';

/**
 * Set base path for leaflet images.
 */
// leaflet.Icon.Default.imagePath = 'https://unpkg.com/leaflet/dist/images/';

/**
 * The url template that leaflet tile layers.
 * See http://leafletjs.com/reference-1.0.3.html#tilelayer
 */
//const URL_TEMPLATE: string = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

/**
 * The options for leaflet tile layers.
 * See http://leafletjs.com/reference-1.0.3.html#tilelayer
 */
//const LAYER_OPTIONS: TileLayerOptions = {
//  attribution: 'Map data (c) <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
//  minZoom: 0,
//  maxZoom: 18
//};


export
class RenderedGeoJSON extends Widget implements IRenderMime.IRenderer {
  /**
   * Create a new widget for rendering Vega/Vega-Lite.
   */
  constructor(options: IRenderMime.IRendererOptions) {
    super();
    this.addClass(CSS_CLASS);
    this._mimeType = options.mimeType;
  }

  /**
   * Dispose of the widget.
   */
  dispose(): void {
    //this._map.remove();
    this._map = null;
    super.dispose();
  }

  /**
   * Render GeoJSON into this widget's node.
   */
  renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    const data = model.data[this._mimeType] as any;
    const metadata = model.metadata[this._mimeType] as any || {};
    return new Promise<void>((resolve, reject) => {
      this._map = geojs.map({
        node: this.node,
        center: {
          x: -98,
          y: 39
        },
        zoom: 3
      });
      this._map.createLayer('osm');
      // TODO: Fix this

      var layer = this._map.createLayer('feature');
      var reader = geojs.createFileReader('jsonReader', {'layer': layer});
      reader.read(data);
      this._map.draw();


      //this._geoJSONLayer = leaflet.geoJSON(data).addTo(this._map);
      //this._map.fitBounds(this._geoJSONLayer.getBounds());
      //this._map.invalidateSize();
      resolve(undefined);
    });
  }

  /**
   * A message handler invoked on a `'resize'` message.
   */
  protected onResize(msg: Widget.ResizeMessage) {
    this._width = msg.width;
    this._height = msg.height;

    if (this._width > 0 && this._height > 0)
    {
      this._map.size({width:this._width, height:this._height});
      this._map.draw();
    }
    console.log(msg);

    //this._map.fitBounds(this._geoJSONLayer.getBounds());
    //this._map.invalidateSize();
  }

  private _map: geojs.Map;
  //private _geoJSONLayer: leaflet.GeoJSON;
  private _width = -1;
  private _height = -1;
  private _mimeType: string;
}


/**
 * A mime renderer factory for GeoJSON data.
 */
export
const rendererFactory: IRenderMime.IRendererFactory = {
  safe: true,
  mimeTypes: [MIME_TYPE],
  createRenderer: options => new RenderedGeoJSON(options)
};


const extensions: IRenderMime.IExtension | IRenderMime.IExtension[] = [
  {
    name: 'GeoJSON',
    rendererFactory,
    rank: 0,
    dataType: 'json',
    fileTypes: [{
      name: 'GeoJSON',
      mimeTypes: [MIME_TYPE],
      extensions: ['.geojson', '.geo.json'],
      iconClass: CSS_ICON_CLASS
    }],
    documentWidgetFactoryOptions: {
      name: 'GeoJSON',
      primaryFileType: 'GeoJSON',
      fileTypes: ['GeoJSON'],
      defaultFor: ['GeoJSON']
    }
  }
];

export default extensions;
