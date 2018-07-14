export class LASPointCloud {
  constructor();
  dispose(): void;
  loadBuffers(arraybuffers: ArrayBuffer[]): Promise<void>;
  loadFiles(files: Blob[]): Promise<void>;
  bounds(): number[];
  pointCount(): number;
  render(elem: HTMLElement): void;

  // For advanced users:
  static getLASHeader(arraybuffer: ArrayBuffer): Promise<any>;
  setZRange(zmin: number, zmax: number): void;
}
