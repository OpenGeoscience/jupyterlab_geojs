export interface IColorFormat {
  DOUBLE: symbol;
  RGB: symbol;
  HEX: symbol;
}
export var ColorFormat: IColorFormat;

export class ColorMap {
  constructor(name?: string);
  static listColorSeries(): string[];
  useColorSeries(name: string): void;
  inputColorSeries(values: number[][]): void;
  interpolateColor(x: number, format?: symbol): any;
}
