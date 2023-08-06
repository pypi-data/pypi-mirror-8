Ext.namespace("GeoExt.data")

GeoExt.data.PrintProvider && Ext.apply(GeoExt.data.PrintProvider.prototype, {

    /* i18n text START */
    unsuportedText: "Some layers currently visible on the map are not supported by the print service",
    
    excludedText: "They would be excluded from the document.",
    
    proceedAnywayText: "Do you wish to proceed anyway ?",
    
    turnLayersOffText: "Please, turn them off first.",
    
    tileCacheWMSUnsuportedText: "TileCache using WMS requests",

    activeDrawFeatureControlText: "There's currently an active drawing control.  Please, turn it off first.",
    /* i18n text END */

    /**
     * Method: beforePrint
     * Checks if there are unsuppored layers currently visible on map and
     * ask the user what to do about them.
     *
     * Parameters:
     * printProvider {<GeoExt.data.PrintProvider>}
     * map           {<OpenLayers.Map>}
     * pages         {Array}
     * options       {Object}
     *
     * Returns:
     * {Boolean}
     */
    beforePrint: function(printProvider, map, pages, options) {
        pages = pages instanceof Array ? pages : [pages];
        options = options || {};
 
        var pagesLayer = pages[0].feature.layer;
        var unLayers = []; // unsupported layers
        var classNamePrefix = "OpenLayers.Layer.";
        var prefixLen = classNamePrefix.length;
        var canPrint = true;

        var activeDrawControl;
        Ext.each(map.controls, function(control){
            if (control instanceof OpenLayers.Control.DrawFeature &&
                control.active) {
                activeDrawControl = true;
                return false;
            }
        }, this);

        if (activeDrawControl) {
            alert(this.activeDrawFeatureControlText);
            return false;
        }
        
        Ext.each(map.layers, function(layer){
            if(layer !== pagesLayer && layer.getVisibility() === true) {
                // Vector layers used by handlers mustn't be added...
                if (layer instanceof OpenLayers.Layer.Vector) {
                    if (layer.name === "OpenLayers.Handler.Point" ||
                        layer.name === "OpenLayers.Handler.Path" ||
                        layer.name === "OpenLayers.Handler.Polygon") {
                        return true;
                    }
                } else {
                    var enc = this.encodeLayer(layer);
                    if (!enc) {
                        var suffix = layer.CLASS_NAME.substr(prefixLen);
                        if (OpenLayers.Util.indexOf(unLayers, suffix) == -1) {
                            unLayers.push(suffix);
                        }
                    }
                }
            }
        }, this);

        if (unLayers.length > 0) {
            return this.showUnsupportedLayers(unLayers, canPrint);
        } else {
            return true;
        }
    },

    /**
     * Method: showUnsupportedLayers
     * Show the user the unsupported layer types and ask the user what to do
     * about them.
     *
     * Parameters:
     * unsupportedLayers {Array} Array of unsupported layers to show to the user
     * canPrint          {Boolean} Whether the user can print anyway or not
     *
     * Returns:
     * {Boolean}
     */
    showUnsupportedLayers: function(unsupportedLayers, canPrint) {
        var text = this.unsuportedText + " : \n" + unsupportedLayers.join(", ") + "\n";
        text += (canPrint) ? this.excludedText + " " + this.proceedAnywayText : this.turnLayersOffText;

        if (canPrint) {
            return confirm(text);
        } else {
            alert (text);
            return false;
        }
    }
});
