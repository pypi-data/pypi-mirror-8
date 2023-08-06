/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Handler/Box.js
 */

/**
 * Class: OpenLayers.Control.QueryByRect
 *
 * Inherits From:
 *  - <OpenLayers.Control>
 */
OpenLayers.Control.QueryByRect = OpenLayers.Class(OpenLayers.Control, {

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
     * APIProperty: handlerOptions
     * {Object} Additional options for the box handler used by this control.
     */
    handlerOptions: null,

    /**
     * APIProperty: clickTolerance
     * {Integer} Tolerance for the filter query in pixels. This has the
     *     same effect as the tolerance parameter on WMS GetFeatureInfo
     *     requests.  Will be ignored for box selections.  Applies only if
     *     <click> or <hover> is true.  Default is 5.  Note that this not
     *     only affects requests on click, but also on hover.
     */
    clickTolerance: 5,

    /**
     * Property: filterType
     * {<String>} The type of filter to use when sending off a request. 
     *     Possible values: 
     *     OpenLayers.Filter.Spatial.<BBOX|INTERSECTS|WITHIN|CONTAINS>
     *     Defaults to: OpenLayers.Filter.Spatial.BBOX
     */
    filterType: OpenLayers.Filter.Spatial.BBOX,


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
    featurepanels: [],

    /**
     * Property: getFeaturesResource
     * {Array(<Functions>)} Array of functions to forward the resource
     *                      to getFeatures.
     */
    getFeaturesResource: [],


    /**
     * APIProperty: resetOnDeactivation
     * {String} Defines what to reset when this widget is deactivated.
     */
    resetOnDeactivation: null,

    /**
     * Property: progressBar
     * {Ext.ProgressBar}
     */
    progressBar: null,

    /**
     * Constructor: OpenLayers.Control.QueryByRect
     * Create a new QueryByRect control.
     *
     * Parameters:
     * options - {Object} Optional object whose properties will be set on the
     *     control.
     */
    initialize: function(options) {
        options.handlerOptions = options.handlerOptions || {};

        OpenLayers.Control.prototype.initialize.apply(this, [options]);
        this.resourcestoquery = [];
        this.features = [];
        this.htmlResults = [];

        if(!this.resources){
            this.resources = [];
        }

        if(!this.results){
            this.results = [];
            // TODO : apply a default result object if none was provided
        }


        // Handler.Box
        this.handler= new OpenLayers.Handler.Box(
            this, {done: this.selectBox},
            OpenLayers.Util.extend(this.handlerOptions, {
                boxDivClassName: "olHandlerBoxSelectFeature"
            })
        ); 

        // resetOnDeactivation events listeners
        switch(this.resetOnDeactivation) {
          case "all":
            this.events.register("deactivate", this, this.resetQueryData);
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
     * Method: selectBox
     * Callback from the handlers.box set up when <box> selection is on
     *
     * Parameters:
     * position - {<OpenLayers.Bounds>}  
     */
    selectBox: function(position) {
        var bounds;
        if (position instanceof OpenLayers.Bounds) {
            var minXY = this.map.getLonLatFromPixel(
                new OpenLayers.Pixel(position.left, position.bottom)
            );
            var maxXY = this.map.getLonLatFromPixel(
                new OpenLayers.Pixel(position.right, position.top)
            );
            bounds = new OpenLayers.Bounds(
                minXY.lon, minXY.lat, maxXY.lon, maxXY.lat
            );
            
        } else {
            bounds = this.pixelToBounds(position);
        }
        //this.setModifiers(this.handlers.box.dragHandler.evt);
        this.request(bounds);
    },

    /**
     * Method: request
     */
    request: function(bounds) {
        // Reset the query data and all results panels
        this.resetQueryData();
        
        /**
         * RESOURCE VALIDATION
         * First, browse each resource.  If a layer that has the resource is
         * queryable, add it to the resources to query.
         */
        for (var i=0, len = this.resources.length; i<len; i++){
            var oResource = this.resources[i];

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

                    var layerParamForResource 
                        = oLayer.layersByResource[oResource.resource];

                    if(typeof layers == "string"){
                        //
                        if (layers.match(layerParamForResource)) {
                            bLayerFound = true;
                            break;
                        }
                    } else { // means it's an array
                        // todo : support the One Mother Of all WMS layer
                        // with service:name

                        if(OpenLayers.Util.indexOf(
                               layers, layerParamForResource) != -1){
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

        this.showWaitMessageBox();

        // load each query
        for (var i=0, len = this.resourcestoquery.length; i<len; i++){
            var oResource = this.resourcestoquery[i];

            var filter = new OpenLayers.Filter.Spatial({
                type: this.filterType, 
                value: bounds
            });

            this.getFeaturesResource[oResource.resource] = new Function("response","this.getFeatures(response,'"+oResource.resource+"');");

            var response = oResource.protocol.read({
                filter: filter,
                callback: this.getFeaturesResource[oResource.resource],
                scope: this
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
        if(response.success()) {
            var oResource = this.getResourceByName(resource);
            var oFeatures = response.features;
            for (var i=0, nbFeatures=oFeatures.length; i<nbFeatures; i++) {
                oFeatures[i].resource = resource;
            }
            this.features = this.features.concat(oFeatures);
        } else {
            this.errors++;
        }

        this.queries++;
        this.updateProgressBar();

        if(this.queries == this.resourcestoquery.length){
            this.showResult();
        }
    },

    /**
     * Method: resetResults
     * Reset all results content.
     */
    resetResults: function() {
        for(var i=0, len=this.results.length; i<len; i++){
            this.results[i].resetPanel();
        }
    },

    /**
     * Method: resetQueryData
     * Reset all properties used for a query and reset all
     *     result panels.
     */
    resetQueryData: function() {
        this.resourcestoquery = [];
        this.features = [];
        this.htmlResults = [];
        this.queries = 0;
        this.errors = 0;
        this.resetResults();
    },

    /**
     * Method: showResult
     * If results were found call each result "showResult" function.
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

        // execute each results (using features and htmlResults returned)
        for(var i=0, len=this.results.length; i<len; i++){
            this.results[i].showResult(this.features, this.htmlResults);
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
     * Method: pixelToBounds
     * Takes a pixel as argument and creates bounds after adding the
     * <clickTolerance>.
     * 
     * Parameters:
     * pixel - {<OpenLayers.Pixel>}
     */
    pixelToBounds: function(pixel) {
        var llPx = pixel.add(-this.clickTolerance/2, this.clickTolerance/2);
        var urPx = pixel.add(this.clickTolerance/2, -this.clickTolerance/2);
        var ll = this.map.getLonLatFromPixel(llPx);
        var ur = this.map.getLonLatFromPixel(urPx);
        return new OpenLayers.Bounds(ll.lon, ll.lat, ur.lon, ur.lat);
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

    CLASS_NAME: "OpenLayers.Control.QueryByRect"
});
