import { baseMaps } from './base_maps.js';
import { TimeIntervalControl, QueryDataFormControl, InfoControl, LegendControl } from './controls.js';
import { style } from './rasterStyling.js';
import { colorGrades, grades, countriesUrl } from './constants.js'

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

// Was wenn es keine Länder gibt?
fetch(countriesUrl)
.then((res) => res.json())
.then((json) => formControl.setCountryOptions(json));


function queryData() {
    const formData = new FormData(formControl.form);
    if (!formControl.form.checkValidity()) {
        formControl.form.querySelector(".error").innerHTML = "<span>Bitte alle Felder ausfüllen</span>";
    } else {
        formControl.form.querySelector(".error").innerHTML= "";
    }

    const country = formData.get('country');
    const startDate = formData.get('start-date');
    const endDate = formData.get('end-date');

    const queryUrl = countriesUrl + '/' + country + '?start_date=' + startDate + '&end_date=' + endDate;
    console.log(queryUrl);

    fetch(queryUrl)
        .then((res) => res.json())
        .then(res => {
            // Was bei Änderungen der Datenstruktur?
            const { config, values } = res;
            //console.log(res);
            const dates = values.map(dailyData => dailyData.date);
            const geoJsons = values.map(dailyData => {
                const coValues = JSON.parse(dailyData.data);
                // Features berechen
                // { "type": "Feature", "properties": { "pixel_id": 1.0, "CO": 75.024267662118106, }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 2.5, 49.5 ], [ 2.5, 50.0 ], [ 3.0, 50.0 ], [ 3.0, 49.5 ], [ 2.5, 49.5 ] ] ] } },
                const { lat_min, lat_max, lat_count, lon_min, lon_max, lon_count } = config;

                // const lat_min = 49.5;
                // const lat_max = 51.5
                // const lat_count = 4;
                const lat_inc = (lat_max - lat_min) / lat_count;
                // const long_min = 2.5;
                // const long_max = 6.0;
                // const long_count = 7;
                const lon_inc = (lon_max - lon_min) / lon_count;

                const features = [];
                let coValueIdx = 0;

                for (let lon = lon_min; lon < lon_max; lon += lon_inc) {
                    for (let lat = lat_min; lat < lat_max; lat += lat_inc) {
                        const coordinates = [[lon, lat], [lon, lat + lat_inc], [lon + lon_inc, lat + lat_inc], [lon + lon_inc, lat], [lon, lat]];
                        const feature = {
                            "type": "Feature",
                            "properties": {
                                "CO": coValues[coValueIdx]
                            },
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [coordinates]
                            }
                        };
                        features.push(feature);
                        coValueIdx++;
                    }
                }

                //console.log(features);
                const geoJson = {
                    "type": "FeatureCollection",
                    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
                    "features": features
                };
                return geoJson;
            });
            //console.log(geoJsons);
            console.log(JSON.stringify(geoJsons[0]));
            timeIntervalControl.update(geoJsons, dates, createGeoJsonLayer)
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