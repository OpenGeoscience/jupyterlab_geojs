import { IRenderMime } from '@jupyterlab/rendermime-interfaces';

import { Widget } from '@phosphor/widgets';

import { GeoJSBuilder } from './geojsbuilder.js';

import '../style/index.css';


/**
 * The default mime type for the extension.
 */
const MIME_TYPE = 'application/geojs';


/**
 * The class name added to the extension.
 */
const CLASS_NAME = 'jp-OutputWidgetGeoJS';


/**
 * A widget for rendering GeoJS.
 */
export
class OutputWidget extends Widget implements IRenderMime.IRenderer {
  /**
   * Construct a new output widget.
   */
  constructor(options: IRenderMime.IRendererOptions) {
    super();
    this._mimeType = options.mimeType;
    this.addClass(CLASS_NAME);

    // Keep reference to geomap, for resizing and dispose
    this._geoMap = null;
  }

  /**
   * Dispose of the widget
   */
  dispose() {
    // Dispose of the geojs map
    if (!!this._geoMap) {
      console.debug('Disposing geo.map');
      this._geoMap.exit();
      this._geoMap = null;
    }
    super.dispose();
  }

  /**
   * Handle widget resize
   */
  onResize(msg: Widget.ResizeMessage) {
    if (!this._geoMap) {
      return;
    }
    // Update map to its element size
    this._geoMap.size({
      width: this._geoMap.node().width(),
      height: this._geoMap.node().height()
    });
  }

  /**
   * Render GeoJS into this widget's node.
   */
  renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    //console.log(`OutputWidget.renderModel() ${this._mimeType}`);
    //console.dir(model);
    //this.node.textContent = model.data[this._mimeType];
    const data = model.data[this._mimeType] as any;
    //const metadata = model.metadata[this._mimeType] as any || {};

    const mapModel = data;
    if (!mapModel) {
      console.error('mapModel missing');
    }

    // Make sure any existing map is removed
    if (!!this._geoMap) {
      console.debug('Deleting geo.map instance');
      this._geoMap.exit();  // safety first
      this._geoMap = null;
    }

    let builder = new GeoJSBuilder();
    // Return promise that resolves when builder generates map
    return new Promise<void>((resolve, reject) => {
      builder.generate(this.node, mapModel)
       .then((geoMap:any) => {
          this._geoMap = geoMap;
          // Need resize event to get map to fill widget
          this.onResize(new Widget.ResizeMessage(-1, -1));
          this._geoMap.draw();
          resolve();
       }, reject => console.error(reject))
      .catch(error => { reject(error); });
    });
  }  // renderModel()

  private _geoMap: any;
  private _mimeType: string;
}  // OutputWidget


/**
 * A mime renderer factory for GeoJS data.
 */
export
const rendererFactory: IRenderMime.IRendererFactory = {
  safe: true,
  mimeTypes: [MIME_TYPE],
  createRenderer: options => new OutputWidget(options)
};

export
const extension: IRenderMime.IExtension = {
  id: 'jupyterlab_geojs:factory',
  rendererFactory,
  rank: 0,
  dataType: 'json',
  documentWidgetFactoryOptions: {
    name: 'GeoJSMap',
    primaryFileType: 'geojson',
    fileTypes: ['geojson'],
    defaultFor: []
  },
  fileTypes: [
    {
      name: 'geojs',
      mimeTypes: [MIME_TYPE],
      extensions: ['.geojs']
    }
  ]

};

export default extension;
