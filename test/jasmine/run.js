// Run jasmine tests
// We are using this script with babel-node in order to handle ES6 code
// As described at https://gist.github.com/mauvm/172878a9646095d03fd7

import { JSDOM } from 'jsdom';
import Jasmine from 'jasmine';

// Create jasmine instance
var jasmine = new Jasmine();
// FYI the config file is NOT in the default path
jasmine.loadConfigFile('test/jasmine/jasmine.json');

// Create dom instance and mocks required for testing geojs
const dom = new JSDOM('<div id="map"></div>');
global.window = dom.window;
global.document = dom.window.document;
global.Image = dom.window.Image;  // needed for 'osm' layer
global.File = dom.window.File;    // needed for geoFileReader

// For some reason, jsdom not creating userAgent, so do it manually
let userAgent = `Mozilla/5.0 (${process.platform}) AppleWebKit/537.36 (KHTML, like Gecko) jsdom`;
global.navigator = { userAgent: userAgent };

// Fix strange problem detecting styles (setting variable isOldIE)
global.self = {
  navigator: global.navigator
}

// This fixes nonfatal errors when testing raster features
global.HTMLCanvasElement = window.HTMLCanvasElement;

// For some reason, the inherit() needs to be mocked
function newfunc() {
  return function() {};
}

global.inherit = function(C, P) {
  var F = newfunc();
  F.prototype = P.prototype;
  C.prototype = new F();
  C.prototype.constructor = C;
}

// Run the tests
jasmine.execute();
