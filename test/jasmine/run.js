// Run jasmine tests
// We are using this script with babel-node in order to handle ES6 code
// As described at https://gist.github.com/mauvm/172878a9646095d03fd7
import { JSDOM } from 'jsdom';
import Jasmine from 'jasmine';

// Create jasmine instance
var jasmine = new Jasmine()
// FYI the config file is NOT in the default path
jasmine.loadConfigFile('test/jasmine/jasmine.json')

// Create dom instance and other mocks required for loading geojs
const dom = new JSDOM(`
  <!DOCTYPE html>
    <p>Hello world</p>
    <div id="map"></div>
`)
global.window = dom.window;
global.document = dom.window.document

// Fix strange problem detecting styles (setting variable isOldIE)
global.navigator = { userAgent: 'jasmine' };
global.self = {
  navigator: navigator
}

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
jasmine.execute()
