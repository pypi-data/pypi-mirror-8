/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Control.js
 * @requires mapfish/Protocol/MapFish.js
 * @requires OpenLayers/Format/GeoJSON.js
 *
 * @requires OpenLayers/Control/SelectFeature.js
 * @requires OpenLayers/Control/DrawFeature.js
 * @requires OpenLayers/Control/ModifyFeature.js
 * @requires OpenLayers/Control/DeleteFeature.js
 * @requires OpenLayers/Control/Snapping.js
 */

/**
 * Class: OpenLayers.Control.EditFeature
 *
 * N.B. Supports only ONE vector layer
 *
 * Inherits From:
 *  - <OpenLayers.Control>
 */
OpenLayers.Control.EditFeature = OpenLayers.Class(OpenLayers.Control, {

    /**
     * Constant: EVENT_TYPES
     *
     * Only used by OpenLayers 2.11 or older.  New versions support any events.
     * Supported event types:
     *  - *aftercommit* Triggered after features commit
     */
    EVENT_TYPES: ["aftercommit"],

    /**
     * Property: VECTOR_LAYER_TYPES
     * {Array(String)} Supported Vector layer types for the edition control.
     */
    VECTOR_LAYER_TYPES : ["OpenLayers.Layer.Vector"],

    /**
     * Property: WMS_LAYER_TYPES
     * {Array(String)} Supported WMS layer types.  Only used to redraw on
     *     commits.
     */
    WMS_LAYER_TYPES : ["OpenLayers.Layer.WMS"],

    /**
     * APIProperty: APIProperty: drawMode
     * {string}
     */
    drawMode: null,

    /**
     * APIProperty: snappingcontrol
     * {OpenLayers.Control.Snapping}Snapping Control
     */
    snappingcontrol: null,

    /**
     * APIProperty: snappingcontroloptions
     * {Object} Object of options to use when creating this.snappingcontrol
     */
    snappingcontroloptions: null,

    /**
     * APIProperty: id
     * {string} A unique id used to get the GeoExt.Action (button/checkItem)
     *          for enable/disable purpose (by following the vector layer
     *          visibility).
     */
    id: null,

    /**
     * APIProperty: featurepanel
     * {<org.GeoPrisma.FeatureFormPanel>} Customized Ext.FormPanel object in
     *                                    which to display the feature's
     *                                    attributes
     */
    featurepanel: null,

    /**
     * APIProperty: featurecontrol
     * {<OpenLayers.Control.SelectFeature>||<OpenLayers.Control.ModifyFeature>)}
     * The OpenLayers.Control used when editing a feature.
     */
    featurecontrol: null,

    /**
     * APIProperty: featurecontroloptions
     * {Object} Object of options to use when creating this.featurecontrol
     */
    featurecontroloptions: null,

    /**
     * APIProperty: singlefeature
     * {Boolean} true if only one feature can be selected at a time by the
     *           SelectFeature control (of the featurecontrol)
     */
    singlefeature: false,

    /**
     * APIProperty: resource
     * {String} Resource name.  Used to find the corresponding vector layer.
     */
    resource: null,

    /**
     * Property: layer
     * {OpenLayers.Layer.Vector} Vector layer that has this.resource
     */
    layer: null,

    /**
     * Property: handlers
     * {Array(<OpenLayers.Handler>)}
     */
    handlers: null,

    /**
     * Property: wmslayer
     * {OpenLayers.Layer.WMS} WMS layer that has this.resource
     */
    wmslayer: null,

    /**
     * APIProperty: wmslayerredraw
     * {boolean} Redraw the WMS Layer on commits.
     */
    wmslayerredraw: true,

    /**
     * APIProperty: cancelCodes
     * {Array(Integer)} The key codes to trigger the 'cancel' action
     */
    cancelCodes: null,

    /**
     * APIProperty: confirm
     * {org.GeoPrisma.EditFeature.Confirm} The confirm plugin to manage the
     * commits.  Is automatically set when widget is added and follow the
     * requirements.
     */
    confirm: null,

    /**
     * APIProperty: resourceOptions
     * {Options} The options of the resource linked to this widget.
     */
    resourceOptions: null,

    /**
     * APIProperty: afterInsertWindowOptions
     * {afterInsertWindowOptions} The options used to create the window
     *                            displayed after a single commit.  Only used
     *                            if 'selectorMethod' resource option is set.
     */
    afterInsertWindowOptions: null,

    /**
     * Constructor: OpenLayers.Control.EditFeature.Update
     * Create a new EditFeature.Update control.
     *
     * Parameters:
     * options - {Object} Optional object whose properties will be set on the
     *     control.
     */
    initialize: function(options) {
        // concatenate events specific to this control with those from the base
        if (OpenLayers.Control.prototype.EVENT_TYPES) {
            this.EVENT_TYPES =
                OpenLayers.Control.EditFeature.prototype.EVENT_TYPES.concat(
                OpenLayers.Control.prototype.EVENT_TYPES
            );
        }

        OpenLayers.Control.prototype.initialize.apply(this, [options]);

        this.cancelCodes = [OpenLayers.Event.KEY_ESC];
        this.resourceOptions = this.resourceOptions || {};

        // afterInsertWindow options setting
        this.afterInsertWindowOptions = Ext.applyIf(
            this.afterInsertWindowOptions || {}, {
            layout: 'fit',
            closable : true,
            width : this.resourceOptions.selectorTemplateWidth || 400,
            height : this.resourceOptions.selectorTemplateHeight || 300,
            border : false,
            modal: true,
            plain : true,
            resizable : false,
            autoScroll: true,
            constrain: true
        });

        // configure the keyboard handler
        var keyboardOptions = {
            keydown: this.handleKeypress
        };
        this.handlers = {
            keyboard: new OpenLayers.Handler.Keyboard(this, keyboardOptions)
        };
    },

    /**
     * APIProperty: onSelect 
     * {Function} Optional function to be called when a feature is selected.
     *     The function should expect to be called with a feature.
     */

    /**
     * Method: setFeatureControl
     * Called as soon as the vector layer related to the resources of this
     * control is found.  It creates the according OpenLayers control depending
     * on what is the type of editfeature control currently used.
     * The code of this function is redefined in the child control, i.e. :
     * /create/Create.js
     * /update/Update.js
     * /delete/Delete.js
     *
     * Parameters:
     * layer - {<OpenLayers.Layer.Vector>} The vector layer to assign the
     *                                     control to be created.
     * options - {Object} Options for the control to be created.
     */
    setFeatureControl: function(layer) {},

     /**
     * Method: setSnappingControl
     * Called as soon as the vector layer related to the resources of this
     * control is found.  
     * The code of this function is redefined in the child control, i.e. :
     * /create/Create.js
     * /update/Update.js
     * /delete/Delete.js
     *
     * Parameters:
     * layer - {<OpenLayers.Layer.Vector>} The vector layer to assign the
     *                                     control to be created.
     * options - {Object} Options for the control to be created.
     */
    setSnappingControl: function(layer) {},

    /**
     * Method: getSelectControl
     * Returns the SelectFeature control used by this control depending on
     * this.snappingcontrol.
     *
     * options - {Object} Options for the control to be created.
     * Returns: 
     * {<OpenLayers.Control.SelectFeature>}
     */
    getSelectControl: function() {
        var control;

        switch(this.featurecontrol.CLASS_NAME) {
            case "OpenLayers.Control.SelectFeature":
              control = this.featurecontrol;
              break;
            case "OpenLayers.Control.ModifyFeature":
            case "OpenLayers.Control.DeleteFeature":
              control = this.featurecontrol.selectControl;
              break;
        }

        return control;
    },

//TODO: remove and replace this
    /**
     * Method: getSelectedFeatures
     * Returns current selected features.
     *
     * Returns: 
     * {Array of(<OpenLayers.Feature.Vector>)}
     */
    getSelectedFeatures: function() {
        return this.layer.selectedFeatures;
    },

    /**
     * Method: commit
     * Commit created/updated/deleted features using the layer's protocol.
     * Currently supports the MapFish and HTTP protocols.
     *
     * Calls this.onCommit function when a response is received.
     *
     * Parameters:
     * features {Array of(<OpenLayers.Feature.Vector>)}
     */
    commit: function (features) {
        switch(this.layer.protocol.CLASS_NAME) {
          // FEATURESERVER
          case "mapfish.Protocol.MapFish":
          case "OpenLayers.Protocol.HTTP":
            this.layer.protocol.commit(
                features, {
                    "create": {
                      callback: this.onCommit,
                      scope: this
                },
                    "update": {
                      callback: this.onCommit,
                      scope: this
                },
                    "delete": {
                      callback: this.onCommit,
                      scope: this
                }
            });
            break;
          default:
            alert("not suported");
        }
    },

    /**
     * Method: onCommit
     * Called after protocol commit.
     *
     * Currently supports GeoJSON format only.
     *
     * Parameters:
     * response - {<OpenLayers.Protocol.Response>} A response object.
     */
    onCommit: function(response) {
        // Get the features from the returned GeoJSON
        var oFormat = new OpenLayers.Format.GeoJSON();
        var aoReturnedFeatures = oFormat.read(response.priv.responseText);

        // Get the features returned in reqFeatures, thoses that still have
        // their "state" to DELETE/INSERT/UPDATE
        var aoFeatures = response.reqFeatures;
        if(!aoFeatures.length){
            aoFeatures = [aoFeatures];
        }

        var szState, oFeature, single;
        var aoDestroys = [];
        var j = 0;
        for(var i=0, len=aoFeatures.length; i<len; ++i) {
            oFeature = aoFeatures[i];
            szState = oFeature.state;
            if(szState) {
                if(szState == OpenLayers.State.DELETE) {
                    aoDestroys.push(oFeature);
                } else if(szState == OpenLayers.State.INSERT) {
                    // add the fid to current feature
                    oFeature.fid = aoReturnedFeatures[j].fid;
                    single = oFeature;
                    ++j;
                }
                oFeature.state = null;
            }
        }

        // after inserting a single feature, if resource has a 'selectorMethod'
        // option and no featurePanel is linked to this widget, open a window
        // containing whatever the 'selectorMethod' returns.  Only 'Create',
        // 'Copy' and 'Update' widgets supported
        if (Ext.isFunction(this.resourceOptions.selectorMethod) &&
            !this.featurepanel &&
            ((OpenLayers.Control.EditFeature_Create != undefined && this instanceof OpenLayers.Control.EditFeature_Create) ||
             (OpenLayers.Control.EditFeature_Copy != undefined && this instanceof OpenLayers.Control.EditFeature_Copy) ||
             (OpenLayers.Control.EditFeature_Update != undefined && this instanceof OpenLayers.Control.EditFeature_Update)) &&
            j == 1 // only one feature was inserted
        ) {
            // selectorMethod called with following arguments :
            // (1) resource name
            // (2) feature id
            new Ext.Window(Ext.applyIf({items: [
                this.resourceOptions.selectorMethod(this.resource, single.fid)
            ]}, this.afterInsertWindowOptions)).show();
        }
        
        this.events.triggerEvent("aftercommit", {
            returnedFeatures : aoReturnedFeatures,
            requestFeatures: aoFeatures
        });

        // destroy the deleted features
        if(aoDestroys.length > 0) {
            this.featurecontrol.layer.destroyFeatures(aoDestroys);
            
            //On rafraichit la couche
            try{
                    var arrLayerCustomRes = map.getLayersByResource('126');
                    var wmslayer = null;
                    for (var i=0;i<2;i++){
                        wmslayer = arrLayerCustomRes[i];
                        if( wmslayer.servicetype == 'wms' || wmslayer.serviceType == 'wms'){
                            wmslayer.redraw(true);
                        }
                    }
            }catch(e){}
        }

        if(this.wmslayer && this.wmslayerredraw){
            this.wmslayer.redraw({force:true});
        }
        
        // Force layer redraw to force style map are aplied on new fid
        this.featurecontrol.layer.redraw({force:true});
    },

    /**
     * Method: onModificationStart
     * Called before feature modification.  Show the FeaturePanel if it's set.
     * If the feature is about to be modified (not a new feature), clone it
     * to keep an original copy if modification are canceled.
     *
     * Parameters:
     * object - {<OpenLayers.Event>} Used to get the feature about to be 
     *                               modified
     */
    onModificationStart: function(object) {
        var feature = (object.geometry) ? object : object.feature;

        if (this.featurepanel || this.confirm) {
            if(feature.state != OpenLayers.State.INSERT && !feature.myClone){
                feature.myClone = feature.clone();
                feature.myClone.fid = feature.fid;
            }
        }

        if (this.featurepanel) {
            var customform_id = this.featurepanel.CUSTOM_FORM_ID;
            if(!Ext.getCmp(customform_id)){
                this.featurepanel.showFeaturePanel([feature], this);
            }
        }
    },

    /**
     * Method: onModification
     * Called on feature modification.
     *
     * Parameters:
     * object - {<OpenLayers.Event>} Used to get the modified feature
     */
    onModification: function(object) {
        //we could execute commits here instead
    },

    /**
     * Method: onModificationEnd
     * Called after feature modification.  
     * If using a FeaturePanel :
     *     Validate that it's currently commiting.  If not, depending of the
     *     feature state, reset or destroy the feature.
     * If not using a FeaturePanel :
     *     Simply commit the modifications made to the feature.
     *
     * Parameters:
     * object - {<OpenLayers.Event>} Used to get the modified feature
     */
    onModificationEnd: function(object) {
        var feature = (object.geometry) ? object : object.feature;
        
        if(this.featurepanel){
            if(!this.featurepanel.commiting){
                this.cancel(feature);
            }
            this.featurepanel.hideFeaturePanel(feature);
        } else if (this.confirm && this.confirm.cancel) {
            this.cancel(feature);
        } else {
            if (feature.myClone) {
                feature.myClone = null;
            }
            this.commit([feature]);
        }
    },

    /**
     * Method: cancel
     * Cancel modification on a feature (if it has any).
     *
     * Parameters:
     * feature - {<OpenLayers.Feature.Vector>}
     */
    cancel: function(feature) {
        switch (feature.state)
        {
          case OpenLayers.State.INSERT:
            this.layer.destroyFeatures([feature]);
            break;
          case OpenLayers.State.UPDATE:
            this.layer.addFeatures([feature.myClone]);
            this.layer.destroyFeatures([feature]);
            break;
        }
    },

    /**
     * APIMethod: setFeaturePanel
     * Set the FeaturePanel of this control, which supports only one.  At the
     * same time, this control is also added as an owner to the FeaturePanel
     * object for reference uses.
     *
     * Parameters:
     * result - {<OpenLayers.Result>} The result object to be set
     */
    setFeaturePanel: function(featurepanel){
        this.featurepanel = featurepanel;
        this.featurepanel.setSingleFeature(true);
        this.featurepanel.addOwner(this);
    },

    /**
     * Method: toggleExtComponent
     * Called on map "moveend" events.  If the layer becomes out
     * of range, disable the according Ext.Component (button/checkItem).
     */
    toggleExtComponent: function(){
        var oComponent = Ext.getCmp(this.id);

        if(!oComponent) {
            return;
        }

        if (this.layer.inRange){
            oComponent.enable();
        } else {
            oComponent.disable();
            if(this.active) {
                this.deactivate();
            }
        }
    },

    /**
     * Method: handleKeypress
     * Called by the keyboard handler when a key is pressed.  This is used to
     * for the following key+events :
     *   - 'esc' : cancel the current edition.
     *
     * Parameters:
     * {Integer} Key code corresponding to the keypress event.
     */
    handleKeypress: function(evt) {
        var code = evt.keyCode;

        // 'cancel'
        if(OpenLayers.Util.indexOf(this.cancelCodes, code) != -1) {
            if(this.featurepanel){
                this.featurepanel.commiting = false;                
            }
            this.getSelectControl().unselectAll();
            return;
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
        OpenLayers.Control.prototype.setMap.apply(this, arguments);
        this.handlers.keyboard.setMap(map);
        this.setLayers();
    },

    /**
     * APIMethod: setLayers
     *
     * Browse the current layers of the map having the resource used by this
     * widget.  Assign this.layer to the first supported vector layer found. 
     * If a WMS layer is found, assign it to this.wmslayer (for redraw use
     * only).
     */
    setLayers: function() {
        var layers = this.map.getLayersByResource(this.resource);
        for (var i=0, len=layers.length; i<len; i++) {
            layer = layers[i];

            var index = OpenLayers.Util.indexOf(
                this.VECTOR_LAYER_TYPES, layer.CLASS_NAME);
            if(index != -1 && !this.layer) {
                this.setFeatureControl(layer);
                this.setSnappingControl(layer);
                this.layer = layer;
                this.map.events.register(
                    "moveend", this, this.toggleExtComponent);
            }

            index = OpenLayers.Util.indexOf(
                this.WMS_LAYER_TYPES, layer.CLASS_NAME);
            if(index != -1 && !this.wmslayer) {
                this.wmslayer = layer;
            }

            if(this.layer && this.wmslayer) {
                break;
            }
        }
    },

    /**
     * APIMethod: activate
     * Activate the control.
     * 
     * Returns:
     * {Boolean} Successfully activated the control.
     */
    activate: function() {
        var activated = this.layer && 
            OpenLayers.Control.prototype.activate.apply(this, arguments);
        
        if (activated && this.handlers) {
            for (var key in this.handlers){
                this.handlers[key].activate();                
            }
        }

        if(activated){
            this.layer.setVisibility(true);
            
            //On force le rafraichissement
            this.layer.refresh({force: true})
            index=Math.max(this.map.Z_INDEX_BASE['Feature']-1,this.layer.getZIndex())+10;
            this.layer.setZIndex(index);
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
        var deactivated = this.layer &&
            OpenLayers.Control.prototype.deactivate.apply(this, arguments);

        if (deactivated && this.handlers) {
            for (var key in this.handlers){
                this.handlers[key].deactivate();                
            }
        }

        deactivated && this.layer.setVisibility(false);

        // if control was deactivated and there is still a confirm popup
        // currently visible, close it
        this.confirm && this.confirm.popup && this.confirm.popup.close();

        return deactivated;
    },

    CLASS_NAME: "OpenLayers.Control.EditFeature"
});
