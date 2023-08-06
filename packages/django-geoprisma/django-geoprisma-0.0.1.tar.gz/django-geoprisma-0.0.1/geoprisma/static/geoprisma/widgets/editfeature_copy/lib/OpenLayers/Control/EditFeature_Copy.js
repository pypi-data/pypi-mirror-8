/* 
   Copyright (c) 2011 Mapgears inc. , published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Control/ModifyFeature.js
 */

/**
 * Class: OpenLayers.Control.EditFeature_Copy
 *
 * Inherits From:
 *  - <OpenLayers.Control.EditFeature>
 */
OpenLayers.Control.EditFeature_Copy = OpenLayers.Class(OpenLayers.Control.EditFeature, {

    /* API Properties */

    /**
     * APIProperty: offset
     * {String} The **X,Y** offset in pixel units the copied feature should be
     *          moved from its original. Two integer comma-separated values,
     *          first for X second for Y. Negative X means "to the left".
     *          Negative Y means "to the bottom". Example : **-33,47**,
     *          means : "33 pixels to the left and 47 pixels to the top".
     */
    offset: null,

    /**
     * APIProperty: updateControl
     * {<OpenLayers.Control.EditFeature_Update>}
     */
    updateControl: null,

    /**
     * APIProperty: attributes
     * {<Array>} If set, defines the list of attributes to copy.  If not set,
     *           all feature attributes are copied.  If set to an empty array,
     *           then no attributes are copied.
     */
    attributes: null,

    /* Private Properties */

    /**
     * Property: dragControl
     * {<OpenLayers.Control.ModifyFeature>}
     */
    dragControl: null,

    /**
     * Property: offsetX
     * {Integer} Offset in pixel for the X axis.  Negative value means
     *           "to the left"
     */
    offsetX: null,

    /**
     * Property: offsetY
     * {Integer} Offset in pixel for the Y axis.  Negative value means
     *           "to the bottom"
     */
    offsetY: null,
    
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
        if (this.offset) {
            var offsets = this.offset.split(",");
            if (offsets && offsets.length == 2) {
                this.offsetX = parseInt(offsets[0]);
                this.offsetY = parseInt(offsets[1]);
            }
        }
    },

    setMap: function(map) {
        OpenLayers.Control.EditFeature.prototype.setMap.apply(this, arguments);
        this.handlers.feature = new OpenLayers.Handler.Feature(
            this, this.layer, {click: this.cloneFeature});
        this.handlers.feature.setMap(map);
    },

    /**
     * Method: setFeatureControl
     * Create a new OpenLayers.Control.ModifyFeature control and assign it to 
     *     this control.
     *
     * Parameters:
     * layer - {<OpenLayers.Layer.Vector>} The vector layer to assign the
     *                                     created control to.
     */
    setFeatureControl: function(layer) {
        this.dragControl = new OpenLayers.Control.ModifyFeature(layer, {
            mode: OpenLayers.Control.ModifyFeature.DRAG
        });
        this.map.addControl(this.dragControl);

        // in order to support the parent "commit" method, it uses the
        // featurecontrol property
        this.featurecontrol = this.dragControl;
    },

    /**
     * APIMethod: activate
     * Activate the control and the feature handler. Add layer event listeners.
     * 
     * Returns:
     * {Boolean} Successfully activated the control.
     */
    activate: function() {
        var activated = OpenLayers.Control.EditFeature.prototype.activate.apply(this, arguments);
        if (activated) {
            this.handlers.feature.activate();
            this.layer.events.on(this.getLayerEventListeners());
        }        
        return activated;
    },

    /**
     * APIMethod: deactivate
     * Deactivate the control. Remove layer event listeners.
     *
     * Returns: 
     * {Boolean} Successfully deactivated the control.
     */
    deactivate: function() {
        var deactivated = OpenLayers.Control.EditFeature.prototype.deactivate.apply(this, arguments);
        if (deactivated) {
            this.dragControl.deactivate();
            this.layer.events.un(this.getLayerEventListeners());
        }
        return deactivated;
    },

   /**
     * Method: getLayerEventListeners
     * Returns: 
     * {Object} The events to add/remove listeners for this control
     */
    getLayerEventListeners: function() {
        var listeners;
        if (this.updateControl) {
            listeners = {
                "afterfeaturemodified": this.delegateToEditFeature_Update,
                scope: this
            }
        } else {
            listeners = {
                "beforefeaturemodified": this.onModificationStart,
                "afterfeaturemodified": this.onModificationEnd,
                scope: this
            }
        }
        return listeners;
    },

   /**
     * Method: delegateToEditFeature
     * Used to delegate the editing to the updateControl.
     * 
     * Parameters:
     * {Object} The feature that had modifications
     */
    delegateToEditFeature_Update: function(object) {
        var feature = (object.geometry) ? object : object.feature;
        this.updateControl.activate();
        this.updateControl.getSelectControl().select(feature);
    },

   /**
     * Method: cloneFeature
     * Feature handler callback method.  Used to clone the clicked feature, then
     *     select it for dragging purpose.  If an offset is set, the clone will
     *     be moved to its location.
     * 
     * Parameters:
     * feature - {OpenLayers.Feature.Vector} The feature clicked
     */
    cloneFeature: function(feature) {
        var clone = feature.clone();

        // attribute copying management
        if (this.attributes && Ext.isArray(this.attributes)) {
            var copyAttributes = this.attributes.slice();
            var index;
            for (var key in clone.attributes) {
                index = copyAttributes.indexOf(key);
                if (index == -1) {
                    // attribute was not found, so erase its clone value
                    clone.attributes[key] = null;
                } else {
                    // attribute found, keep value and remove it from search
                    copyAttributes.splice(index, 1);
                }
            }
        }

        clone.state = OpenLayers.State.INSERT;
        feature.layer.addFeatures([clone]);

        if (this.offsetX && this.offsetY) {
            var resolution = this.map.getResolution();
            var px = this.map.getViewPortPxFromLonLat(
                clone.geometry.getBounds().getCenterLonLat()
            );
            px.x += this.offsetX;
            px.y -= this.offsetY;
            clone.move(px);
        }

        this.toggleFeatureHandler(false);
        this.dragControl.selectControl.select(clone);
    },

    /**
     * Method: onModificationEnd
     * Call parent onModificationEnd and re-enable feature handler.
     */
    onModificationEnd: function(object) {
        var superProto = OpenLayers.Control.EditFeature.prototype;
        superProto.onModificationEnd.apply(this, arguments);
        this.toggleFeatureHandler(true);
    },

    /**
     * Method: toggleFeatureHandler
     * 
     * Parameters:
     * toggle - {boolean} true : enables feature handler and deactivate drag
     *                    control, false is the opposite.
     */
    toggleFeatureHandler: function(toggle) {
        if (toggle) {
            this.dragControl.deactivate();
            this.handlers.feature.activate();
        } else {
            this.handlers.feature.deactivate();
            this.dragControl.activate();
        }
    },

    CLASS_NAME: "OpenLayers.Control.EditFeature_Copy"
});
