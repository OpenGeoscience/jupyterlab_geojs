import { LASFile } from './laslaz'
import { ParticleSystem } from './particlesystem'

class LASPointCloud {
  constructor() {
    this.particleSystem = new ParticleSystem();

    // Temp variables used in loadData()
    this._lasFile = null;
    this._lasHeader = null;
  }  // constructor()

  // Deletes resources
  dispose() {
    this.particleSystem.destroy();
    this.particleSystem = null;
  }

  // Parses LAS public header from input arraybuffer
  // Input arraybuffer must be long enough to include header
  // For LAS 1.4 and lower, 350 bytes is sufficient.
  // Returns Promise<header>
  static
  getLASHeader(arraybuffer) {
    return new Promise((resolve, reject) => {
      let lasFile = new LASFile(arraybuffer);
      lasFile.open()
        .then(() => lasFile.getHeader())
        .then(header => resolve(header))
        .catch(err => reject(err));
      });  // newPromise
  }  // getLASHeader()

  // Returns promise
  loadData(arraybuffer) {
    return new Promise((resolve, reject) => {
      this._lasFile = new LASFile(arraybuffer);
      // Load the LAS file
      this._lasFile.open()
        .then(() => this._lasFile.getHeader())
        .then(header => {
          this._lasHeader = header;
          console.log('LAS header:');
          //console.dir(header);
          let count = header.pointsCount
          console.log(`Input point count ${count}`);

          return this._lasFile.readData(count, 0, 0);
        })
        .then(data => {
          //- console.log('readData result:');
          //- console.dir(data);
          let Unpacker = this._lasFile.getUnpacker();
          this.particleSystem.push(new Unpacker(
            data.buffer, data.count, this._lasHeader));
        })
        .then(() => {
          this._lasFile.close();
          console.log(`Loaded point count ${this.particleSystem.pointsSoFar}`);
          resolve();
        })
        .then(() => {
          // Poor man's way to release resources
          delete this._lasFile.arraybuffer;
          this._lasFile.arraybuffer = null;
          this._lasHeader = null;
          this._lasFile = null;
        })
        .catch(err => {
          this._lasFile.close(); alert(err);
          reject()
        })
    });  // new Promise()
  }  // loadData()

  pointCount() {
    return this.particleSystem.pointsSoFar;
  }

  render(elem) {
    if (!this.pointCount()) {
      console.error('No LAS data -- nothing to render');
      return;
    }

    this.particleSystem.init(elem);
    this.particleSystem.render(true);
    this.particleSystem.resize(elem);
  }

  setZRange(zmin, zmax) {
    this.particleSystem.setZRange(zmin, zmax);
  }
}

export { LASPointCloud }
