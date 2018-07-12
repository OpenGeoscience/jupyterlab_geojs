import { IRenderMime } from '@jupyterlab/rendermime-interfaces';

import { GeoJSExtension } from './geojsextension';
import { PointCloudExtension } from './pointcloudextension';

const extensions: Array<IRenderMime.IExtension> = [GeoJSExtension, PointCloudExtension];
export default extensions;
