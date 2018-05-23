// Tests for GeoJSBuilder

import fs from 'fs';
import geo from 'geojs';
import { GeoJSBuilder } from '../../src/geojsbuilder.js';

describe('jasmine', () => {
  it('should be configured for testing', () => {
    expect(true).toBeTruthy();
  });
});

describe('GeoJSBuilder', () => {

  // Use jasmine async support for convenience
  // (Async not technically required, but simpifies test code.)
  // Also use mockVGLRenderer()
  let geoMap = null;
  beforeEach(function(done) {
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


  it('should be able to initialize a geo.map instance', async () => {
    let node = document.querySelector('#map');
    expect(node).toBeDefined();
    let builder = new GeoJSBuilder();
    geoMap = await builder.generate(node);
    expect(geoMap).toBeDefined();
    expect(geoMap.layers().length).toBe(0);
  });

  it('should instantiate a simple model', async () => {
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
    let modelString = fs.readFileSync(__dirname + '/../models/geojson_model.json');
    let model = JSON.parse(modelString);
    //console.dir(model);
    let node = document.getElementById('map');
    let builder = new GeoJSBuilder();
    geoMap = await builder.generate(node, model)

    let layers = geoMap.layers()
    expect(layers.length).toBe(2);
    let layer1 = layers[1];
    expect(layer1.features().length).toBe(2)  // 1 polygon with 1 edge
  });

  it('should load basic features', async () => {
    let modelString = fs.readFileSync(__dirname + '/../models/basic_features.json');
    let model = JSON.parse(modelString);
    let node = document.querySelector('#map');
    let builder = new GeoJSBuilder();
    geoMap = await builder.generate(node, model);

    let layers = geoMap.layers()
    expect(layers.length).toBe(2);
    let layer1 = layers[1];
    expect(layer1.features().length).toBe(2)  // 1 point feature, 1 quad feature
  });

});
