import commonjs from 'rollup-plugin-commonjs';
import nodeResolve from 'rollup-plugin-node-resolve';

export default {
    input: 'lib/geojsbuilder.js',
    output: {
        file: 'test/browser/browser.bundle.js',
        format: 'iife',
        exports: 'named',
        name: 'jupyterlab_geojs',
        strict: false,
    },
    plugins: [
        nodeResolve({
            jsnext: false,
            main: true
        }),
        commonjs({})
    ]
}
