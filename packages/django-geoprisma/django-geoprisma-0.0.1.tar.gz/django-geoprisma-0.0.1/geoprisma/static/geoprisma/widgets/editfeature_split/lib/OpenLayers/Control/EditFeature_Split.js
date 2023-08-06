/* 
   Copyright (c) 2011 Mapgears inc. , published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Control/SplitFeature.js
 * @requires OpenLayers/Control/ModifyFeature.js
 */

/**
 * Class: OpenLayers.Control.EditFeature_Split
 *
 * Inherits From:
 *  - <OpenLayers.Control.EditFeature>
 */
OpenLayers.Control.EditFeature_Split = OpenLayers.Class(OpenLayers.Control.EditFeature, {

    /* i18n start */

    /* i18n end */

    /**
     * APIProperty: splitWindow
     * {<Ext.Window>} The window to open after spliting features
     */
    splitWindow: null,

    /**
     * Property: splitControl
     * {<OpenLayers.Control.SplitFeature>}
     */
    splitControl: null,

    /**
     * Property: splitFeatures
     * {Array} Is populated with an hash of original + split features on each
     *         split event triggered.
     */
    splitFeatures: null,

    
    /**
     * Constructor: OpenLayers.Control.EditFeature_Split
     * Create a new EditFeature_Split control.
     *
     * Parameters:
     * options - {Object} Optional object whose properties will be set on the
     *     control.
     */
    initialize: function(options) {
        OpenLayers.Control.EditFeature.prototype.initialize.apply(this, [options]);
        this.splitFeatures = [];
        if (this.splitWindow) {
            this.splitWindow.editfeature_split = this;
        }
    },

    /**
     * Method: setFeatureControl
     * Create a new OpenLayers.Contro.Split control and assign it to this
     * control.
     *
     * Parameters:
     * layer - {<OpenLayers.Layer.Vector>} The vector layer to assign the
     *                                     created control to.
     */
    setFeatureControl: function(layer) {
        var Split = OpenLayers.Class(OpenLayers.Control.Split, {
            initialize: function(options) {
                Array.prototype.push.apply(
                    this.EVENT_TYPES, ["sketchcomplete"]
                );
                OpenLayers.Control.Split.prototype.initialize.apply(
                    this, [options]
                );
            },
            onSketchComplete: function(event) {
                this.events.triggerEvent("sketchcomplete")
                var superProto = OpenLayers.Control.Split.prototype;
                superProto.onSketchComplete.apply(this, arguments);
            }
        });

        this.splitControl = new Split({
            layer: layer,
            eventListeners: {
                sketchcomplete: this.sketchComplete,
                split: this.split,
                aftersplit: this.afterSplit,
                scope: this
            }
        });
        this.map.addControl(this.splitControl);

        // in order to support the parent "commit" method, it uses the
        // featurecontrol property
        this.featurecontrol = this.splitControl;
    },

    /**
     * APIMethod: activate
     * Activate the control.
     * 
     * Returns:
     * {Boolean} Successfully activated the control.
     */
    activate: function() {
        var activated = OpenLayers.Control.EditFeature.prototype.activate.apply(this, arguments);
        if (activated) {
            this.splitControl.activate();
        }        
        return activated;
    },

    /**
     * APIMethod: deactivate
     * Deactivate the control.
     *
     * Returns: 
     * {Boolean} Successfully deactivated the control.
     */
    deactivate: function() {
        var deactivated = OpenLayers.Control.EditFeature.prototype.deactivate.apply(this, arguments);
        if (deactivated) {
            this.cancel();
            this.splitControl.deactivate();
        }
        return deactivated;
    },

    sketchComplete: function(event) {
        this.splitFeatures = [];
    },

    split: function(event) {
        this.splitFeatures.push({
            original: event.original,
            features: event.features
        });
    },

    afterSplit : function(event) {
        if (this.splitWindow) {
            this.splitWindow.show();
        }
    },

    cancel: function() {
        var layer = this.splitControl.layer;
        // cancel by refreshing the layer, make sure it's visible.  If not,
        // make it visible first, then hide it.
        var layerVisible = layer.visibility;
        !layerVisible && layer.setVisibility(true);
        layer.refresh({force: true});
        !layerVisible && layer.setVisibility(false);
        this.splitWindow && this.splitWindow.hide();
    },

    flashFeatures: function(features, index) {
        if(!index) {
            index = 0;
        }
        var current = features[index];
        if(current && current.layer === this.layer) {
            this.layer.drawFeature(features[index], "select");
        }
        var prev = features[index-1];
        if(prev && prev.layer === this.layer) {
            this.layer.drawFeature(prev, "default");
        }
        ++index;
        if(index <= features.length) {
            window.setTimeout(function() {
                this.flashFeatures(features, index)
            }, 200);
        }
    },

    CLASS_NAME: "OpenLayers.Control.EditFeature_Split"
});
