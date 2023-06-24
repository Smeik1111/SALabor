import { baseMaps } from '../base_maps.js';
import { TimeIntervalControl, QueryDataFormControl, InfoControl, LegendControl } from '../controls.js';
import { style } from '../rasterStyling.js';
import { colorGrades, grades, countriesUrl } from '../constants.js'

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
    formControl.form;

    // Country, start, end, global
    const country = 'canada';
    const startDate = '2023-05-30';
    const endDate = '2023-05-31';

    //Y

    const queryUrl = countriesUrl + '/' + country + '?start_date=' + startDate + '&end_date=' + endDate;
    console.log(queryUrl);
    // request options
    const options = {
        method: 'POST',
    };
    // send POST request
    fetch(queryUrl)
        .then((res) => res.json())
        .then(res => {
            if (res) {
                // TODO: Keine Daten! => Dann Land anfrangen!
            }
            const geoJsons = res.map(dailyData => {
                const date = dailyData.date;
                const coValues = dailyData.data;
                console.log(coValues);

                // Features berechen
                // { "type": "Feature", "properties": { "pixel_id": 1.0, "CO": 75.024267662118106, }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 2.5, 49.5 ], [ 2.5, 50.0 ], [ 3.0, 50.0 ], [ 3.0, 49.5 ], [ 2.5, 49.5 ] ] ] } },
                const lat_min = 49.5;
                const lat_max = 51.5
                const lat_count = 4;
                const lat_inc = (lat_max - lat_min) / lat_count;
                const long_min = 2.5;
                const long_max = 6.0;
                const long_count = 7;
                const long_inc = (long_max - long_min) / long_count;

                const features = [];
                let coValueIdx = 0;

                for (let long = long_min; long < long_max; long += long_inc) {
                    for (let lat = lat_min; lat < lat_max; lat += lat_inc) {
                        const coordinates = [[long, lat], [long, lat + lat_inc], [long + long_inc, lat + lat_inc], [long + long_inc, lat], [long, lat]];
                        const feature = {
                            "type": "Feature",
                            "properties": {
                                "CO": coValues[coValueIdx]
                            },
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": coordinates
                            }
                        };
                        features.push(feature);
                        coValueIdx++;
                    }
                }

                console.log(features);
                const geoJson = {
                    "type": "FeatureCollection",
                    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
                    "features": features
                };
                return geoJson;
            });
            //timeIntervalControl.update(res, createGeoJsonLayer)
        })
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