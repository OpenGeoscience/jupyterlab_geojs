declare namespace G {

    class Map {
        constructor(element: string | HTMLElement, options?: MapOptions);
    }

    function map(element: string | HTMLElement, options?: MapOptions): Map;
}

declare module 'geojs' {
    export = G;
}