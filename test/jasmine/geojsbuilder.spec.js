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
    let geoMap = builder.generate(node);
    expect(geoMap).toBeDefined();
    expect(geoMap.layers().length).toBe(0);
  });

  it('should instantiate a simple model', () => {
    let modelString = fs.readFileSync(__dirname + '/../models/basic_model.json');
    let model = JSON.parse(modelString);
    let node = document.querySelector('#map');
    let builder = new GeoJSBuilder();
    let geoMap = builder.generate(node, model);

    expect(geoMap.layers().length).toBe(2);
    let center = geoMap.center();
    expect(center.x).toBeCloseTo(model.options.center.x);
    expect(center.y).toBeCloseTo(model.options.center.y);
    let zoom = geoMap.zoom();
    expect(zoom).toBe(10);
  });

  it('should load a geojson object', () => {
    let modelString = fs.readFileSync(__dirname + '/../models/geojson_model.json');
    let model = JSON.parse(modelString);
    let node = document.querySelector('#map');
    let builder = new GeoJSBuilder();
    let geoMap = builder.generate(node, model);

    let layers = geoMap.layers()
    expect(layers.length).toBe(2);
    for (let layer of layers) {
      console.log(`layer ${layer.name()}, features: ${layer.features().length}`);
      //console.dir(layer.features());
    }
  });

});
