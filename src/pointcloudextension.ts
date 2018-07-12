import { IRenderMime } from '@jupyterlab/rendermime-interfaces';

import { JSONObject } from '@phosphor/coreutils';
import { Widget } from '@phosphor/widgets';

import { decode as base64Decode } from 'base64-arraybuffer';

import { LASPointCloud } from '../lib/JUPYTERLAB_FILE_LOADER_pointcloud.bundle.js';

// Local interface definitions - do these need to be exported?
export interface IFeatureModel {
  data: string[];
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
   * Current code only supports ONE pointcloud
   */
  async renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    //console.log(`OutputWidget.renderModel() ${this._mimeType}`);
    //console.dir(model);
    const mapModel = model.data[this._mimeType] as any;
    if (!mapModel) {
      console.error('mapModel missing');
    }

    let pointcloud = new LASPointCloud();
    let buffers: ArrayBuffer[] = [];

    let layerModels: ILayerModel[] = mapModel.layers || [];
    for (let layerModel of layerModels) {
      let featureModels: IFeatureModel[] = layerModel.features;
      for (let featureModel of featureModels) {
        // console.log('featureModel:')
        // console.dir(featureModel);
        const lasArray: string[] = featureModel.data;
        for (let lasString of lasArray) {
          const binaryData: ArrayBuffer = base64Decode(lasString);
          buffers.push(binaryData);
        }  // lasString
      }  // for (featureModel)
    }  // for (layerModel)
    pointcloud.loadBuffers(buffers)
      .then(() => {
        if (!pointcloud.pointCount()) {
          // If we reach here, then no pointcloud features detected, so...
          //console.log('No pointcloud feature');
          this.node.textContent = 'No pointcloud feature to display';
          return Promise.resolve();
        }
        // (else)
        return pointcloud.render(this.node);
      });
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
