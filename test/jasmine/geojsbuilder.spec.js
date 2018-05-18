import { GeoJSBuilder } from '../../src/geojsbuilder.js';

describe('jasmine', function() {
  it('should be configured for testing', function() {
    expect(true).toBeTruthy();
  });
});

describe('GeoJSBuilder', function() {
  it('should be able to initialize a geo.map instance', function() {
    let node = document.querySelector('#map');
    expect(node).toBeDefined();
    let builder = new GeoJSBuilder();
    let map = builder.generate(node);
    expect(map).toBeDefined();
  });
});
