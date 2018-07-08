import { LASFile } from './laslaz'
import { ParticleSystem } from './particlesystem'

class LASPointCloud {
  constructor() {
    this.lasFile = null;
    this.lasHeader = null;
    this.particleSystem = null;
  }  // constructor()

  // Deletes resources
  dispose() {
    this.particleSystem.destroy();
    this.particleSystem = null;

    // Todo add LASFile.destroy() method
    // This is a poor man's equivalent
    this.lasFile = null;
    this.lasHeader = null;

  }

  // Returns promise
  loadData(arraybuffer) {
    return new Promise((resolve, reject) => {
      this.lasFile = new LASFile(arraybuffer);
      // Load the LAS file
      this.lasFile.open()
        .then(() => this.lasFile.getHeader())
        .then(header => {
          this.lasHeader = header;
          console.log('LAS header:');
          //console.dir(header);
          let count = header.pointsCount
          console.log(`Input point count ${count}`);
          return this.lasFile.readData(count, 0, 0);
        })
        .then(data => {
          //- console.log('readData result:');
          //- console.dir(data);

          let Unpacker = this.lasFile.getUnpacker();

          // Remove extant particle system then make new one
          if (this.particleSystem) {
            this.particleSystem.destroy();
          }
          this.particleSystem = new ParticleSystem();
          this.particleSystem.push(new Unpacker(
            data.buffer, data.count, this.lasHeader));
        })
        .then(() => {
          this.lasFile.close();
          console.log(`Loaded point count ${this.particleSystem.pointsSoFar}`);
          resolve();
        })
        .then(() => {
          // Poor man's way to release resources in LASFile
          delete this.lasFile.arraybuffer;
          this.lasFile.arraybuffer = null;
        })
        .catch(err => {
          this.lasFile.close(); alert(err);
          reject()
        })
    });  // new Promise()
  }  // loadData()

  lasVersion() {
    return this.lasFile ? this.lasFile.versionAsString : 'no data';
  }

  pointCount() {
    return this.lasHeader ? this.lasHeader.pointsCount : -1;
  }

  pointFormat() {
    return this.lasFile ? this.lasFile.formatId : -1;
  }

  render(elem) {
    if (!this.lasHeader) {
      console.error('No LAS data -- nothing to render');
      return;
    }

    this.particleSystem.init(elem);
    this.particleSystem.render(true);
    this.particleSystem.resize(elem);
  }
}

export { LASPointCloud }
