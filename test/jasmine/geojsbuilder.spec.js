// Tests for GeoJSBuilder

import fs from 'fs';
import { GeoJSBuilder } from '../../src/geojsbuilder.js';

describe('jasmine', () => {
  it('should be configured for testing', () => {
    expect(true).toBeTruthy();
  });
});

describe('GeoJSBuilder', () => {
  it('should be able to initialize a geo.map instance', () => {
    let node = document.querySelector('#map');
    expect(node).toBeDefined();
    let builder = new GeoJSBuilder();
    let map = builder.generate(node);
    expect(map).toBeDefined();
    expect(map.layers().length).toBe(0);
  });

  it('should instantiate a simple model', () => {
    let modelString = fs.readFileSync(__dirname + '/../models/basic_model.json');
    let model = JSON.parse(modelString);
    let node = document.querySelector('#map');
    let builder = new GeoJSBuilder();
    let map = builder.generate(node, model);

    expect(map.layers().length).toBe(2);
    let center = map.center();
    expect(center.x).toBeCloseTo(model.options.center.x);
    expect(center.y).toBeCloseTo(model.options.center.y);
    let zoom = map.zoom();
    expect(zoom).toBe(10);
  });

  it('should load a geojson object', () => {
    let modelString = fs.readFileSync(__dirname + '/../models/geojson_model.json');
    let model = JSON.parse(modelString);
    let node = document.querySelector('#map');
    let builder = new GeoJSBuilder();
    let map = builder.generate(node, model);

    let layers = map.layers()
    expect(layers.length).toBe(1);
    let layer = layers[0];
    let features = layer.features();
    console.log(`features: ${features.length}`);
  });

});
