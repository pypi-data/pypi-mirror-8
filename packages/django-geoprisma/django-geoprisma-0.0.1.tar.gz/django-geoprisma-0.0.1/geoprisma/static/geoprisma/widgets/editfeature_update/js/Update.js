/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Control/ModifyFeature.js
 * @requires OpenLayers/Control/SelectFeature.js
 */

/**
 * Class: OpenLayers.Control.EditFeature_Update
 *
 * Inherits From:
 *  - <OpenLayers.Control.EditFeature>
 */
OpenLayers.Control.EditFeature_Update = OpenLayers.Class(OpenLayers.Control.EditFeature, {
    /**
     * APIProperty: editgeom
     * {Boolean} true if you want to be able to edit the geometry with a 
     *           ModifyFeature control, else use a SelectFeature control
     */
    editgeom: true,

    /**
     * Constructor: OpenLayers.Control.EditFeature_Update
     * Create a new EditFeature_Update control.
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
     * Create a ModifyFeature or SelectFeature control and assign it to this
     * control.  The choice of the control depends on this.editgeom property.
     *
     * Parameters:
     * layer - {<OpenLayers.Layer.Vector>} The vector layer to assign the
     *                                     created control to.
     */
    setFeatureControl: function(layer) {
        var options = this.featurecontroloptions || {};
        var control;

        if(this.editgeom === true) {
            control = new OpenLayers.Control.ModifyFeature(
                layer, options);
        } else {
            control = new OpenLayers.Control.SelectFeature(
                layer, options);
        }

        this.featurecontrol = control;
        this.map.addControl(control);

        // when the featurecontrol is activated, activate THIS Update
        // ctrl as well
        control.events.register("activate", this, this.activate);
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

            if(this.editgeom === true) {
                // register before/after/featuremodified events
                // (ModifyFeature ctrl)
                this.layer.events.on({
                   "beforefeaturemodified": this.onModificationStart,
                    scope: this
                });

                this.layer.events.on({
                   "featuremodified": this.onModification,
                    scope: this
                });

                this.layer.events.on({
                   "afterfeaturemodified": this.onModificationEnd,
                    scope: this
                });
            } else {
                // register featureselected events
                // (ModifyFeature ctrl)
                this.layer.events.on({
                   "featureselected": this.onModificationStart,
                    scope: this
                });

                this.layer.events.on({
                   "featureunselected": this.onModificationEnd,
                    scope: this
                });
            }
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

            if(this.editgeom === true){
                // unregister before/after/featuremodified events
                // (ModifyFeature ctrl)
                this.layer.events.un({
                   "beforefeaturemodified": this.onModificationStart,
                    scope: this
                });

                this.layer.events.un({
                   "featuremodified": this.onModification,
                    scope: this
                });

                this.layer.events.un({
                   "afterfeaturemodified": this.onModificationEnd,
                    scope: this
                });
            } else {
                // register featureselected events
                // (ModifyFeature ctrl)
                this.layer.events.un({
                   "featureselected": this.onModificationStart,
                    scope: this
                });

                this.layer.events.un({
                   "featureunselected": this.onModificationEnd,
                    scope: this
                });
            }
        }
        return deactivated;
    },

    CLASS_NAME: "OpenLayers.Control.EditFeature_Update"
});
