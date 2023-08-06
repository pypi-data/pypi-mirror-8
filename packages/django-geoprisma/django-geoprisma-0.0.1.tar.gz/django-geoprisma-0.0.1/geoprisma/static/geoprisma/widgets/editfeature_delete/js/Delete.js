/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Control/DeleteFeature.js
 */

/**
 * Class: OpenLayers.Control.EditFeature_Delete
 *
 * Inherits From:
 *  - <OpenLayers.Control.EditFeature>
 */
OpenLayers.Control.EditFeature_Delete = OpenLayers.Class(OpenLayers.Control.EditFeature, {
    
    /*
        const: i18n_delete_confirm_message
        {String} Delete confirm message
    */
    i18n_delete_confirm_message : "Delete selected features ?",
    
    /**
     * Constructor: OpenLayers.Control.EditFeature_Delete
     * Create a new EditFeature_Delete control.
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
     * Create a DeleteFeature control and assign it to this control.
     *
     * Parameters:
     * layer - {<OpenLayers.Layer.Vector>} The vector layer to assign the
     *                                     DeleteFeature control to.
     */
    setFeatureControl: function(layer) {
        var options = this.featurecontroloptions || {};
        var control;

        control = new OpenLayers.Control.DeleteFeature(
            layer, options);

        this.featurecontrol = control;
        this.map.addControl(control);

        // when the DeleteFeature ctrl is activated, activate THIS Delete
        // ctrl as well
        control.events.register("activate", this, this.activate);
    },

    /**
     * Method: beforeFeaturesDeleted
     * Called when the user triggers the 'beforefeaturesdeleted' event, i.e. on
     * 'del' keypress.  Displays a confirm message to make sure the user
     * really wants to delete the selected features.
     *
     * Parameters:
     * event - {<OpenLayers.Event>} 
     */
    beforeFeaturesDeleted: function (event) {
        return (confirm(this.i18n_delete_confirm_message))
    },

    /**
     * Method: deleteFeatures
     * Called when the user triggers the 'deletefeatures' event, i.e. on
     * 'del' keypress AND confirmed the deletion of features.
     * 
     * The event contains the reference of the features to be deleted (from 
     * the layer's selected features array).
     *
     * Parameters:
     * event - {<OpenLayers.Event>} 
     */
    deleteFeatures: function (event) {
        features = event.features;
        this.commit(features);
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
        if(activated) {
            this.featurecontrol.activate();

            // register delete events (DeleteFeature ctrl)
            this.featurecontrol.events.on({
               "beforefeaturesdeleted": this.beforeFeaturesDeleted,
                scope: this
            });

            this.featurecontrol.events.on({
               "deletefeatures": this.deleteFeatures,
                scope: this
            });
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
        var deactivated = false;
        // the return from the controls is unimportant in this case
        if(OpenLayers.Control.EditFeature.prototype.deactivate.apply(this, arguments)) {
            this.featurecontrol.deactivate();

            // unregister delete events (DeleteFeature ctrl)
            this.featurecontrol.events.un({
               "beforefeaturesdeleted": this.beforeFeaturesDeleted,
                scope: this
            });

            this.featurecontrol.events.un({
               "deletefeatures": this.deleteFeatures,
                scope: this
            });
        }
        return deactivated;
    },

    CLASS_NAME: "OpenLayers.Control.EditFeature_Delete"
});
