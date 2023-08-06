/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Handler/Click.js
 */

/**
 * Class: OpenLayers.Control.QueryOnClick
 *
 * Inherits From:
 *  - <OpenLayers.Control>
 */
OpenLayers.Control.QueryOnClick = OpenLayers.Class(OpenLayers.Control, {

    /**
     * Constant: EVENT_TYPES
     *
     * Supported event types:
     * afterqueries - Triggered after all queries were completed. The event
     *      object is an array of feature properties of the returned features.
     */
    EVENT_TYPES: ["afterqueries"],

    /**
     * Constant: DEFAULT_PARAMS
     * {Object} Hashtable of default parameter key/value pairs 
     */
    DEFAULT_PARAMS: {
        VERSION: "1.0.0",
        REQUEST: "GetFeatureInfo",
        EXCEPTIONS: "application/vnd.ogc.se_xml",
        FORMAT: "image/jpeg",
        INFO_FORMAT: 'application/vnd.ogc.gml',
        STYLES: "",
        FEATURE_COUNT: 1000
    },
    
    /*
        const: i18n_wait_options_msg
        {String} Wait msg        
    */
    i18n_wait_options_msg : "Query in progress, please wait...", 
    
    /*
        const: i18n_wait_options_progress_text
        {String} Wait progress text        
    */
    i18n_wait_options_progress_text : "Loading...", 
    
    /*
        const: i18n_wait_options_completed_text
        {String} Completed :
    */
    i18n_wait_options_completed_text : "Completed : ",

    /*
        const: i18n_wait_options_of_text
        {String} of
    */
    i18n_wait_options_of_text : " of ",

    /*
        const: i18n_no_layer_queryable
        {String} No layer is queryable       
    */
    i18n_no_layer_queryable : "No layer currently queryable.", 
    
    /*
        const: i18n_warning
        {String} Warning text       
    */
    i18n_warning : "Warning", 
    
    /*
        const: i18n_message_no_result_msg
        {String} No result message       
    */
    i18n_message_no_result_msg : "No record found.", 
    
        /*
        const: i18n_message_no_result_title
        {String} No result title
    */
    i18n_message_no_result_title : "No record found", 
    
    /**
     * Property: APIProperty: drawMode
     * {string}
     */
    drawMode: null,

    /**
     * Property: queryablelayers
     * {Array(String)} Layers that are queryable with GetFeatureInfo requests
     */
    queryablelayertypes : ["OpenLayers.Layer.WMS",
                           "OpenLayers.Layer.MapServer"],

    /**
     * Property: markerLayer
     * {<OpenLayers.Layer.Vector>} Layer used to point a marker where the user
     *                             clicked.
     */
    markerLayer: null,

    /**
     * Property: marker
     * {<OpenLayers.Feature.Vector>} Point feature created/updated on click
     */
    marker: null,

    /**
     * APIProperty: resources
     * {Array(<Object>)} Array of queryable resource objects.
     */
    resources: null,

    /**
     * APIProperty: resources
     * {Array(<Object>)} Array resource objects ready to be queried.
     */
    resourcestoquery: null,

    /**
     * APIProperty: lastEvt
     * {Event} Last event queried.
     */
    lastEvt: null,

    /**
     * Property: results
     * {Array(<Openlayer.Result>)} An array of Result objects used to render
     *                             the results of the query.
     */
    results: null,

    /**
     * Property: queries
     * {Integer} The number of queries received.  As soon as this number is
     *           equal to the length of the resourcestoquery array, that means
     *           all responses were received.
     */
    queries: 0,

    /**
     * Property: errors
     * {Integer} When an error occurs on the response of a query, this number is
     *           incremented.
     */
    errors: 0,

    /**
     * Property: features
     * {Array(<OpenLayers.Feature>)} Array of features created from the
     *                               responses received.
     */
    features: null,

    /**
     * Property: features
     * {Array(String)} Array of html results returned by queries using
     *                 'text/html' info_format parameter.
     */
    htmlResults: null,

    /**
     * Property: featurepanels
     * {Array(<OpenLayers.FeaturePanel>)} Array of FeaturePanel objects used to
     *                                    render the results of the query.
     */
    featurepanels: null,

    /**
     * Property: getFeaturesResource
     * {Array(<Functions>)} Array of functions to forward the resource
     *                      to getFeatures.
     */
    getFeaturesResource: null,


    /**
     * APIProperty: resetOnDeactivation
     * {String} Defines what to reset when this widget is deactivated.
     */
    resetOnDeactivation: null,

    /**
     * APIProperty: markerStyle
     * {Object} Used for the StyleMap for the markerLayer.  If none is providen,
     *          DEFAULT_MARKER_STYLE is used.
     */
    markerStyle: null,

    /**
     * Property: DEFAULT_MARKER_STYLE
     * {Object} Used for the StyleMap for the markerLayer if no markerStyle is
     *          providen.
     */
    DEFAULT_MARKER_STYLE : {
        graphicWidth: 21,
        graphicHeight: 25,
        graphicYOffset: -25,
        externalGraphic: OpenLayers.ImgPath+"marker.png"
    },

    /**
     * APIProperty: noMarker
     * {Boolean} If set to true, no marker layer is created.
     */
    noMarker: false,

    /**
     * Property: progressBar
     * {Ext.ProgressBar}
     */
    progressBar: null,

    /**
     * APIProperty: multipleKey
     * {String} An event modifier ('altKey', 'shiftKey' or 'ctrlKey') that
     *     temporarily sets the <multiple> property to true.  Default is null.
     */
    multipleKey: null,

    /**
     * APIProperty: toggleKey
     * {String} An event modifier ('altKey', 'shiftKey' or 'ctrlKey') that
     *     temporarily sets the <toggle> property to true.  Default is null.
     */
    toggleKey: null,

    /**
     * Property: modifiers
     * {Object} The event modifiers to use, according to the current event
     *     being handled by this control's handlers
     */
    modifiers: null,

    /**
     * APIProperty: multiQueryResource
     * {String} when in 'multiple' mode, query this resource only if this
     *     property is set.  Defaults to null.
     */
    multiQueryResource: null,

    /**
     * APIProperty: multiple
     * {Boolean} Allow selection of multiple features.  Default is false.
     */
    multiple: false, 

    /**
     * APIProperty: toggle
     * {Boolean} Unselect a selected feature on click.  Default is false.
     */
    toggle: false,

    /**
     * Constructor: OpenLayers.Control.QueryOnClick
     * Create a new QueryOnClick control.
     *
     * Parameters:
     * options - {Object} Optional object whose properties will be set on the
     *     control.
     */
    initialize: function(options) {
        OpenLayers.Control.prototype.initialize.apply(this, [options]);
        this.resourcestoquery = [];
        this.features = [];
        this.htmlResults = [];
        this.resources = this.resources || [];
        this.results = [];
        this.featurepanels = [];
        this.getFeaturesResource = [];

        if(this.noMarker !== true) {
            // markerStyle
            var markerStyle;
            if(this.markerStyle || this.markerStyle != null) {
                markerStyle = this.markerStyle;
            } else {
                markerStyle = this.DEFAULT_MARKER_STYLE;
            }

            var styleMap = new OpenLayers.StyleMap({
                "default": markerStyle
            });

            this.markerLayer = new OpenLayers.Layer.Vector(
                "QueryOnClick_Marker",
                { displayInLayerSwitcher: false, styleMap: styleMap }
            );
        }

        // Handler.Click
        var callbacks = {
          click: this.onClick
        };
        var options = {
          delay: 0
        };
        this.handler = new OpenLayers.Handler.Click(this, callbacks, options);

        // resetOnDeactivation events listeners
        switch(this.resetOnDeactivation) {
          case "marker":
            this.events.register("deactivate", this, this.removeMarker);
            break;
          case "all":
            this.events.register("deactivate", this, function() {
                this.resetQueryData({"modifiers": {"multiple": false}});
                this.resetFeatures();
            });
            break;
        }
    },

    /**
     * Method: getResourceNameByLayer
     * Returns the resource name of a layer given a service type.
     *
     * Parameters:
     * szLayer       - {String} The server-side layer name
     * szServiceType - {String} The service type (i.e. "wms")
     *
     * Returns:
     * {String} The resource name
     */
    getResourceNameByLayer: function(szLayer, szServiceType){
        for(var i=0; i<this.resources.length; i++){
            var oResource = this.resources[i];

            switch(szServiceType)
            {
              case "wms":
                if(oResource[szServiceType].queryLayers == szLayer){
                    return oResource.resource;
                }
                break;    
              case "wfs":
                if(oResource[szServiceType].typename == szLayer){
                    return oResource.resource;
                }               
                break;
              default:
                // unsuported
            }
        }
        return false;
    },

    /**
     * APIMethod: addResult
     * Add the result to this.results array.
     *
     * Parameters:
     * result - {<OpenLayers.Result>} The result object to add
     */
    addResult: function(result){
        this.results.push(result);
    },

    /**
     * APIMethod: addResults
     * Add the results to this.results array.
     *
     * Parameters:
     * results - {Array(<OpenLayers.Result>)} The result object to add
     */
    addResults: function(results){
        for(var i=0, len=results.length; i<len; i++){
            this.addResult(results[i]);
        }
    },

    /**
     * APIMethod: addFeaturePanel
     * Add the featurepanel to this.featurepanels array.
     *
     * Parameters:
     * featurepanel - {<OpenLayers.FeaturePanel>} The featurepanel object to add
     */
    addFeaturePanel: function(featurepanel){
        this.featurepanels.push(featurepanel);
    },


    /**
     * Method: onClick
     * Called by this click handler when the user click the map.
     * 
     * First, the current query data is reset and all result panels are reset
     * too.  Second, each resources are validated : is there a layer currently
     * visible that has the resource ?  Third, all queryable resource builds a
     * query and send it.
     */
    onClick: function(evt) {
        this.setModifiers(evt);

        // always reset all results before making any query
        this.resetQueryData();

        // Reset the query data and all results panels
        if (!this.modifiers.multiple) {
            this.resetFeatures();
        }

        this.lastEvt = evt;

        var lonlat = this.map.getLonLatFromPixel(evt.xy);
        
        /**
         * RESOURCE VALIDATION
         * First, browse each resource.  If a layer that has the resource is
         * queryable, add it to the resources to query.
         */
        for (var i=0, len = this.resources.length; i<len; i++){
            var oResource = this.resources[i];

            // check if we're in 'multiple' mode, if the 'multiQueryResource'
            // is set then the resource must be equal to it
            if (this.modifiers.multiple &&
                this.multiQueryResource !== null &&
                this.multiQueryResource !== oResource.resource) {
                continue;
            }

            // check if the resource is queryable, i.e. is 
            if(!oResource.queryable || !oResource['wms']){
                continue;
            }

            var szQueryLayers = oResource['wms']['queryLayers'];

            // find each layer having sharing the resourcename and check
            // if at least one is visible and inrange.  If so, carry on...
            var aoLayers = this.map.getLayersByResource(oResource.resource);
            var bLayerFound = false;
            for(var j=0; j<aoLayers.length; j++){
                var oLayer = aoLayers[j];
                if(!oLayer.visibility){
                    continue;
                }

                if(!oLayer.isBaseLayer && !oLayer.inRange){
                    continue;
                }

                // If the layer is WMS or MapServer, we must also validate
                // that the layer is currently in the params.LAYERS
                // property.  If not, it means that it's not currently 
                // visible
                if(OpenLayers.Util.indexOf(
                       this.queryablelayertypes, oLayer.CLASS_NAME) != -1 && 
		   oLayer.serviceType == "wms"){
                    var oParam = OpenLayers.Util.upperCaseObject(
                        oLayer.params);
                    var layers = oParam.LAYERS;

                    if(typeof layers == "string"){
                        //
                        if (layers.match(szQueryLayers)) {
                            bLayerFound = true;
                            break;
                        }
                    } else { // means it's an array
                        // todo : support the One Mother Of all WMS layer
                        // with service:name

                        if(OpenLayers.Util.indexOf(
                               layers, szQueryLayers) != -1){
                            bLayerFound = true;
                            break;
                        }
                    }           
                } else { // layer is not WMS or MapServer, no need to check more
                    bLayerFound = true;
                    break;
                }
            }
       
            if(!bLayerFound){
                continue;
            }          

            this.resourcestoquery.push(oResource);
        }

        if(this.resourcestoquery.length == 0){
            // TODO : this is HARDCODED
            var szMessage = this.i18n_no_layer_queryable;
            this.showMessage(this.i18n_warning, szMessage);
            return;
        }

        /**
         * QUERY START
         * From this point, we have one on more resource that needs to be
         * queryed.
         */

        if(this.noMarker !== true) {
            this.marker = new OpenLayers.Feature.Vector(
                new OpenLayers.Geometry.Point(lonlat.lon, lonlat.lat)
            );
        }

        this.showWaitMessageBox();

        // load each query
        for (var i=0, len = this.resourcestoquery.length; i<len; i++){
            var oResource = this.resourcestoquery[i];
            
            var szURL = oResource['wms'].url;

            var objParams = {
                osmresource: oResource.resource,
                osmservice: oResource['wms'].service,
                QUERY_LAYERS: oResource['wms'].queryLayers,
                LAYERS: oResource['wms'].queryLayers,
                SRS: this.map.getProjection(),
                BBOX: this.map.getExtent().toBBOX(),
                X: evt.xy.x,
                Y: evt.xy.y,
                WIDTH: this.map.size.w,
                HEIGHT: this.map.size.h,
                junk: Math.random()
            };
            objParams[oResource.session_name] = oResource.session_id

            if (oResource['wms']['version'])
            {
                objParams['VERSION'] = oResource['wms']['version'];
            }

            if (oResource['wms']['info_format'])
            {
                objParams['INFO_FORMAT'] = oResource['wms']['info_format'];
            }

            OpenLayers.Util.applyDefaults(
                objParams, 
                OpenLayers.Util.upperCaseObject(this.DEFAULT_PARAMS)
            );

            // temp fix, related to http://trac.openlayers.org/ticket/2478
            if (parseFloat(objParams['VERSION']) >= 1.3)
            {
                objParams['EXCEPTIONS'] = "INIMAGE";
            }

            var strParams = OpenLayers.Util.getParameterString(objParams);

            if(strParams.length > 0) {
                var strSeparator = (szURL.indexOf('?') > -1) ? '&' : '?';
                szURL += strSeparator + strParams;
            }
            
            this.getFeaturesResource[oResource.resource] = new Function("response","this.getFeatures(response,'"+oResource.resource+"');");

            OpenLayers.Request.GET({
                url:szURL,
                params:'',
                scope:this,
                success:this.getFeaturesResource[oResource.resource],
                failure:this.onError
            });
        }
    },

    /**
     * Method: getFeatures
     * Retreive the features from the query response and add them to 
     * this.features.  The number of result received is incremented
     * (this.queries).  When the last result is received, the method showResult
     * is called.
     *
     * Parameters:
     * response - {AJAX} Ajax response
     * resource - {String} Name of the resource
     */
    getFeatures: function(response, resource){
        var oResource = this.getResourceByName(resource);

        if (oResource['wms']['info_format'] != "text/html") {
            var oFormat = new OpenLayers.Format.WMSGetFeatureInfo();
            var oFeatures = oFormat.read(response.responseXML ||
                                         response.responseText);
            var feature;
            for (var i=0, nbFeatures=oFeatures.length; i<nbFeatures; i++) {
                feature = oFeatures[i];
                feature.resource = resource;
                if (oResource.resourcePrimaryField) {
                    feature.fid = feature.type + "." + 
                            feature.attributes[oResource.resourcePrimaryField];
                    
                }
                var pushFeature = feature.fid === null;
                if (!pushFeature) {
                    var existingFeature = 
                        this.getFeatureByResourceAndFid(resource, feature.fid);
                    if (existingFeature) {
                        if (this.modifiers.toggle) {
                            this.features = OpenLayers.Util.removeItem(
                                this.features, existingFeature);
                        }
                    } else {
                        pushFeature = true;
                    }
                }
                pushFeature && this.features.push(feature);
            }
        } else {
            this.htmlResults.push(
                {
                    'resource': oResource['resource'],
                    'resourceTitle': oResource['resourceTitle'],
                    'html': response.responseText
                }
            );
        }

        this.queries++;
        this.updateProgressBar();

        if(this.queries == this.resourcestoquery.length){
            this.events.triggerEvent("afterqueries", {
                features: this.features,
                resourceNames: this.getFeatureResourceNames()
            });
            this.showResult();
        }
    },

    /**
     * Method: onError
     * Called when an error occurs with the AJAX request
     *
     * Parameters:
     * response - {AJAX response}
     */
    onError: function(response){
        this.queries++;
        this.errors++;
        if(this.queries == this.resourcestoquery.length){
            this.showResult();
        }
    },

    /**
     * Method: removeMarker
     * Remove the query marker from the map.
     */
    removeMarker: function() {
        if(this.noMarker !== true) {
            this.marker = null;
            this.markerLayer.destroyFeatures(this.markerLayer.features);
        }
    },

    /**
     * Method: resetResults
     * Reset all results content.
     *
     * options     - {<Object>} Hash of options.  Possible keys are :
     *               - modifiers : the query modifiers
     */
    resetResults: function(options) {
        options = options || {};
        for(var i=0, len=this.results.length; i<len; i++){
            this.results[i].resetPanel(options);
        }
    },

    /**
     * Method: resetQueryData
     * Reset all properties used for a query and reset all result panels.
     *
     * options     - {<Object>} Hash of options.  Possible keys are :
     *               - modifiers : the query modifiers
     */
    resetQueryData: function(options) {
        options = options || {"modifiers": this.modifiers};
        this.resourcestoquery = [];
        this.queries = 0;
        this.errors = 0;
        this.resetResults(options);
    },

    /**
     * Method: resetQueryData
     * Reset 'feature-related' properties, such as : removing markers, reseting
     * features and htmlResults
     */
    resetFeatures: function() {
        for (var i=this.features.length; i>0; i--) {
            this.features[i-1].destroy();
        }
        this.features = [];
        this.htmlResults = [];
        this.removeMarker();
    },

    /**
     * Method: showResult
     * If results were found, add a marker where the user clicked and call each
     * result "showResult" function.
     */
    showResult: function(){
        // if no records were found
        if (this.features.length == 0 && this.htmlResults.length == 0) {
            this.hideWaitMessageBox();

            // TODO : this is HARDCODED
            var szMessage = this.i18n_message_no_result_msg;
            var szTitle =  this.i18n_message_no_result_title;

            if(this.errors == 1){
                szMessage += " "+this.errors+" occured.";
                szTitle += " and error";
            } else if (this.errors > 1){
                szMessage += " "+this.errors+" occured.";
                szTitle += " and errors";
            }
            this.showMessage(szTitle, szMessage);
            return;
        }
 
        if(this.noMarker !== true) {
            this.markerLayer.addFeatures([this.marker]);
        }

        // execute each results (using features and htmlResults returned)
        for(var i=0, len=this.results.length; i<len; i++){
            this.results[i].showResult(
                this.features, this.htmlResults, {'modifiers': this.modifiers});
        }
        this.hideWaitMessageBox();
		
        // execute each feature panels
        for(var i=0, len=this.featurepanels.length; i<len; i++){
            this.featurepanels[i].showFeaturePanel(this.features);
        }

        if(this.errors > 0){
            // TODO this is HARDCODED
            var szMessage = this.errors+" error";
            var szTitle = "Error";
            if(this.errors == 1){
                szMessage += " occured.";
            } else {
                szMessage += "s occured";
                szTitle += "s";
            }
            this.showMessage(szTitle, szMessage);
        }
    },

    /**
     * Method: showWaitMessageBox
     * Shows a "wait message" in a Ext.Window with a ProgressBar.
     */
    showWaitMessageBox: function() {
        this.waitmessagebox = new Ext.Window({
              title: this.i18n_wait_options_msg,
              width: '200',
              modal: true,
              closable: false,
              closeAction: 'hide',
              items:[
                  new Ext.ProgressBar({
                      text: this.i18n_wait_options_progress_text,
                      id:'queryonclick-pbar',
                      xtype: 'progress',
                      cls:'left-align'
                  })
              ]
        });
        this.updateProgressBar();
        this.waitmessagebox.show();
    },

    /**
     * Method: hideWaitMessageBox
     * Hides the "wait message" Ext.Window.
     */
    hideWaitMessageBox: function() {
        this.waitmessagebox.hide();
    },

    /**
     * Method: updateProgressBar
     * Update the "wait message" window with the current queries completed.
     */
    updateProgressBar: function() {
        var nCurrent = this.queries;
        var nCount = this.resourcestoquery.length;
        var szMessage =  this.i18n_wait_options_completed_text + nCurrent + 
            this.i18n_wait_options_of_text  + nCount + '...';

        var oProgressBar = Ext.getCmp('queryonclick-pbar');
        oProgressBar.updateProgress(nCurrent/nCount, szMessage);
    },

    /**
     * Method: setMap
     * Set the map property for the control and all handlers.
     *
     * Parameters:
     * map - {<OpenLayers.Map>} The control's map.
     */
    setMap: function(map) {
        if(this.noMarker !== true) {
            map.addLayer(this.markerLayer);
        }
        this.handler.setMap(map);
        OpenLayers.Control.prototype.setMap.apply(this, arguments);
    },

    /**
     * Method: getResourceByName
     * Returns the resource object inside this widget using its name.  If not
     *     found, returns false.
     *
     * Parameters:
     * resourceName - {String} The name of the resource to look for
     *
     * Return:
     * {Object} The resource object contained in this widget or false if not
     *          found.
     */
    getResourceByName: function(resourceName) {
        for (var i=0, len=this.resources.length; i<len; i++) {
            if (this.resources[i].resource == resourceName) {
                return this.resources[i];
            }
        }
        return false;
    },

    /**
     * Method: setModifiers
     * Sets the multiple modifiers according to the current event
     * 
     * Parameters:
     * evt {<OpenLayers.Event>}
     */
    setModifiers: function(evt) {
        this.modifiers = {
            multiple: this.multiple || (this.multipleKey && evt[this.multipleKey]),
            toggle: this.toggle || (this.toggleKey && evt[this.toggleKey])
        };        
    },

    /**
     * APIMethod: getFeatureByResourceAndFid
     * Given a feature resource and fid, return the feature if it exists in the
     *     features array
     *
     * Parameters:
     * resource - {String} The feature resource name
     * fid - {String} The feature fid
     *
     * Returns:
     * {<OpenLayers.Feature.Vector>} A feature corresponding to the given
     * fid and resource or null if there is no such feature.
     */
    getFeatureByResourceAndFid: function(resource, fid) {
        var feature = null;
        for (var i=0, len=this.features.length; i<len; ++i) {
            if (this.features[i]['fid'] == fid &&
                this.features[i]['resource'] == resource) {
                feature = this.features[i];
                break;
            }
        }
        return feature;
    },

    /**
     * APIMethod: getFeatureResourceNames
     * Returns all resource names of current features.
     *
     * Returns:
     * {Array} of resource names
     */
    getFeatureResourceNames: function() {
        var resourceNames = [], resourceName;
        for (var i=0, iLen=this.features.length; i<iLen; i++) {
            resourceName = this.features[i].resource;
            OpenLayers.Util.indexOf(resourceNames, resourceName) == -1 &&
                resourceNames.push(resourceName);
        }
        return resourceNames;
    },

    /**
     * Method: showMessage
     * Display a Ext.MessageBox and hide it after 2 seconds.
     * 
     * Parameters:
     * title   - {String} Title of the message
     * message - {String} The message
     * icon    - {String} The ext icon to use in the message box
     */
    showMessage: function(title, message, icon) {
        Ext.MessageBox.show({
            title: title,
            msg: message,
            modal: false,
            icon: icon || Ext.MessageBox.WARNING
        });
        setTimeout(function(){
            Ext.MessageBox.hide();
        }, 2000);
    },

    CLASS_NAME: "OpenLayers.Control.QueryOnClick"
});
