export class LASPointCloud {
  constructor();
  dispose(): void;
  loadData(arraybuffer: ArrayBuffer): Promise<void>;
  lasVersion(): string;
  pointCount(): number;
  pointFormat(): number;
  render(elem: HTMLElement): void;
}
