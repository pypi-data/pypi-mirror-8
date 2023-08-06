/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Control/SelectFeature.js
 * @requires OpenLayers/Handler/Keyboard.js
 */

/**
 * Class: OpenLayers.Control.DeleteFeature
 * Control to delete features.  When activated, a SelectFeature control is
 *     activated to select the features to be deleted.  On select, the feature
 *     state are set to DELETE.  When the user is ready to commit, he can press
 *     the 'del' key.  That triggers a 'deletefeatures' event with the features
 *     selected.  The user then need to register a listener on this event to 
       handle the actual delete command (protocol.commit for example).
 *
 * Inherits From:
 *  - <OpenLayers.Control>
 */
OpenLayers.Control.DeleteFeature = OpenLayers.Class(OpenLayers.Control, {
    /**
     * Constant: EVENT_TYPES
     * {Array(String)} Supported application event types.  Register a listener
     *     for a particular event with the following syntax:
     * (code)
     * control.events.register(type, obj, listener);
     * (end)
     *
     *  - *beforefeaturesdeleted* Triggered before features are deleted.  Can
     *      be used to
     *  - *deletefeatures* Triggered 
     */
    EVENT_TYPES: ["beforefeaturesdeleted","deletefeatures"],

    /**
     * APIProperty: multiple
     * {Boolean} Allow selection of multiple geometries.  Default is false.
     */
    multiple: false, 

    /**
     * APIProperty: clickout
     * {Boolean} Unselect features when clicking outside any feature.
     *     Default is true.
     */
    clickout: true,

    /**
     * APIProperty: toggle
     * {Boolean} Unselect a selected feature on click.
     *      Default is true.
     */
    toggle: true,

    /**
     * APIProperty: box
     * {Boolean} Allow feature selection by drawing a box.
     */
    box: false,

    /**
     * APIProperty: unselectAllOnCancel
     * {Boolean} Unselect all features if "beforefeaturesdeleted" returns false.
     */
    unselectAllOnCancel: true,

    /**
     * Property: layer
     * {<OpenLayers.Layer.Vector>}
     */
    layer: null,

    /**
     * Property: selectControl
     * {<OpenLayers.Control.SelectFeature>}
     */
    selectControl: null,

    /**
     * Property: handlers
     * {Object}
     */
    handlers: null,

    /**
     * APIProperty: deleteCodes
     * {Array(Integer)} Keycodes for deleting features.  Set to null to disable
     *     feature deltion by keypress.  If non-null, keypresses with codes
     *     in this array will delete features in this.features array. Default
     *     is 46 and 68, the 'delete' and lowercase 'd' keys.
     */
    deleteCodes : null,

    /**
     * APIProperty: unselectAllCodes
     * {Array(Integer)} Keycodes for unselecting all features.  Set to null to
     *     disable feature unselection by keypress.  If non-null, keypresses
     *     with codes in this array will unselect features in this.features
     *     array. Default is 27, the 'esc' key.
     */
    //unselectAllCodes : null,

    /**
     * Constructor: OpenLayers.Control.DeleteFeature
     * Create a new delete feature control.
     *
     * Parameters:
     * layer - {<OpenLayers.Layer.Vector>} Layer that contains features that
     *     will be deleted.
     * options - {Object} Optional object whose properties will be set on the
     *     control.
     */
    initialize: function(layer, options) {
        // concatenate events specific to this control with those from the base
        this.EVENT_TYPES =
            OpenLayers.Control.DeleteFeature.prototype.EVENT_TYPES.concat(
            OpenLayers.Control.prototype.EVENT_TYPES
        );

        this.layer = layer;
        this.deleteCodes = [46]; // 'del' key only
        //this.unselectAllCodes = [27]; // 'esc' key

        OpenLayers.Control.prototype.initialize.apply(this, [options]);

        if(!(this.deleteCodes instanceof Array)) {
            this.deleteCodes = [this.deleteCodes];
        }
        if(!(this.unselectAllCodes instanceof Array)) {
            this.unselectAllCodes = [this.unselectAllcodes];
        }

        // configure the select control
        var selectOptions = {
            clickout: this.clickout,
            toggle: this.toggle,
            multiple: this.multiple,
            box: this.box,
            toggleKey: "ctrlKey",
            multipleKey: "shiftKey",
            onSelect: this.selectFeature,
            onUnselect: this.unselectFeature,
            scope: this
        };
        this.selectControl = new OpenLayers.Control.SelectFeature(
            layer, selectOptions
        );

        // configure the keyboard handler
        var keyboardOptions = {
            keydown: this.handleKeypress
        };
        this.handlers = {
            keyboard: new OpenLayers.Handler.Keyboard(this, keyboardOptions)
        };
    },

    /**
     * Method: selectFeature
     * When a feature is selected by this control, set the state to DELETE.
     * Draw the feature again with its new state.
     *
     * Parameters:
     * feature - {OpenLayers.Feature.Vector}
     */
    selectFeature: function(feature){
        feature.state = OpenLayers.State.DELETE;
        this.layer.drawFeature(feature);
    },

    /**
     * Method: unselectFeature
     * When a feature is unselected by this control, reset the state to null.
     *
     * Parameters:
     * feature - {OpenLayers.Feature.Vector}
     */
    unselectFeature: function(feature){
        feature.state = null;
    },

    /**
     * Method: handleKeypress
     * Called by the feature handler on keypress.  This is used to trigger
     * 2 kinds of events :
     *   - delete the selected features (on 'del' or 'd' keypress)
     *   - unselect the selected features (on 'esc' keypress)
     *
     * Parameters:
     * {Integer} Key code corresponding to the keypress event.
     */
    handleKeypress: function(evt) {
        var code = evt.keyCode;
        var features = this.layer.selectedFeatures;

        var delKey = OpenLayers.Util.indexOf(this.deleteCodes, code) != -1;
        if(delKey && features && features.length > 0) {
            this.deleteFeatures();
            return;
        }

/*
        var escKey = OpenLayers.Util.indexOf(this.unselectAllCodes, code) != -1;
        if(escKey){
            this.selectControl.unselectAll();
        }
*/
    },

    /**
     * Method: deleteFeatures
     * Trigger "beforefeaturesdeleted" and "deletefeatures" events with 
     * layer selected features as features to delete.
     * 
     * options - {Object}
     *     if {silent: true}, the function will skip the beforefeaturesdeleted
     *     and trigger deletefeatures
     */
    deleteFeatures: function (options){
        var silent = options && options.silent;
        var ret;
        var event = {features: this.layer.selectedFeatures};
        
        if (!silent){
            ret = this.events.triggerEvent("beforefeaturesdeleted", event);
        } else {
            ret = true;
        }

        if(ret === true) {
            this.events.triggerEvent("deletefeatures", event);
        } else if (this.unselectAllOnCancel){
            this.selectControl.unselectAll();
        }
    },

    /**
     * Method: setMap
     * Set the map property for the control and all handlers.
     *
     * Parameters:
     * map - {<OpenLayers.Map>} The control's map.
     */
    setMap: function(map) {
        this.selectControl.setMap(map);
        this.handlers.keyboard.setMap(map);
        OpenLayers.Control.prototype.setMap.apply(this, arguments);
    },

    /**
     * Method: activate
     * Explicitly activates a control and it's associated
     * handlers if one has been set.  Controls can be
     * deactivated by calling the deactivate() method.
     * 
     * Returns:
     * {Boolean}  True if the control was successfully activated or
     *            false if the control was already active.
     */
    activate: function () {
        if (this.active) {
            return false;
        }
        if (this.handlers) {
            for (var key in this.handlers){
                this.handlers[key].activate();                
            }
        }

        this.selectControl.activate();

        this.active = true;
        this.events.triggerEvent("activate");
        return true;
    },

    /**
     * Method: deactivate
     * Deactivates a control and it's associated handlers if any.  Unselect all
     * selected features.
     * 
     * Returns:
     * {Boolean} True if the control was effectively deactivated or false
     *           if the control was already inactive.
     */
    deactivate: function () {
        if (this.active) {
            // deactivate all handlers
            if (this.handlers) {
                for (var key in this.handlers){
                    this.handlers[key].deactivate();                
                }
            }

            // unselect all features and deactivate selectControl
            this.selectControl.unselectAll();
            this.selectControl.deactivate();

            this.active = false;
            
            this.events.triggerEvent("deactivate");
            return true;
        }
        return false;
    },
    CLASS_NAME: "OpenLayers.Control.DeleteFeature"
});
