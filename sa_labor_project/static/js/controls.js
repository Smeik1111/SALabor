export const TimeIntervalControl = L.Control.extend({
    layers: undefined,
    currLayer: undefined,
    map: undefined,
    container: undefined,
    slider: undefined,
    playBtn: undefined,
    dateInfoLine: undefined,

    onAdd(map) {
        this.map = map;
        this.container = L.DomUtil.create('div', 'timeIntervalContainer control');

        this.playBtn = L.DomUtil.create('button', 'btn playBtn');
        this.playBtn.innerHTML = "▶️";
        this.playBtn.title = "Play";
        this.playBtn.addEventListener('click', () => this._play());
        this.playBtn.disabled = true;

        this.slider = L.DomUtil.create('input', 'timeIntervalSlider');
        this.slider.min = 0;
        this.slider.type = 'range';
        this.slider.disabled = true;

        this.slider.addEventListener('click', () => this._slide());
        const controlsContainer = L.DomUtil.create('div', 'timeIntervalontrolsContainer');
        controlsContainer.appendChild(this.playBtn);
        controlsContainer.appendChild(this.slider);

        this.dateInfoLine = L.DomUtil.create('div', 'dates')

        this.container.appendChild(controlsContainer)
        this.container.appendChild(this.dateInfoLine);
        L.DomEvent.disableClickPropagation(this.container);
        return this.container;
    },

    update(datasets, createLayer) {
        //console.log('datasets ' + JSON.stringify(datasets));
        if (!datasets || datasets.length === 0) {
            console.error('No geojson datasets');
            return;
        }
        let dates = datasets.map(geo => geo.date).filter(date => date);
        if (!dates ||dates.length === 0) dates = Array(datasets.length).fill().map((element, index) => "Tag " + (index + 1))
        console.log(dates);

        if (this.currLayer) this.currLayer.remove();
        this.currLayer = undefined;
        this.layers = datasets.map(createLayer);

        this._nextLayer(this.layers[0]);
        this.slider.disabled = false;
        this.playBtn.disabled = false;
        this.slider.value = 0;

        if (dates.length === 1) this.dateInfoLine.innerHTML = `<span>${dates[0]}</span>`
        else {
            this.slider.max = dates.length - 1;
            this.dateInfoLine.innerHTML = dates[0] + " - " + dates[dates.length - 1];
        }
    },

    _slide() {
        const idx = this.slider.value;
        if (idx < this.layers.length) this._nextLayer(this.layers[idx]);
        else console.error('No data for slider value: ' + this.slider.value)
    },

    // Annhame: Das erste Bild wird schon angezeigt
    _play() {
        const start = this.slider.value >= this.layers.length - 1 ? 0 : this.slider.value;
        for (let i = start; i < this.layers.length; i++) {
            setTimeout(() => {
                console.log('next');
                this._nextLayer(this.layers[i])
                this.slider.value = i;
            }, 1000 * (i + 1));

        }
        //else console.error('No data for slider value: ' + this.slider.value)
    },

    _nextLayer(nextLayer) {
        if (this.currLayer) this.currLayer.remove();
        this.currLayer = nextLayer;
        this.currLayer.addTo(this.map);
    }
});

export const QueryDataFormControl = L.Control.extend({
    form: undefined,

    onAdd: function (map) {
        const div = L.DomUtil.create('div', 'control');
        L.DomEvent.disableClickPropagation(div);

        const countryInputContainer = L.DomUtil.create('div', 'inputFieldContainer');
        countryInputContainer.innerHTML = `
            <label for="country">Land</label>
            <select name="Land" id="country">
                <option value="germany">Deutschland</option>
                <option value="china">China</option>
            </select>
        `;
        const startInputContainer = L.DomUtil.create('div', 'inputFieldContainer');
        startInputContainer.innerHTML = `
            <label for="start">Von</label>
            <input type="date" id="start" name="data-start" value="2023-04-01" min="2023-04-01" max="2023-04-30"/>
        `;
        const endInputContainer = L.DomUtil.create('div', 'inputFieldContainer');
        endInputContainer.innerHTML = `
            <label for="end">Bis</label>
            <input type="date" id="end" name="data-end" value="2023-04-02" min="2023-04-01" max="2023-04-30"/>
        `;
        const queryContainer = L.DomUtil.create('div', 'inputFieldContainer');

        const queryBtn = L.DomUtil.create('input');
        queryBtn.type = 'button';
        queryBtn.value = 'Daten anfragen';
        queryBtn.addEventListener('click', this._createQueryDataEvent);
        queryContainer.appendChild(queryBtn);

        this.form = L.DomUtil.create('form', 'queryDataForm');
        this.form.appendChild(countryInputContainer)
        this.form.appendChild(startInputContainer)
        this.form.appendChild(endInputContainer)
        this.form.appendChild(queryContainer);

        div.appendChild(this.form);
        return div;
    },
    _createQueryDataEvent() {
        this.dispatchEvent(
            new CustomEvent("queryData", {
                bubbles: true,
                detail: { text: () => textarea.value },
            })
        );
    }
});


export const InfoControl = L.Control.extend({
    onAdd(map) {
        this._div = L.DomUtil.create('div', 'infobox control');
        L.DomEvent.disableClickPropagation(this._div);
        this.update();
        return this._div;
    },
    update(props) {
        this._div.innerHTML = '<h4>Tropospheric CO</h4>' + (props ?
            props.CO + ' [Pmol/cm2]' : 'Lade Daten und hovere über</br>einen eingefärbten Bereich');
    }
});


export const LegendControl = L.Control.extend({
    colorPallet: undefined,
    onAdd(map) {
        this.colorPallet = L.DomUtil.create('div', 'legend control');
        L.DomEvent.disableClickPropagation(this.colorPallet);
        return this.colorPallet;
    },

    setColorPallet(grades, colors) {
        this.colorPallet.innerHTML = '';
        for (let i = 0; i < grades.length; i++) {
            this.colorPallet.innerHTML +=
                '<div>' +
                '<i style="background:' + colors[i] + '"></i> ' +
                grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+') +
                '</div>';
        }
    }
});