import {
  Widget
} from '@phosphor/widgets';

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
  }

  /**
   * Render GeoJS into this widget's node.
   */
  renderModel(model) {
    this.node.textContent = model.data[this._mimeType];
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
  name: 'GeoJS',
  rendererFactory,
  rank: 0,
  dataType: 'json',documentWidgetFactoryOptions: {
    name: 'GeoJS',
    primaryFileType: 'geojson',
    fileTypes: ['geojson'],
    defaultFor: []
  },
  fileTypes: []

};

export default extension;
