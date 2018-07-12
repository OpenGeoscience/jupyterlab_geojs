// The MIT License (MIT)

// Copyright (c) 2014 Uday Verma, uday.karan@gmail.com

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

/**
 * Point format spec - currently reading 0, 1, 2, 3
 */
var pointFormatReaders = {
    0: function(dv) {
        return {
            "position": [ dv.getInt32(0, true), dv.getInt32(4, true), dv.getInt32(8, true)],
            "intensity": dv.getUint16(12, true),
            "classification": dv.getUint8(15, true)
        };
    },
    1: function(dv) {
        return {
            "position": [ dv.getInt32(0, true), dv.getInt32(4, true), dv.getInt32(8, true)],
            "intensity": dv.getUint16(12, true),
            "classification": dv.getUint8(15, true)
        };
    },
    2: function(dv) {
        return {
            "position": [ dv.getInt32(0, true), dv.getInt32(4, true), dv.getInt32(8, true)],
            "intensity": dv.getUint16(12, true),
            "classification": dv.getUint8(15, true),
            "color": [dv.getUint16(20, true), dv.getUint16(22, true), dv.getUint16(24, true)]
        };
    },
    3: function(dv) {
        return {
            "position": [ dv.getInt32(0, true), dv.getInt32(4, true), dv.getInt32(8, true)],
            "intensity": dv.getUint16(12, true),
            "classification": dv.getUint8(15, true),
            "color": [dv.getUint16(28, true), dv.getUint16(30, true), dv.getUint16(32, true)]
        };
    }
};

/**
 *
 * @param {*} buf
 * @param {*} Type
 * @param {*} offset
 * @param {*} count
 */
function readAs(buf, Type, offset, count) {
    count = (count === undefined || count === 0 ? 1 : count);
    var sub = buf.slice(offset, offset + Type.BYTES_PER_ELEMENT * count);

    var r = new Type(sub);
    if (count === undefined || count === 1)
        return r[0];

    var ret = [];
    for (var i = 0 ; i < count ; i ++) {
        ret.push(r[i]);
    }

    return ret;
}

/**
 * Parse LAS header
 *
 * @param {*} arraybuffer
 */
function parseLASHeader(arraybuffer) {
    var _this = {};

    _this.pointsOffset = readAs(arraybuffer, Uint32Array, 32*3);
    _this.pointsFormatId = readAs(arraybuffer, Uint8Array, 32*3+8);
    _this.pointsStructSize = readAs(arraybuffer, Uint16Array, 32*3+8+1);
    _this.pointsCount = readAs(arraybuffer, Uint32Array, 32*3 + 11);

    var start = 32*3 + 35;
    _this.scale = readAs(arraybuffer, Float64Array, start, 3); start += 24; // 8*3
    _this.offset = readAs(arraybuffer, Float64Array, start, 3); start += 24;

    var bounds = readAs(arraybuffer, Float64Array, start, 6); start += 48; // 8*6;
    _this.maxs = [bounds[0], bounds[2], bounds[4]];
    _this.mins = [bounds[1], bounds[3], bounds[5]];

    return _this;
}

/**
 * LAS Reader
 * @param {*} arraybuffer
 */
var LASLoader = function(arraybuffer) {
    this.arraybuffer = arraybuffer;
};

/**
 * Open the file
 */
LASLoader.prototype.open = function() {
    this.readOffset = 0;
    return new Promise(function(res, rej) {
        setTimeout(res, 0);
    });
};

/**
 * Get header information
 */
LASLoader.prototype.getHeader = function() {
    var _this = this;

    return new Promise(function(res, rej) {
        setTimeout(function() {
            _this.header = parseLASHeader(_this.arraybuffer);
            res(_this.header);
        }, 0);
    });
};

/**
 * Read point data in mini-batch mode
 */
LASLoader.prototype.readData = function(count, offset, skip) {
    var _this = this;

    return new Promise(function(res, rej) {
        setTimeout(function() {
            if (!_this.header)
                return rej(new Error("Cannot start reading data till a header request is issued"));

            var start;
            if (skip <= 1) {
                count = Math.min(count, _this.header.pointsCount - _this.readOffset);
                start = _this.header.pointsOffset + _this.readOffset * _this.header.pointsStructSize;
                var end = start + count * _this.header.pointsStructSize;
                res({
                    buffer: _this.arraybuffer.slice(start, end),
                    count: count,
                    hasMoreData: _this.readOffset + count < _this.header.pointsCount});
                _this.readOffset += count;
            }
            else {
                var pointsToRead = Math.min(count * skip, _this.header.pointsCount - _this.readOffset);
                var bufferSize = Math.ceil(pointsToRead / skip);
                var pointsRead = 0;

                var buf = new Uint8Array(bufferSize * _this.header.pointsStructSize);
                for (var i = 0 ; i < pointsToRead ; i ++) {
                    if (i % skip === 0) {
                        start = _this.header.pointsOffset + _this.readOffset * _this.header.pointsStructSize;
                        var src = new Uint8Array(_this.arraybuffer, start, _this.header.pointsStructSize);

                        buf.set(src, pointsRead * _this.header.pointsStructSize);
                        pointsRead ++;
                    }

                    _this.readOffset ++;
                }

                res({
                    buffer: buf.buffer,
                    count: pointsRead,
                    hasMoreData: _this.readOffset < _this.header.pointsCount
                });
            }
        }, 0);
    });
};

/**
 * Close the reader
 */
LASLoader.prototype.close = function() {
    var _this = this;
    return new Promise(function(res, rej) {
        _this.arraybuffer = null;
        setTimeout(res, 0);
    });
};

// LAZ Loader
// Uses NaCL module to load LAZ files
//
var LAZLoader = function(arraybuffer) {
    this.arraybuffer = arraybuffer;
    this.ww = new Worker("workers/laz-loader-worker.js");

    this.nextCB = null;
    var _this = this;

    this.ww.onmessage = function(e) {
        if (_this.nextCB !== null) {
            console.log('dorr: >>', e.data);
            _this.nextCB(e.data);
            _this.nextCB = null;
        }
    };

    this.dorr = function(req, cb) {
        console.log('dorr: <<', req);
        _this.nextCB = cb;
        _this.ww.postMessage(req);
    };
};

LAZLoader.prototype.open = function() {

    // nothing needs to be done to open this file
    //
    var _this = this;
    return new Promise(function(res, rej) {
        _this.dorr({type:"open", arraybuffer: _this.arraybuffer}, function(r) {
            if (r.status !== 1)
                return rej(new Error("Failed to open file"));

            res(true);
        });
    });
};

/**
 *
 */
LAZLoader.prototype.getHeader = function() {
    var _this = this;

    return new Promise(function(res, rej) {
        _this.dorr({type:'header'}, function(r) {
            if (r.status !== 1)
                return rej(new Error("Failed to get header"));

            res(r.header);
        });
    });
};

/**
 *
 */
LAZLoader.prototype.readData = function(count, offset, skip) {
    var _this = this;

    return new Promise(function(res, rej) {
        _this.dorr({type:'read', count: count, offset: offset, skip: skip}, function(r) {
            if (r.status !== 1)
                return rej(new Error("Failed to read data"));
            res({
                buffer: r.buffer,
                count: r.count,
                hasMoreData: r.hasMoreData
            });
        });
    });
};

/**
 *
 */
LAZLoader.prototype.close = function() {
    var _this = this;

    return new Promise(function(res, rej) {
        _this.dorr({type:'close'}, function(r) {
            if (r.status !== 1)
                return rej(new Error("Failed to close file"));

            res(true);
        });
    });
};

/**
 * A single consistent interface for loading LAS/LAZ files
 */
var LASFile = function(arraybuffer) {
    this.arraybuffer = arraybuffer;

    this.determineVersion();
    if (this.version > 13)
        throw new Error("Only file versions <= 1.3 are supported at this time");

    this.determineFormat();
    if (pointFormatReaders[this.formatId] === undefined)
        throw new Error("The point format ID is not supported");

    this.loader = this.isCompressed ?
        new LAZLoader(this.arraybuffer) :
        new LASLoader(this.arraybuffer);
};

/**
 *
 */
LASFile.prototype.determineFormat = function() {
    var formatId = readAs(this.arraybuffer, Uint8Array, 32*3+8);
    var bit_7 = (formatId & 0x80) >> 7;
    var bit_6 = (formatId & 0x40) >> 6;

    if (bit_7 === 1 && bit_6 === 1)
        throw new Error("Old style compression not supported");

    this.formatId = formatId & 0x3f;
    this.isCompressed = (bit_7 === 1 || bit_6 === 1);
};

/**
 *
 */
LASFile.prototype.determineVersion = function() {
    var ver = new Int8Array(this.arraybuffer, 24, 2);
    this.version = ver[0] * 10 + ver[1];
    this.versionAsString = ver[0] + "." + ver[1];
};

/**
 *
 */
LASFile.prototype.open = function() {
    return this.loader.open();
};

/**
 *
 */
LASFile.prototype.getHeader = function() {
    return this.loader.getHeader();
};

/**
 *
 */
LASFile.prototype.readData = function(count, start, skip) {
    return this.loader.readData(count, start, skip);
};

LASFile.prototype.close = function() {
    return this.loader.close();
};

/**
 * Decodes LAS records into points
 *
 * @param {*} buffer
 * @param {*} len
 * @param {*} header
 */
var LASDecoder = function(buffer, len, header) {
    //console.log(header);
    //console.log("POINT FORMAT ID:", header.pointsFormatId);
    this.arrayb = buffer;
    this.decoder = pointFormatReaders[header.pointsFormatId];
    this.pointsCount = len;
    this.pointSize = header.pointsStructSize;
    this.scale = header.scale;
    this.offset = header.offset;
    this.mins = header.mins;
    this.maxs = header.maxs;
};

/**
 *
 */
LASDecoder.prototype.getPoint = function(index) {
    if (index < 0 || index >= this.pointsCount)
        throw new Error("Point index out of range");

    var dv = new DataView(this.arrayb, index * this.pointSize, this.pointSize);
    return this.decoder(dv);
};

// NACL Module support
// Called by the common.js module.
//
// window.startNaCl = function(name, tc, config, width, height) {
//  // check browser support for nacl
//  //
//  if(!common.browserSupportsNaCl()) {
//      return $.event.trigger({
//          type: "plasi_this.nacl.error",
//          message: "NaCl support is not available"
//      });
//  }
//  console.log("Requesting persistent memory");

//  navigator.webkitPersistentStorage.requestQuota(2048 * 2048, function(bytes) {
//      common.updateStatus(
//          'Allocated ' + bytes + ' bytes of persistant storage.');
//          common.attachDefaultListeners();
//          common.createNaClModule(name, tc, config, width, height);
//  },
//  function(e) {
//      console.log("Failed!");
//      $.event.trigger({
//          type: "plasi_this.nacl.error",
//          message: "Could not allocate persistant storage"
//      });
//  });

//  $(document).on("plasi_this.nacl.available", function() {
//      scope.LASModuleWasLoaded = true;
//      console.log("NACL Available");
//  });
// };

/**
 *
 */
LASFile.prototype.getUnpacker = function() {
    return LASDecoder;
};

// <!-- })(module.exports); -->


/**
 *
 * @param {*} url
 * @param {*} cb
 */
var getBinary = function(url, cb) {
    var oReq = new XMLHttpRequest();
    return new Promise(function(resolve, reject) {
        oReq.open("GET", url, true);
        oReq.responseType = "arraybuffer";

        oReq.onload = function(oEvent) {
            if (oReq.status == 200) {
                console.log(oReq.getAllResponseHeaders());
                return resolve(new LASFile(oReq.response));
            }
            reject(new Error("Could not get binary data"));
        };

        oReq.onerror = function(err) {
            reject(err);
        };

        oReq.send();
    });
};

/**
 *
 * @param {*} file
 * @param {*} cb
 */
var getBinaryLocal = function(file, cb) {
    var fr = new FileReader();
    var p = Promise.defer();

    fr.onprogress = function(e) {
        cb(e.loaded / e.total, e.loaded);
    };
    fr.onload = function(e) {
        p.resolve(new LASFile(e.target.result));
    };

    fr.readAsArrayBuffer(file);

    return p.promise.cancellable().catch(Promise.CancellationError, function(e) {
        fr.abort();
        throw e;
    });
};


export { LASFile };
