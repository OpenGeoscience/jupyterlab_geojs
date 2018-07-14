// Simple color map class
// Adapted from https://github.com/timothygebhard/js-colormaps

import rainbow from './rainbow.js';

let ColorSeriesTable = {
  'rainbow': rainbow,
};

const ColorFormat = Object.freeze({
    DOUBLE: Symbol('double'),  // 3-tuple with double values 0.0-1.0
    HEX:    Symbol('hex'),     // standard hex string "#ddddd"
    RGB:    Symbol('rgb'),     // 3-tuple with unsigned values 0-255
});

class ColorMap {
  constructor(colorSeriesName) {
    this.x_values = null;
    this.r_values = null;
    this.g_values = null;
    this.b_values = null;
    this.x_range = [0.0, 1.0];  // default

    if (colorSeriesName) {
      this.useColorSeries(colorSeriesName);
    }
  }  // constructor

  // Lists available colormaps
  static
  listColorSeries() {
    return ColorSeriesTable.keys();
  }

  setInputRange(range) {
    this.x_range = range;
  }

  useColorSeries(name) {
    if (!(name in ColorSeriesTable)) {
      throw Error(`Unrecognized colormap name ${name}`);
    }
    let values = ColorSeriesTable[name];
    this.inputColorSeries(values);
    console.log(`Using color series ${name}`);
  }

  inputColorSeries(values) {
    // Split values into four lists
    this.x_values = [];
    this.r_values = [];
    this.g_values = [];
    this.b_values = [];
    for (let i in values) {
        this.x_values.push(values[i][0]);
        this.r_values.push(values[i][1][0]);
        this.g_values.push(values[i][1][1]);
        this.b_values.push(values[i][1][2]);
    }  // for (i)
  }  // inputColorSeries()

  interpolateColor(val, format=ColorFormat.RGB) {
    if (!this.x_values) {
      //throw Error('color map not initialized');
      // Use rainbow as default color series
      this.inputColorSeries(rainbow);
    }

    // Scale input value
    let scaled = (val - this.x_range[0]) / (this.x_range[1] - this.x_range[0]);
    let x = this.enforceBounds(scaled);

    // Traverse values brute force
    let i = 1;
    while (this.x_values[i] < x) {
        i = i+1;
    }
    i = i-1;

    let width = Math.abs(this.x_values[i] - this.x_values[i+1]);
    let scaling_factor = (x - this.x_values[i]) / width;

    // Get the new color values though interpolation
    let r = this.r_values[i] + scaling_factor * (this.r_values[i+1] - this.r_values[i]);
    let g = this.g_values[i] + scaling_factor * (this.g_values[i+1] - this.g_values[i]);
    let b = this.b_values[i] + scaling_factor * (this.b_values[i+1] - this.b_values[i]);

    let doubleResult = [this.enforceBounds(r), this.enforceBounds(g), this.enforceBounds(b)];
    //console.log(`doubleResult ${doubleResult}`);
    if (format == ColorFormat.DOUBLE) {
      return doubleResult;
    }

    // Convert to rgb (0-255)
    let rgbResult = doubleResult.map(val => Math.round(255.0 * val));
    //console.log(`rgbResult ${rgbResult}`);
    if (format == ColorFormat.RGB) {
      return rgbResult;
    }

    if (format == ColorFormat.HEX) {
      // Convert to hex string array
      let hexResult = rgbResult.map(val => ('0' + val.toString(16)).slice(-2));
      //console.log(`hexResult ${hexResult}`);
      return '#' + hexResult.join('');
    }

    // (else) Some format we missed
    throw Error(`Unrecognized ColorFormat ${format}`);
  }  // interpolateColor()

  enforceBounds(x) {
      if (x < 0) {
          return 0;
      } else if (x > 1){
          return 1;
      } else {
          return x;
      }
  }  // enforceBounds()

}  // Colormap

export { ColorFormat, ColorMap };
