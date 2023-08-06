/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * @requires OpenLayers/Result
 *
 * Class: OpenLayers.ResultExtGrid
 * 
 * Inherits from:
 *  - <OpenLayers.Result>
 */
OpenLayers.ResultExtGrid = OpenLayers.Class({

    /*
        const: i18n_default_panel_html
        {String} Html contain of the default panel        
    */
    i18n_default_panel_html : "<p>Query the map first</p>", 
    
    /*
        const: i18n_default_panel_title
        {String} Title of the default panel        
    */
    i18n_default_panel_title : "Help", 
    
    /*
        const: i18n_no_result_panel_html
        {String} Html contain of the no result panel
    */
    i18n_no_result_panel_html : "<p>No result to display</p>", 
    
    /*
        const: i18n_no_result_panel_title
        {String} Title of the no result panel       
    */
    i18n_no_result_panel_title : "Warning", 
    
    /*
        const: i18n_query_result
        {String} ??      
    */
    i18n_query_result : "Query result",
    
    /*
        const: i18n_message_select_row
        {String} Alert message to select row in grid      
    */
    i18n_message_select_row_msg : "Please select a row", 
    
    /*
        const: i18n_message_select_row
        {String} Alert message to select row in grid      
    */
    i18n_message_select_row_title : "Warning", 
    
    /*
        const: i18n_window_title
        {String} Title for window when inwindow is true     
    */
    i18n_window_title : "Result", 


    /**
     * Property: APIProperty: drawMode
     * {string}
     */
    drawMode: null,

    query: null,

    resources: null,

    /**
     * Property: panel
     * {Ext.TabPanel} The panel that contains the GridPanel created for each
     *                query result type
     */
    panel: null,

    /**
     * APIProperty: inWindow
     * {Boolean} If true, the panel is automatically drawn inside a Ext.Window, 
     *           so there's no need to call the widget drawWidget function.
     *           If false, the panel need to be drawn in the template as normal,
     *           but its ownerCt must have layout:'fit' set.
     */
    inWindow: true,

    /**
     * Property: oldWindow
     * {Ext.Window} When in inWindow:true mode, the window that opens is not
     *              destroyed on closing.  It is assigned to this property.
     *              This is a fix because of a bug in IE.  See below.
     */
    oldWindow: null,

    /**
     * APIProperty: widgetName
     * {String} The name of the widget.  Used to create unique id, like the
     *          panel id.
     */
    widgetName: null,

    /**
     * APIProperty: widgetName
     * {Object} If set, becomes an object containing info needed for the link
     *          to other application.  TODO: document this more...
     */
    delegateContext: false,

    /**
     * Property: defaultPanel
     * {Object} The object used to create the panel displayed by default in
     *          this.panel.  As soon as a result is returned, it is removed.
     */
    defaultPanel: null,

    /**
     * Property: defaultPanel
     * {Object} The object used to create the panel displayed when the retuned
     *          query had no results to display.
     */
    noResultPanel: null,

    /**
     * Property: htmlInfoFormatRequests
     * {Array} An array of request urls that containt 'info_format' equal to 
     *         'text/html'.  These kind of requests are simply directly inside
     *         automatically created panels.
     */
    htmlInfoFormatRequests: [],
    
    /**
     * Constructor: OpenLayers.ResultExtGrid
     * Create a new ResultExtGrid renderer
     *
     * Parameters:
     * options - {Object} An optional object whose properties will be set on
     *     this instance.
     */
    initialize: function(options) {
        OpenLayers.Util.extend(this, options);

        this.defaultPanel = {
                                'html'  : this.i18n_default_panel_html,                                
                                 title  : this.i18n_default_panel_title,
                                 border : false
                            };
                            
        this.noResultPanel = {
                                'html'  : this.i18n_no_result_panel_html,                                
                                 title  : this.i18n_no_result_panel_title,
                                 border : false
                            };                     
        
        switch(this.drawMode) {
          case "extjs":
          case "mapfish":
          case "geoext":
            var oPanelOptions = {
                'border': false,
                region: "center",
                autoScroll: true,
                enableTabScroll: true,
                id: this.widgetName+"_panel",
                items: [this.defaultPanel]
            };
            if(this.inWindow === false){
                // Todo : validate that code is usefull
                oPanelOptions['title'] = this.i18n_query_result;
            }

            this.panel = new Ext.TabPanel(oPanelOptions);
            break;
          default:
        }
    },

    setQuery: function(query){
        this.query = query;
    },
    
    getResourceByLayer: function(szLayer, szServiceType){
        var szResourceName = 
            this.query.getResourceNameByLayer(szLayer, szServiceType);

        if(!szResourceName){
            return null;
        }

        for(var i=0; i<this.resources.length; i++)
        { 
            var oResource = this.resources[i];
            if(oResource.resource == szResourceName){
                return oResource;
            }
        } 

        return null;  
    },

    /**
     * Method: resetPanel
     * Called by the query as soon as the user clicks the map.  It adds the
     * defaultPanel and removes all other components from this.panel.
     *
     * options     - {<Object>} Hash of options.  Possible keys are :
     *               - modifiers : the query modifiers
     */
    resetPanel: function(options) {
        options = options || {};
        this.panel.add(this.defaultPanel);
        while(this.panel.items.length != 1){
            var oItem = this.panel.items.items[0];
            this.panel.remove(oItem, true);
        }
    },

    /**
     * Method: showResult
     * Called by the query as soon as all responses were parses to features.
     * First clean this.panel to reset the default values, then prepare the
     * data to be displayed in Ext.GridPanels, one per server-side layer.
     *
     * Parameters:
     * features    - {Array of <OpenLayers.Feature.Vector>} 
     * htmlResults - {Array of <Object>} Objects returned by queries using
     *                                   'info_format' equal to 'text/html'.
     */
    showResult: function(features, htmlResults){
        // Stores creation  
        var aoStores = {}, aoColumns = {}, nStores = 0;
        for(var i=0; i<features.length; i++)
        {
            var oFeature = features[i];
            var szType = oFeature.type; // layername, WMSGetFeatureInfo only
            var resource, resourceName;

            if (oFeature.resource) {
                resource = this.getResource(oFeature.resource);
            } else {
                resource = this.getResourceByLayer(szType, "wms");
            }

            if (resource === null){
                continue;
            } else {
                resourceName = resource.resource;
            }
            
            var aFields = [], aColumns = [];

            // if 'fields' is a string, that means we use all the fields from
            // the features
            if (typeof resource.fields === "string") {
                for (var szAttrKey in oFeature.attributes) {
                    var szAttrValue = oFeature.attributes[szAttrKey];
                    aFields.push({name: szAttrKey, type: "string"});
                    aColumns.push({
                        header: szAttrKey,
                        sortable: true,
                        dataIndex: szAttrKey
                    });
                }
            } else {
                for(var j=0; j<resource.fields.length; j++)
                { 
                    var field = resource.fields[j];

                    // field for SimpleStore
                    var oField = { name: field.id, type: field.type };
                    aFields.push(oField);

                    // column for GridPanel
                    var oColumn = {header: field.label, width: field.width, sortable: true, dataIndex: field.id};
                    aColumns.push(oColumn);
                }
            }    

            if(aFields.length > 0){
                aoStores[resourceName] = new Ext.data.SimpleStore({fields: aFields});
                aoStores[resourceName].resource = resource;
                aoColumns[resourceName] = aColumns;
                nStores++;
            }
        }

        if (nStores > 0) {
            for (var i=0; i<features.length; i++){
                var oFeature = features[i];
                resource = this.getResource(oFeature.resource);
                if (aoStores[resource.resource] != null)
                { 
                    aoStores[resource.resource].add([new Ext.data.Record(oFeature.attributes)]);
                }
            }

            // grids creation
            var aoGrids = {};
            for (var resourceName in aoStores){
                resource = aoStores[resourceName].resource;

                if (resource.delegatecontext && resource.delegatecontext.enabled)
                {
                    aoGrids[resourceName] = new Ext.grid.GridPanel({
                            store: aoStores[resourceName],
                            forceFit: false,
                            columns: aoColumns[resourceName],
                            title: resource.displayname,
                            stripeRows: true,
                            trackMouseOver: true,
                            tbar: [new Ext.Toolbar.Button({
                                    gridindex: resourceName,
                                    resource: resource,
                                    text: resource.delegatecontext.label,
                                    handler: function(param1, param2){ 
                                        var selected = aoGrids[param1.gridindex].getSelectionModel().getSelected(); 
                                        if (selected == null)
                                        {                                    
                                            Ext.MessageBox.show(
                                                                {
                                                                    title: this.i18n_message_select_row_title,
                                                                    msg: this.i18n_message_select_row_msg,
                                                                    buttons: Ext.MessageBox.OK,
                                                                    icon: Ext.MessageBox.WARNING
                                                                });    
                                        }
                                        else
                                        {
                                            var strJSON = new OpenLayers.Format.JSON().write(selected.data, true);
                                            var resourceName = param1.resource.resource;
                                            //alert('resourcename: '+resourceName+'\n\r\n\rdata: '+ strJSON);
                                            
                                            oGPDelegateFeature.fireEvent("onFeatureClick", {resourceName: resourceName, data: strJSON});   
                                        }
                                },
                                scope : this
                            })],
                            sm: new Ext.grid.RowSelectionModel({singleSelect:true})
       
                            
                    });  
                }
                else
                {
                    aoGrids[resourceName] = new Ext.grid.GridPanel({
                        store: aoStores[resourceName],
                        forceFit: false,
                        columns: aoColumns[resourceName],
                        title: resource.displayname,
                        stripeRows: true
                    }); 
                }
            
            }

            // add GridPanels to the panel
            for (var resourceName in aoStores){
                this.panel.add(aoGrids[resourceName]).show();
                this.panel.setActiveTab(aoGrids[resourceName]);
            }
        }

        // create and add panels containing the 'htmlResults'
        for (var i=0, len=htmlResults.length; i<len; i++) {
            var panelTitle = (htmlResults[i]['resourceTitle'] != "")
                ? htmlResults[i]['resourceTitle'] : htmlResults[i]['resource'];
            var oHTMLPanel = new Ext.Panel({
                  title: panelTitle,
                        html: htmlResults[i]['html'],
                        autoScroll: true,
                        overflow: true
            });
            this.panel.add(oHTMLPanel).show();
            this.panel.setActiveTab(oHTMLPanel);
        }

        // if no stores were created and we also don't have any htmlResults,
        // that means that there's nothing to display
        if(nStores == 0 && htmlResults.length == 0) {
            this.panel.add(this.noResultPanel);
            this.panel.remove(this.panel.items.items[0], true);
        } else {
            // remove the default panel before showing the result
            this.panel.remove(this.panel.items.items[0], true);
        }

        this.showPanel();
    },

    /**
     * Method: showPanel
     * Called by this.showResult when the panel received all its new results or
     * when an error occurs, like "there's no result to display".
     *
     * The results are displayed in a window if inWindow:true else in 
     * this.panel.ownerCt
     *
     * Parameters:
     * this.panel - {Ext.TabPanel} 
     */
    showPanel: function(){
        if(this.inWindow){
            /**
             * The normal way would have been to create the window object only
             * once and remove its items ( like what we're doing to the panel )
             * but because of an bug in IE, we create a brand new one that hide
             * on close and is destroyed once an other one appears.
             */
            var oResultWindow = new Ext.Window({
                  title    : this.i18n_window_title,
                  layout: 'fit',
                  closable : true,
                  closeAction: 'hide',
                  width    : 800,
                  height   : 600,
                  border : false,
                  modal: true,
                  plain    : true,
                  resizable : false,
                  autoScroll: true,
                  constrain: true,
                  region: 'center',
                  items: [this.panel]
            });
            oResultWindow.show();

            if(this.oldWindow){ // IE bug fix
                this.oldWindow.destroy();
                this.oldWindow = oResultWindow;
            }
        } else {
            this.panel.doLayout();
            this.panel.expand();

            // if parent panel is collapsed, expand it also
            if (this.panel.ownerCt){
                var owner = this.panel.ownerCt;
                    owner.expand();
                if(owner.activeTab){
                    owner.setActiveTab(this.widgetName+"_panel");
                }
            }
        }
    },

    /**
     * Method: getResource
     * Returns the resource object of this widget having a given name.  If not
     *     found, returns false.
     *
     * Parameters:
     * resourceName - {String} The name of the resource to find
     *
     * Returns:
     * {Object} The resource
     */
    getResource: function(resourceName) {
        for (var i=0, len=this.resources.length; i<len; i++) {
            if (this.resources[i].resource === resourceName) {
                return this.resources[i];
            }
        }

        return false;
    },
    
    CLASS_NAME: "OpenLayers.ResultExtGrid"
});
