// Leaflet plugins such as markercluster attach to a global L, so expose the mutable UMD build first.
import L from 'leaflet/dist/leaflet-src.js';
globalThis.L = L;
export default L;
