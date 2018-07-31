// Tests for GeoJSBuilder

import fs from 'fs';
import geo from 'geojs';
import { GeoJSBuilder } from '../../lib/geojsbuilder.js';

describe('jasmine', () => {
  it('should be configured for testing', () => {
    expect(true).toBeTruthy();
  });
});

describe('GeoJSBuilder', () => {

  // Use jasmine async support for convenience
  // (Async not technically required, but simpifies test code.)
  // Also disable OSM renderer so that we don't have to mock canvas
  // Also use mockVGLRenderer()

  // USE STATIC/GLOBAL geoMap VARIABLE IN ALL TESTS
  let geoMap = null;

  beforeEach(function(done) {
    // Wait for async tests
    setTimeout(function() {
      if (geoMap) {
        geoMap.exit();
        geoMap = null;
      }
      geo.util.mockVGLRenderer();
      done();
    }, 1);
  });

  afterEach(() => {
    geo.util.restoreVGLRenderer();
  });

  // Helper method to load model
  // @param modelFile: string relative path to input model file (optional)
  async function initGeoMap(modelFile) {
    let node = document.querySelector('#map');
    let modelString = fs.readFileSync(__dirname + '/' + modelFile);
    let model = JSON.parse(modelString);
    let builder = new GeoJSBuilder();
    return builder.generate(node, model);
  };

  it('should be able to initialize a geo.map instance', async () => {
    let node = document.querySelector('#map');
    expect(node).toBeDefined();
    let builder = new GeoJSBuilder();
    geoMap = await builder.generate(node);
    expect(geoMap).toBeDefined();
    expect(geoMap.layers().length).toBe(0);
  });

  it('should instantiate a simple model', async () => {
    // Init model locally so that we can query its contents
    let modelString = fs.readFileSync(__dirname + '/../models/basic_model.json');
    let model = JSON.parse(modelString);
    let node = document.querySelector('#map');
    let builder = new GeoJSBuilder();
    geoMap = await builder.generate(node, model);

    expect(geoMap.layers().length).toBe(2);
    let center = geoMap.center();
    expect(center.x).toBeCloseTo(model.options.center.x);
    expect(center.y).toBeCloseTo(model.options.center.y);
    let zoom = geoMap.zoom();
    expect(zoom).toBe(10);
  });

  it('should load a geojson object', async () => {
    geoMap = await initGeoMap('../models/geojson_model.json');

    let layers = geoMap.layers()
    expect(layers.length).toBe(2);
    let layer1 = layers[1];
    expect(layer1.features().length).toBe(2)  // 1 polygon with 1 edge
  });

  it('should load basic features', async () => {
    geoMap = await initGeoMap('../models/basic-features_model.json');

    let layers = geoMap.layers()
    // Expect 3 layers: osm, features, tooltip
    expect(layers.length).toBe(3);
    let layer1 = layers[1];
    // Expect 2 features: point feature, quad feature
    expect(layer1.features().length).toBe(2)
  });

  it('should load raster features', async () => {
    geoMap = await initGeoMap('../models/raster-rgb_model.json')

    let layers = geoMap.layers()
    expect(layers.length).toBe(2);
    let layer1 = layers[1];
    expect(layer1.features().length).toBe(1)  // 1 quad feature
  });

  it('should load raster features without GeoJSBuilder', () => {
    let node = document.querySelector('#map');
    geoMap = geo.map({node: node});

    let featureLayer = geoMap.createLayer('feature', {features: ['quad.image']});
    let featureData = {
      image: '../data/rasterwithpalette.png',
      ll: { x: -73.758345, y: 41.849604 },
      lr: { x: -72.758345, y: 41.849604 },
      ul: { x: -73.758345, y: 42.849604 },
      ur: { x: -72.758345, y: 42.849604 }
    };
    let feature = featureLayer.createFeature('quad').data([featureData]);

    const bounds = {"bottom": 41.849604, "left": -73.758345, "right": -72.758345, "top": 42.849604}
    let spec = geoMap.zoomAndCenterFromBounds(bounds);
    // console.log('Computed viewpoint spec:');
    // console.dir(spec);
    geoMap.center(spec.center);
    geoMap.zoom(spec.zoom / 2);
    //console.dir(node);
  });

});
