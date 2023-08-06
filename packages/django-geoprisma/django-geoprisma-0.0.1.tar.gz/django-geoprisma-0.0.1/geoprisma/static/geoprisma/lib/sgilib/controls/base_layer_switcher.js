var baseLayerSwitcher = new OpenLayers.Control.LayerSwitcher();
OpenLayers.Util.extend(baseLayerSwitcher, {
    /**
     * Method: draw
     *
     * Returns:
     * {DOMElement} A reference to the DIV DOMElement containing the
     *     switcher tabs.
     */
    draw: function() {
        OpenLayers.Control.prototype.draw.apply(this);

        // create layout divs
        this.loadContents();

        // populate div with current info
        this.redraw();

        return this.div;
    },

    /**
     * Method: redraw
     * Goes through and takes the current state of the Map and rebuilds the
     *     control to display that state. Groups base layers into a
     *     radio-button group and lists each data layer with a checkbox.
     *
     * Returns:
     * {DOMElement} A reference to the DIV DOMElement containing the control
     */
    redraw: function() {
        //if the state hasn't changed since last redraw, no need
        // to do anything. Just return the existing div.
        if (!this.checkRedraw()) {
            return this.div;
        }

        //clear out previous layers
        this.clearLayersArray("base");
        this.clearLayersArray("data");

        var containsOverlays = false;
        var containsBaseLayers = false;

        // Save state -- for checking layer if the map state changed.
        // We save this before redrawing, because in the process of redrawing
        // we will trigger more visibility changes, and we want to not redraw
        // and enter an infinite loop.
        var len = this.map.layers.length;
        this.layerStates = new Array(len);
        for (var i=0; i <len; i++) {
            var layer = this.map.layers[i];
            this.layerStates[i] = {
                'name': layer.name,
                'visibility': layer.visibility,
                'inRange': layer.inRange,
                'id': layer.id
            };
        }

        var layers = this.map.layers.slice();
        if (!this.ascending) { layers.reverse(); }
        for(var i=0, len=layers.length; i<len; i++) {
            var layer = layers[i];
            var baseLayer = layer.isBaseLayer;

            if (layer.displayInLayerSwitcher && baseLayer) {

                containsBaseLayers = true;

                // only check a baselayer if it is *the* baselayer, check data
                //  layers if they are visible
                var checked = (layer == this.map.baseLayer);

                // create input element
                var inputElem = document.createElement("input");
                inputElem.id = this.id + "_input_" + layer.name;
                inputElem.name = this.id + "_baseLayers";
                inputElem.type = "radio";
                inputElem.value = layer.name;
                inputElem.checked = checked;
                inputElem.defaultChecked = checked;
                inputElem.style.display = (checked)?'none':'inline';
                inputElem.className = "olButton";
                inputElem._layer = layer.id;
                inputElem._layerSwitcher = this.id;

                if (!baseLayer && !layer.inRange) {
                    inputElem.disabled = true;
                }
                var context = {
                    'inputElem': inputElem,
                    'layer': layer,
                    'layerSwitcher': this
                };
                OpenLayers.Event.observe(inputElem, "mouseup",
                    OpenLayers.Function.bindAsEventListener(this.onInputClick,
                                                            context)
                );

                // create span
                var labelSpan = document.createElement("label");
                labelSpan["for"] = inputElem.id;
                OpenLayers.Element.addClass(labelSpan, "labelSpan olButton");
                labelSpan._layer = layer.id;
                labelSpan._layerSwitcher = this.id;
                labelSpan.style.display = (checked)?'none':'inline';
                labelSpan.innerHTML = layer.name;
                labelSpan.style.verticalAlign = "bottom"
                OpenLayers.Event.observe(labelSpan, "click",
                    OpenLayers.Function.bindAsEventListener(this.onInputClick,
                                                            context)
                );
                // create line break
                var br = document.createElement("br");

				// create image
				var imgElem = document.createElement("img");
				imgElem.id = this.id + "_img_" + layer.name;
                imgElem._layer = layer.id;
                imgElem._layerSwitcher = this.id;
                imgElem.style.display = (checked)?'none':'block';
				imgElem.width = 96;
				imgElem.height = 76;
				imgElem.src = baseUrl + 'images/layers/'+layer.thumbnailImage;
                OpenLayers.Event.observe(imgElem, "click",
                    OpenLayers.Function.bindAsEventListener(this.onInputClick,
                                                            context)
                );

                var groupArray = this.baseLayers;
                groupArray.push({
                    'layer': layer,
                    'inputElem': inputElem,
                    'labelSpan': labelSpan
                });

                var groupDiv = document.createElement("div");
				groupDiv.align = 'center';
			    groupDiv.style.display = (checked)?'none':'block';
				//groupDiv.appendChild(inputElem);
                groupDiv.appendChild(imgElem);
                //groupDiv.appendChild(br);
                groupDiv.appendChild(labelSpan);

                var baseDiv = this.baseLayersDiv;
                baseDiv.appendChild(groupDiv);
            }
        }

        // if no overlays, dont display the overlay label
        this.dataLbl.style.display = (containsOverlays) ? "" : "none";

        // if no baselayers, dont display the baselayer label
        this.baseLbl.style.display = "";

        return this.div;
    },

    /**
     * Method: showControls
     * Hide/Show all LayerSwitcher controls depending on whether we are
     *     minimized or not
     *
     * Parameters:
     * minimize - {Boolean}
     */
    showControls: function(minimize) {

        this.layersDiv.style.display = minimize ? "none" : "";
    },

    /**
     * Method: loadContents
     * Set up the labels and divs for the control
     */
    loadContents: function() {

        //configure main div
        OpenLayers.Element.addClass(this.div, "baseLayerSwitcherFrame");

        OpenLayers.Event.observe(this.div, "mouseup",
            OpenLayers.Function.bindAsEventListener(this.mouseUp, this));
        OpenLayers.Event.observe(this.div, "click",
                      this.ignoreEvent);
        OpenLayers.Event.observe(this.div, "mousedown",
            OpenLayers.Function.bindAsEventListener(this.mouseDown, this));
        OpenLayers.Event.observe(this.div, "dblclick", this.ignoreEvent);

        // layers list div
        this.layersDiv = document.createElement("div");
        this.layersDiv.id = this.id + "_layersDiv";
        OpenLayers.Element.addClass(this.layersDiv, "layersDiv");

        this.baseLbl = document.createElement("div");
        OpenLayers.Element.addClass(this.baseLbl, "baseLbl");

        this.baseLayersDiv = document.createElement("div");
        OpenLayers.Element.addClass(this.baseLayersDiv, "baseLayersDiv");

        this.dataLbl = document.createElement("div");
        this.dataLbl.innerHTML = OpenLayers.i18n("Overlays");
        OpenLayers.Element.addClass(this.dataLbl, "dataLbl");

        this.dataLayersDiv = document.createElement("div");
        OpenLayers.Element.addClass(this.dataLayersDiv, "dataLayersDiv");

        if (this.ascending) {
            this.layersDiv.appendChild(this.baseLbl);
            this.layersDiv.appendChild(this.baseLayersDiv);
            this.layersDiv.appendChild(this.dataLbl);
            this.layersDiv.appendChild(this.dataLayersDiv);
        } else {
            this.layersDiv.appendChild(this.dataLbl);
            this.layersDiv.appendChild(this.dataLayersDiv);
            this.layersDiv.appendChild(this.baseLbl);
            this.layersDiv.appendChild(this.baseLayersDiv);
        }

        this.div.appendChild(this.layersDiv);

        var imgLocation = OpenLayers.Util.getImagesLocation();
        var sz = new OpenLayers.Size(18,18);
    },

    CLASS_NAME: "OpenLayers.Control.BaseLayerSwitcher"
});
map.addControl(baseLayerSwitcher);