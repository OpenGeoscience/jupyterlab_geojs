// VTK JS import
import vtkjsPackage from 'vtk.js/package.json';
console.log(`Using vtk.js version ${vtkjsPackage.version}`);

import vtkPolyData from 'vtk.js/Sources/Common/DataModel/PolyData';
import vtkMapper from 'vtk.js/Sources/Rendering/Core/Mapper';
import vtkActor from 'vtk.js/Sources/Rendering/Core/Actor';
import vtkPoints from 'vtk.js/Sources/Common/Core/Points';
import vtkCellArray from 'vtk.js/Sources/Common/Core/CellArray';
import vtkDataArray from 'vtk.js/Sources/Common/Core/DataArray';
import vtkOpenGLRenderWindow from 'vtk.js/Sources/Rendering/OpenGL/RenderWindow';
import vtkRenderWindowInteractor from 'vtk.js/Sources/Rendering/Core/RenderWindowInteractor';
import vtkRenderWindow from 'vtk.js/Sources/Rendering/Core/RenderWindow';
import vtkRenderer from 'vtk.js/Sources/Rendering/Core/Renderer';

/**
 * An object that manages a bunch of particle systems
 */
var ParticleSystem = function() {
    this.pss = []; // particle systems in use

    this.mx = null;
    this.mn = null;
    this.cg = null;
    this.cn = null;
    this.cx = null;
    this.in_x = null;
    this.in_y = null;
    this.klass = null;
    this.pointsSoFar = 0;
    this.zrange = null;

    this.renderer = null;
    this.renderWindow = null;
};

/**
 *
 */
ParticleSystem.prototype.push = function(lasBuffer) {
    var count = lasBuffer.pointsCount,
        p, z,
        cg = null,
        mx = null,
        mn = null,
        cn = null,
        cx = null,
        in_x = null,
        in_n = null,
        klass = null;

    var pointBuffer = new Float32Array(count * 3);
    var cellBuffer = new Int32Array(count+1);
    var scalarBuffer = new Float32Array(count);
    cellBuffer[0] = count;
    var maxz, minz;

    if (this.zrange) {
        minz = this.zrange[0];
        maxz = this.zrange[1];
    }
    else {
        // Autoscale
        for ( var i = 0; i < count; i ++) {
            p = lasBuffer.getPoint(i);
            z = p.position[2] * lasBuffer.scale[2] +
                        (lasBuffer.offset[2] - lasBuffer.mins[2]);
            if (maxz === undefined) {
                maxz = z;
                minz = z;
            } else {
                if (z > maxz) {
                    maxz = z;
                }
                if (z < minz) {
                    minz = z;
                }
            }  // (else)
        }  // for (i)
    }


    for ( var i = 0; i < count; i ++) {
        var p = lasBuffer.getPoint(i);

        pointBuffer[i*3]   = p.position[0] * lasBuffer.scale[0] +
            (lasBuffer.offset[0] - lasBuffer.mins[0]);
        pointBuffer[i*3+1] = p.position[1] * lasBuffer.scale[1] +
            (lasBuffer.offset[1] - lasBuffer.mins[1]);
        pointBuffer[i*3+2] = p.position[2] * lasBuffer.scale[2] +
            (lasBuffer.offset[2] - lasBuffer.mins[2]);

        cellBuffer[i+1] = i;
        scalarBuffer[i] = (pointBuffer[i*3+2] - minz)/(maxz - minz);
    }

    // Dump first and last points:
    // let n = 0;
    // console.log(`pointBuffer[${n}]`);
    // let coords_list = [];
    // for (let i=0; i<3; ++i) {
    //   let s = Number(pointBuffer[n+i]).toFixed(2);
    //   coords_list.push(s);
    // }
    // let coords_string = coords_list.join(',');
    // console.log(`Point ${n}: (${coords_string})`);

    // coords_list = [];
    // n = 3*(count - 1);
    // for (let i=0; i<3; ++i) {
    //   let s = Number(pointBuffer[n+i]).toFixed(2);
    //   coords_list.push(s);
    // }
    // coords_string = coords_list.join(',');
    // console.log(`Point ${count-1}: (${coords_string})`);

    const polydata = vtkPolyData.newInstance();
    polydata.getPoints().setData(pointBuffer, 3);
    polydata.getVerts().setData(cellBuffer);

    const dataarray = vtkDataArray.newInstance({values:scalarBuffer, name: 'data'});
    polydata.getPointData().setScalars(dataarray);

    this.pss.push(polydata);

    this.pointsSoFar += count;
    //console.log(`Loaded ${count} points into the particle system`);
};

/**
 *
 */
ParticleSystem.prototype.normalizePositionsWithOffset = function(offset) {
    var _this = this;

    var off = offset.clone();

    this.correctiveOffset = off.clone().sub(_this.corrective);
    this.cg.sub(off);
    this.mn.sub(off);
    this.mx.sub(off);
};

/**
 *
 */
ParticleSystem.prototype.init = function(elem) {
    if (!this.renderer) {
        this.renderer = vtkRenderer.newInstance({ background: [0.1, 0.1, 0.1] });;
        this.openglRenderWindow = vtkOpenGLRenderWindow.newInstance();
        this.renderWindow = vtkRenderWindow.newInstance();
        this.renderWindow.addRenderer(this.renderer);
        this.renderWindow.addView(this.openglRenderWindow);

        this.openglRenderWindow.setContainer(elem);

        const interactor = vtkRenderWindowInteractor.newInstance();
        interactor.setView(this.openglRenderWindow);
        interactor.initialize();
        interactor.bindEvents(elem);
    }
}

/**
 * Render particle system using vtk.js
 */
ParticleSystem.prototype.setZRange = function(zmin, zmax) {
    if (!this.zrange) {
        this.zrange = new Array(2);
    }
    this.zrange[0] = zmin;
    this.zrange[1] = zmax;
}

/**
 * Render particle system using vtk.js
 */
ParticleSystem.prototype.render = function(firstTime) {
    if (firstTime) {
        for (var i = 0; i < this.pss.length; ++i) {
            const actor = vtkActor.newInstance();
            actor.getProperty().setPointSize(5);
            const mapper = vtkMapper.newInstance();
            mapper.setInputData(this.pss[i]);
            actor.setMapper(mapper);
            this.renderer.addActor(actor);
        }

        this.renderer.resetCamera();
    }

    this.renderWindow.render();
}

/**
 * Handle window resize
 */
ParticleSystem.prototype.resize = function(elem) {
    const dims = elem.getBoundingClientRect();
    const windowWidth = Math.floor(dims.width);
    const windowHeight = Math.floor(dims.height);
    this.openglRenderWindow.setSize(windowWidth, windowHeight);
    this.render();
}

ParticleSystem.prototype.destroy = function() {
    if (!this.renderer) {  // never initialized
        return;
    }

    // Delete actors
    let actors = this.renderer.getActors();
    for (let actor of actors) {
        this.renderer.removeActor(actor);
        actor.delete();
    }

    this.renderWindow.delete();
    this.renderer.delete();
}

export { ParticleSystem };
