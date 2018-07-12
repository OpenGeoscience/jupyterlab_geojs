export class LASPointCloud {
  constructor();
  dispose(): void;
  loadBuffers(arraybuffers: ArrayBuffer[]): Promise<void>;
  loadFiles(files: Blob[]): Promise<void>;
  lasVersion(): string;
  pointCount(): number;
  pointFormat(): number;
  render(elem: HTMLElement): void;
}
