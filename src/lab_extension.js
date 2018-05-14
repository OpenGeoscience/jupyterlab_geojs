import {
  Widget
} from '@phosphor/widgets';

import geo from 'geojs';

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
    this._geoMap = null;
    console.assert(this.node);
    this._geoMap = geo.map({node: this.node});
    this._geoMap.createLayer('osm');
  }

  /**
   * Dispose of the widget
   */
  dispose() {
    // Dispose of the geojs map
    this._geoMap.exit();
    this._geoMap = null;
    super.dispose();
  }

  /**
   * Render GeoJS into this widget's node.
   */
  renderModel(model) {
    //console.log(`OutputWidget.renderModel() ${this._mimeType}`);
    console.dir(model);
    //this.node.textContent = model.data[this._mimeType];
    //this.node.textContent = 'Hello from jupyterlab_geojs';
    this._geoMap.draw();
  }

}


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
