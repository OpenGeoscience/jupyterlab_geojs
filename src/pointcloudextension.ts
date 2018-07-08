import { IRenderMime } from '@jupyterlab/rendermime-interfaces';

import { Widget } from '@phosphor/widgets';

import '../style/index.css';


/**
 * The default mime type for the extension.
 */
const MIME_TYPE = 'application/las+json';


/**
 * The class name added to the extension.
 */
const CLASS_NAME = 'jp-OutputWidgetLAS';


/**
 * A widget for rendering pointcloud data; uses vtk.js
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
  }

  /**
   * Render into this widget's node.
   */
  renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    //console.log(`OutputWidget.renderModel() ${this._mimeType}`);
    //console.dir(model);
    this.node.textContent = this._mimeType;
    return Promise.resolve();
  }  // renderModel()

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
const PointCloudExtension: IRenderMime.IExtension = {
  id: 'jupyterlab_geojs:las_factory',
  rendererFactory,
  rank: 0,
  dataType: 'json',
  documentWidgetFactoryOptions: {
    name: 'LASPointCloud',
    primaryFileType: 'las',
    fileTypes: ['las'],
    defaultFor: []
  },
  fileTypes: [
    {
      name: 'las',
      mimeTypes: [MIME_TYPE],
      extensions: ['.las']
    }
  ]

};
