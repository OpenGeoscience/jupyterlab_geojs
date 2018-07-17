var path = require('path');
var webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');
var vtkRules = require('vtk.js/Utilities/config/dependency.js').webpack.v2.rules;

/*
  "JUPYTERLAB_FILE_LOADER_" is a special file prefix that indicates to
  jupyterlab to use its file loader to load the file, instead of
  bundling it with the rest of the extension files at build time.
  This allows the vtk.js code to be packaged separately, because it
  requries some webpack loaders that are not available using jlpm.

  This config generates two files in the lib folder:
    1. JUPYTERLAB_FILE_LOADER_pointcloud.bundle.js, which is the
       point cloud implemenation.
    2. JUPYTERLAB_FILE_LOADER_pointcloud.bundle.d.ts, which is a
       copy of the src/pointcloude/index.d.ts file. This file has the
       minimal definitions needed to successfully compile the
       extension ("jlpm build").
*/
module.exports = {
  entry: path.join(__dirname, './src/pointcloud/index.js'),
  output: {
    path: path.join(__dirname, 'lib'),
    filename: 'JUPYTERLAB_FILE_LOADER_pointcloud.bundle.js',
    libraryTarget: 'umd',
  },
  mode: 'development',
  devtool: 'source-map',
  module: {
    rules: vtkRules,
  },
  plugins: [
    new CopyWebpackPlugin([
      {
        // See not above re JUPYTER_FILE_LOADER_ prefix
        from: './src/pointcloud/index.d.ts',
        to: 'JUPYTERLAB_FILE_LOADER_pointcloud.bundle.d.ts',
        toType: 'file'
      },
    ])  // new CopyWebpackPlugin()
  ]  // plugins
};
