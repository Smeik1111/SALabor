import { baseMaps } from './base_maps.js';
import { TimeIntervalControl, QueryDataFormControl, InfoControl, LegendControl } from './controls.js';
import { style } from './rasterStyling.js';
import { colorGrades, grades, url } from './constants.js'

const map = L.map('map',
    {
        center: [50.0, 8.0],
        crs: L.CRS.EPSG3857,
        zoom: 6,
        zoomControl: true,
        preferCanvas: false,
        layers: [baseMaps['CartoDB.Positron']]
    }
);

L.control.layers(baseMaps, null).addTo(map);

const legend = new LegendControl({ position: 'bottomright' });
legend.addTo(map);
legend.setColorPallet(grades, colorGrades)


const info = new InfoControl();
info.addTo(map);

const formControl = new QueryDataFormControl({ position: 'topleft' });
formControl.addTo(map);
formControl.form.addEventListener('queryData', queryData);

const timeIntervalControl = new TimeIntervalControl({ position: 'bottomleft' });
timeIntervalControl.addTo(map);


function queryData() {
    // TODO: Aus querDataForm.from die Parameter auslesen
    formControl.form; // Country, start, end, global
    const formData = {
        "name": name
    };
    // request options
    const options = {
        method: 'POST',
        body: JSON.stringify(formData),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    // send POST request
    fetch(url)
        .then((res) => res.json())
        .then(res => timeIntervalControl.update(res, createGeoJsonLayer))
        .catch(err => console.log(err));
}

function createGeoJsonLayer(geoData) {
    return L.geoJSON(geoData, {
        style: style,
        onEachFeature: (feature, layer) => {
            layer.on({
                mouseover: () => {
                    info.update(layer.feature.properties);
                }
            });
        }
    });
}