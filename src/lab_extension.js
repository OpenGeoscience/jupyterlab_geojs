import {
  Widget
} from '@phosphor/widgets';

import {
  GeoJSBuilder
} from './geojsbuilder.js';

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
class OutputWidget extends Widget {
  /**
   * Construct a new output widget.
   */
  constructor(options) {
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
      this._geoMap.exit();
      this._geoMap = null;
    }
    super.dispose();
  }

  /**
   * Handle widget resize
   */
  onResize(msg) {
    if (!this._geoMap) {
      return;
    }
    console.log('resize');
    // if (!!msg) {
    //   console.dir(msg);
    // }
    // console.dir(this._geoMap.node());
    // Update map to its element size
    this._geoMap.size({
      width: this._geoMap.node().width(),
      height: this._geoMap.node().height()
    });
  }

  /**
   * Render GeoJS into this widget's node.
   */
  renderModel(model) {
    //console.log(`OutputWidget.renderModel() ${this._mimeType}`);
    console.dir(model);
    //this.node.textContent = model.data[this._mimeType];
    //this.node.textContent = 'Hello from jupyterlab_geojs';
    let builder = new GeoJSBuilder();
    let mapModel = model.data['application/geojs'];
    if (!mapModel) {
      console.error('mapModel missing');
    }

    this._geoMap = builder.generate(this.node, mapModel);
    this.onResize();
    this._geoMap.draw();
  }

}  // OutputWidget


/**
 * A mime renderer factory for GeoJS data.
 */
export
const rendererFactory = {
  safe: true,
  mimeTypes: [MIME_TYPE],
  createRenderer: options => new OutputWidget(options)
};


const extension = {
  name: 'GeoJSMap',
  rendererFactory,
  rank: 0,
  dataType: 'json',documentWidgetFactoryOptions: {
    name: 'GeoJSMap',
    primaryFileType: 'geojson',
    fileTypes: ['geojson'],
    defaultFor: []
  },
  fileTypes: []

};

export default extension;
