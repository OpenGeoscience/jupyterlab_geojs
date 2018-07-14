import { LASFile } from './laslaz'
import { ParticleSystem } from './particlesystem'


// Function to run (map) in sequence an array of
// calls to a promise-returning function
// https://stackoverflow.com/a/41608207
Promise.each = async function(dataArray, fn) {
  for (const item of dataArray) await fn(item);
}


class LASPointCloud {
  constructor() {
    this.particleSystem = new ParticleSystem();
    this.input = {
      bounds: null,   // [xmin,xmax, ymin,ymax, zmin,zmax]
      formats: {},    // <point-record-format, point-count>
      pointCount: 0,  // overall point count
    }
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
      //console.log(`lasFile ${lasFile}`);
      lasFile.open()
        .then(() => lasFile.getHeader())
        .then(header => resolve(header))
        .catch(err => reject(err));
      });  // newPromise
  }  // getLASHeader()

  loadFiles(files) {
    return new Promise((resolve, reject) => {
      // Read files into arraybuffers
      //let buffers = [];
      let promiseList = [];
      for (let f of files) {
        let p = new Promise((resolve, reject) => {
          let fileReader = new FileReader();
          fileReader.onload = evt => {
            let buffer = evt.target.result;
            //buffers.push(buffer);
            resolve(buffer);
          }
          // Read files into array buffer
          fileReader.readAsArrayBuffer(f);
        });  // new Promise()
        promiseList.push(p);
      }  // for (f)

      // Load arraybuffers into particle system
      Promise.all(promiseList)
        .then(buffers => this.loadBuffers(buffers))
        .then(() => resolve());
    });  // new Promise()
  }  // loadFiles()

  loadBuffers(arraybuffers) {
    return new Promise((resolve, reject) => {
      // Parse headers first to compute overall bounds
      // We can do these concurrently, because
      // lasPointCloud.getLASHeader() is a static method.
      let promiseList = [];
      for (let buffer of arraybuffers) {
        let p = this.constructor.getLASHeader(buffer);  // calling static method
        promiseList.push(p);
      }
      Promise.all(promiseList)
        .then(headers => {
          for (let header of headers) {
            // Total point count
            this.input.pointCount += header.pointsCount;

            // Point count by point record format
            const format = header.pointsFormatId;
            let newCount = header.pointsCount;
            if (format in this.input.formats) {
              newCount += this.input.formats[format];
            }
            this.input.formats[format] = newCount;

            // And the bounds
            const bounds = [
              header.mins[0], header.maxs[0],  // xmin, xmax
              header.mins[1], header.maxs[1],  // ymin, ymax
              header.mins[2], header.maxs[2],  // zmin, zmax
              ]
            this.updateBounds(bounds);
          }  // for (header)
        })  // then (headers)
        .then(() => {
          this.setZRange(this.input.bounds[4], this.input.bounds[5]);
          //console.log(`bounds ${this.input.bounds}`);
          // Load each buffer in sequence
          return Promise.each(arraybuffers, buffer => this.loadData(buffer));
        })
        .then(() => resolve())
        .catch(err => {
          alert(err);
          reject(err);
        });
    });  // new Promise()

  }  // loadBuffers()

  // Returns promise
  loadData(arraybuffer) {
    return new Promise((resolve, reject) => {
      let lasFile = new LASFile(arraybuffer);
      let lasHeader = null;
      // Load the LAS file
      lasFile.open()
        .then(() => lasFile.getHeader())
        .then(header => {
          lasHeader = header;
          //console.log('LAS header:');
          //console.dir(header);
          let count = header.pointsCount
          console.log(`Input point count ${count}`);

          return lasFile.readData(count, 0, 0);
        })
        .then(data => {
          //- console.log('readData result:');
          //- console.dir(data);
          let Unpacker = lasFile.getUnpacker();
          this.particleSystem.push(new Unpacker(
            data.buffer, data.count, lasHeader));
        })
        .then(() => {
          lasFile.close();
          console.log(`Loaded point count ${this.particleSystem.pointsSoFar}`);
          resolve();
        })
        .then(() => {
          // Poor man's way to release resources
          delete lasFile.arraybuffer;
          lasFile.arraybuffer = null;
          lasHeader = null;
          lasFile = null;
        })
        .catch(err => {
          lasFile.close(); alert(err);
          reject()
        })
    });  // new Promise()
  }  // loadData()

  bounds() {
    return this.input.bounds;
  }

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

  updateBounds(newBounds) {
    if (!this.input.bounds) {
      this.input.bounds = newBounds;
      return;
    }
    // (else)
    for (let i=0; i<3; ++i) {
      let index = 2*i;
      if (newBounds[index] < this.input.bounds[index]) {
        this.input.bounds[index] = newBounds[index];
      }

      ++index;
      if (newBounds[index] > this.input.bounds[index]) {
        this.input.bounds[index] = newBounds[index];
      }
    }  // for (i)
  }  // updateBounds()

}  // LASPointCloud

export { LASPointCloud }
