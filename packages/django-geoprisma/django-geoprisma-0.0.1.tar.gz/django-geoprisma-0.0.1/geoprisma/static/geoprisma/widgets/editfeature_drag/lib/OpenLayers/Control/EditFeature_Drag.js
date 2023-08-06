/* 
   Copyright (c) 2011 Mapgears inc. , published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Control/DragFeature.js
 * @requires OpenLayers/Control/ModifyFeature.js
 */

/**
 * Class: OpenLayers.Control.EditFeature_Drag
 *
 * Inherits From:
 *  - <OpenLayers.Control.EditFeature>
 */
OpenLayers.Control.EditFeature_Drag = OpenLayers.Class(OpenLayers.Control.EditFeature, {

    /* API Properties */

    /**
     * APIProperty: updateControl
     * {<OpenLayers.Control.EditFeature_Update>} When set, this widget won't
     *     
     */
    updateControl: null,

    /* Private Properties */

    /**
     * Property: dragControl
     * {<OpenLayers.Control.ModifyFeature>}
     */
    dragControl: null,
    
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
     * Activate the control. Add layer event listeners.
     * 
     * Returns:
     * {Boolean} Successfully activated the control.
     */
    activate: function() {
        var activated = OpenLayers.Control.EditFeature.prototype.activate.apply(this, arguments);
        if (activated) {
            this.dragControl.activate();
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
                "beforefeaturemodified": this.onBeforeFeatureModified,
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
     * Method: onBeforeFeatureModified
     * Called on layer "beforefeaturemodified" event triggered.  Clone the
     *     feature for cancelling purpose.
     *
     * Parameters:
     * object - {<OpenLayers.Event>} The event containing the feature
     */
    onBeforeFeatureModified: function(object) {
        var feature = (object.geometry) ? object : object.feature;
        if(feature.state != OpenLayers.State.INSERT){
            feature.myClone = feature.clone();
            feature.myClone.fid = feature.fid;
        }
    },

   /**
     * Method: delegateToEditFeature
     * Used to delegate the editing to the updateControl.
     * 
     * Parameters:
     * object - {Object} The feature that had modifications
     */
    delegateToEditFeature_Update: function(object) {
        var feature = (object.geometry) ? object : object.feature;
        this.updateControl.activate();
        this.updateControl.getSelectControl().select(feature);
    },

    CLASS_NAME: "OpenLayers.Control.EditFeature_Drag"
});
