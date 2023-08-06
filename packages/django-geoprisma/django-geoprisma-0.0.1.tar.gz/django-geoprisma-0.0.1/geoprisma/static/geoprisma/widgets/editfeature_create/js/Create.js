/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Control/DrawFeature.js
 * @requires OpenLayers/Control/ModifyFeature.js
 */

/**
 * Class: OpenLayers.Control.EditFeature_Create
 *
 * Inherits From:
 *  - <OpenLayers.Control.EditFeature>
 */
OpenLayers.Control.EditFeature_Create = OpenLayers.Class(OpenLayers.Control.EditFeature, {
    
    /*
        const: i18n_checkfid_exist_messagebox_title
        {String} Title of the checkfid message box        
    */
    i18n_checkfid_exist_messagebox_title : "Add control was desactivate",
    
    /*
        const: i18n_checkfid_exist_messagebox_message
        {String} Message of the checkfid message box        
    */
    i18n_checkfid_exist_messagebox_message : "Add control was desactivate, because only one feature is autorised",
    
    /**
     * APIProperty: drawfeatureoptions
     * {Object} Options for the draw feature controls created
     */
    drawfeatureoptions: null,

    /**
     * APIProperty: geometrytype
     * {String} Geometry type this control can create.  A single DrawFeature
     *          control is created according to the type.
     */
    geometrytype: null,

    /**
     * Property: drawControl
     * {<OpenLayers.Control.DrawFeature>}
     */
    drawControl: null,
    
    /**
     * Property: checkfid
     * if is not null, create check id feature not exist before add are authorized
     */
    checkfid: null,
    
    /**
     * Constructor: OpenLayers.Control.EditFeature_Create
     * Create a new EditFeature_Create control.
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
     * Create a ModifyFeature and assign it to this control.  Event registration
     * is done in this.activate function.
     *
     * Parameters:
     * layer - {<OpenLayers.Layer.Vector>} The vector layer to assign the
     *                                     created control to.
     */
    setFeatureControl: function(layer) {
        var options = this.featurecontroloptions || {};
        var control;

        // ModifyFeature control, to be able to change the geometry after
        // the feature is drawn.
        control = new OpenLayers.Control.ModifyFeature(
            layer, options);

        this.featurecontrol = control;
        this.map.addControl(control);

        // create the draw controls
        this.setDrawControl(layer);
    },

    /**
     * Method: setDrawControl
     * Create a DrawFeature control for a particular geometry type.  Also
     * registers a 'featureadded' event to deal with features created by 
     * the DrawFeature control.
     *
     * Parameters:
     * layer - {<OpenLayers.Layer.Vector>} The vector layer to assign the
     *                                     created control to.
     */
    setDrawControl: function(layer) {
        var handler, control, options;
        options = this.drawfeatureoptions || {};

        switch(this.geometrytype) {
          case "LineString":
          case "MultiLineString":
            handler = OpenLayers.Handler.Path;
            break;
          case "Point":
          case "MultiPoint":
            handler = OpenLayers.Handler.Point;
            break;
          case "Polygon":
          case "MultiPolygon":
            handler = OpenLayers.Handler.Polygon;
            break;
        }

        control = new OpenLayers.Control.DrawFeature(
            layer, handler, options);

        this.drawControl = control;
        this.map.addControl(control);

        //when a draw control is activated, activate THIS Create control as well
        control.events.register("activate", this, this.activate);
    },

    /**
     * Method: onFeatureAdded
     * Called when a feature is added to the vector layer.  Sets the state of
     * the newly created feature to INSERT, deactivate the DrawFeature control
     * and activate the ModifyFeature control for attributes/geometry edition
     * 
     * Parameters:
     * event - {<OpenLayers.Event>}
     */
    onFeatureAdded: function(event) {
        var feature, geometryType;

        feature = event.feature;
        geometryType = feature.geometry.CLASS_NAME;

        // TODO: support MultiGeometry
        // cast to multilinestring
        /*
        oFeature.geometry = new OpenLayers.Geometry.MultiLineString(
            oFeature.geometry
        );
        */

        feature.state = OpenLayers.State.INSERT;

        this.featurecontrol.activate();
        this.drawControl.deactivate();
        
        this.featurecontrol.selectControl.select(feature);
    },

    /**
     * Method: resumeDraw
     * Called when a modification (edition) is finished.  Deactivates the
     * ModifyFeature control and reactivate the DrawFeature.
     * 
     * Parameters:
     * event - {<OpenLayers.Event>}
     */
    resumeDraw: function(event) {
        this.featurecontrol.deactivate()
        this.drawControl.activate();
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
            // first, check if one draw control has been already activated
            this.drawControl.activate();

            // register "featureadded" event (DrawFeature ctrl)
            this.drawControl.events.on({
               "featureadded": this.onFeatureAdded,
                scope: this
            });

            // register "before/after/featuremodified" events
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
            this.layer.events.on({
               "afterfeaturemodified": this.resumeDraw,
                scope: this
            });
               
            this.doCheckfid(true);      
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
            this.drawControl.deactivate();
            this.featurecontrol.deactivate();
            
            // unregister "featureadded" event (DrawFeature ctrl)
            this.drawControl.events.un({
               "featureadded": this.onFeatureAdded,
                scope: this
            });

            // unregister "before/after/featuremodified" events
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
            this.layer.events.un({
               "afterfeaturemodified": this.resumeDraw,
                scope: this
            });

        }
        return deactivated;
    },
    
    /**
     * APIMethod: onCommit
     * Force check of fid after feature are commited
     *
     * Returns: 
     * (void)
     */
    onCommit: function(response)
    {
        OpenLayers.Control.EditFeature.prototype.onCommit.apply(this, [response])
        this.doCheckfid(false);        
    },
    
    /**
     * Method: doCheckfid 
     * Check if feature alreay exist before its creation. To permit the possibility to add only one feature with url passed fid
     *
     * Returns: 
     * (void)
     */
    doCheckfid: function(showMessage){    
        if (this.checkfid != null)
        {          
            var nFeatureId = this.checkfid;
            var temp = this.layer.protocol.url + "";
            var iParamStart = temp.indexOf("?");
            
            strHost = temp.substring(0,iParamStart);
            strParam = temp.substring(iParamStart);
            
            temp = strHost + '/' + nFeatureId + '.geojson' + strParam;
            
            this.checkfidshowmessage = showMessage;        
            OpenLayers.loadURL({
                url:temp,
                params:'',
                scope:this,
                callback:this.doCheckfidCallback
            });
        }
    },
    
    /**
     * Method: doCheckfidCallback 
     * Ajax request result callback function that check the result and deactivate the create control is feature exist.
     *
     * Returns: 
     * (void)
     */
    doCheckfidCallback : function(response){
        var oFormat = new OpenLayers.Format.GeoJSON();
        var oFeatures = oFormat.read(response.responseText);

        if(oFeatures && oFeatures.length > 0)
        { 
            if (this.checkfidshowmessage)
            {
                Ext.MessageBox.show({
                    title: this.i18n_checkfid_exist_messagebox_title,
                    msg: this.i18n_checkfid_exist_messagebox_message,
                    buttons: Ext.MessageBox.OK,
                    icon: Ext.MessageBox.INFO
                });
            }
            this.deactivate();      
        }   
    },

    CLASS_NAME: "OpenLayers.Control.EditFeature_Create"
});
