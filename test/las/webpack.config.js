var path = require('path');
var webpack = require('webpack');
var vtkRules = require('vtk.js/Utilities/config/dependency.js').webpack.v2.rules;

module.exports = {
  entry: path.join(__dirname, '../../src/pointcloud'),
  output: {
    path: __dirname,
    filename: 'pointcloud.bundle.js',
    libraryTarget: 'umd',
  },
  module: {
    rules: vtkRules,
  },
};
