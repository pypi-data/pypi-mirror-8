/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
Ext.namespace("org.GeoPrisma.FeaturePanel");

org.GeoPrisma.FeaturePanel.Selector = Ext.extend(Ext.grid.GridPanel, {

    /*
        const: i18n_button_delegate
        {String} Delegate Context button        
    */
    i18n_button_delegate : "Consult", 

    /*
        const: i18n_featurepanel_selector_grid_title
        {String} GridPanel title        
    */
    i18n_featurepanel_selector_grid_title : "Result", 

    /*
        const: i18n_featurepanel_selector_no_context_title
        {String} No context error title       
    */
    i18n_featurepanel_selector_no_context_title : "Warning", 

    /*
        const: i18n_featurepanel_selector_no_context_message
        {String} No context error message        
    */
    i18n_featurepanel_selector_no_context_message : "No more info", 
	
    /**
     * APIProperty: featureConfigs
     */
    featureConfigs: [],
	
    /**
     * APIProperty: features
     * {Array(<Objects>)} Array that contains the features of the last request.
     */
    features: [],

    /**
     * APIProperty: owners
     * {Array(<Objects>)} Array that contains the owners of this FeaturePanel.
     */
    owners: [],

    /**
     * APIProperty: cls
     * {String} Default cls value for this widget
     */
    cls: "gp_featurepanel_selector_grid",

    /**
     * APIProperty: border
     * {Boolean} Default border value for this widget
     */
    border: false,

    /**
     * APIProperty: firstTwoRowCSS
     * {String} The css class to use for the first two rows : consult and title
     */
    firstTwoRowCSS: "x-combo-list",

    /**
     * APIProperty: autoExecuteContext
     * {Boolean} If only one feature is returned and has a context set, auto
     *           execute it.
     */
    autoExecuteContext: true,

    /**
     * APIProperty: consultColumnOptions
     * {Object} Used to override the default 'consult' column options.
     */
    consultColumnOptions : {},

    /**
     * APIProperty: titleColumnOptions
     * {Object} Used to override the default 'title' column options.
     */
    titleColumnOptions : {},

    /** private: method[constructor]
     *  Private constructor override.
     */
    constructor: function(config) {
        var aFields = [];
        var aData = [];
        var aHeaderFields = ["gpfps_consult", "gpfps_title"];
        var aTotalFields = [];
		
        for (var i=0; i<config["nbcolumns"]; i++)
        {
            aFields.push("field" + i);
        }

        var store = new Ext.data.SimpleStore({
            fields: aTotalFields.concat(aHeaderFields,aFields),
            data : aData
        });
        config['store'] = store;
        config['columns'] = [];
        config['sm'] = new Ext.grid.RowSelectionModel({singleSelect:true});

        // action column - "consult"
        config['columns'].push(Ext.applyIf(this.consultColumnOptions, {
            width: 65,
            xtype: 'actioncolumn',
            id: aHeaderFields[0],
            resizable : false,
            fixed : false,
            hideable : false,
            sortable: false,
            menuDisabled: true,
            scope: this,
            css: 'border:solid 0px;',
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
				metaData.css = this.firstTwoRowCSS;
			
                var resource = this.features[rowIndex].resource;
                if (!this.featureConfigs[resource].options.method &&
                    !this.featureConfigs[resource].options.template)
                {
                    metaData.attr = 'style="display:none;"';
                }
            },
            iconCls: 'gp_featurepanel_selector_consult_button',
            handler: function(grid, rowIndex, colIndex) {
                this.formCallBack(this.features[rowIndex]);
            }
        }));

        // title column
        config['columns'].push(Ext.applyIf(this.titleColumnOptions, {
            width: 150,
            id: aHeaderFields[1],
            fixed : false,
            hideable : false,
            sortable: false,
            menuDisabled: true,
            scope: this,
            css: 'border:solid 0px;',
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
				metaData.css = this.firstTwoRowCSS;
                var html = [];
                var resource = this.features[rowIndex].resource;
                html.push('<div class="gp_featurepanel_selector_title_col">');
                html.push(this.featureConfigs[resource].titleColumn);
                html.push('</div>');
                return html.join("");
            }
        }));

        // For each field, create a column
        for(var i=0; i<aFields.length; i++)
        {
            config['columns'].push({
                id: aFields[i],
                sortable: false,
                menuDisabled: true
            });
        }

        org.GeoPrisma.FeaturePanel.Selector.superclass.constructor.apply(this, arguments);

        // "consult" on rowdblclick
        this.on("rowdblclick", function(grid, rowIndex, event) {
            this.formCallBack(this.features[rowIndex]);
        }, this);
    },

    /**
     * Method: addOwner
     * Called right after this FeaturePanel has been added to an owner.  The
     * owner is added to this.owners.
     *
     * Parameters:
     * Owner - {<OpenLayers.Control.*>} Can be :
     *                                  - QueryOnClick
     */
    addOwner: function(owner){
        this.owners.push(owner);
    },

    /**
     * Method: formCallBack
     * Called by the delegatecontext button.
     *
     * Parameters:
     * object - {<OpenLayers.Record>} : data from selected feature
     */
    formCallBack: function(object){
        if (typeof object != 'undefined')
        {
            if (!this.featureConfigs[object.resource].options["width"]){ this.featureConfigs[object.resource].options.width = 500; }
            if (!this.featureConfigs[object.resource].options["height"]){ this.featureConfigs[object.resource].options.height = 500; }

            var windowOptions = {
                title : this.i18n_featurepanel_selector_grid_title,
                id: 'FeaturePanelSelectorQueryFormWindow',
                layout: 'fit',
                closable : true,
                width    : this.featureConfigs[object.resource].options.width,
                height   : this.featureConfigs[object.resource].options.height,
                border : false,
                modal: true,
                plain    : true,
                resizable : false,
                autoScroll: true,
                constrain: true,
                region: 'center'
            };

            if(this.featureConfigs[object.resource].options.template)
            {
                var formUrl = baseUrl + this.featureConfigs[object.resource].options.template+"?resource="+object.resource+"&fid="+object.fid;
                var oData = object.data;
                var params = [];

                for (var field in oData){
                    params.push(String.fromCharCode(38));
                    params.push(escape(field));
                    params.push("=");
                    params.push(escape(oData[field]));
                }

                windowOptions.autoLoad = {url: formUrl, scripts: true, params: params.join("")};
            }
            else if(this.featureConfigs[object.resource].options.method && Ext.isFunction(this.featureConfigs[object.resource].options.method))
            {
                windowOptions.items = [this.featureConfigs[object.resource].options.method(object.resource, object.fid)];
            }
            else
            {
                Ext.MessageBox.show({
                    title: this.i18n_featurepanel_selector_no_context_title,
                    msg: this.i18n_featurepanel_selector_no_context_message,
                    buttons: Ext.MessageBox.OK,
                    icon: Ext.MessageBox.WARNING
                });
                return;
            }

            var oFeaturePanelSelectorQueryFormWindow = new Ext.Window(windowOptions);
            oFeaturePanelSelectorQueryFormWindow.show();
        }
        else
        {
            Ext.MessageBox.show({
                title: this.i18n_featurepanel_selector_no_context_title,
                msg: this.i18n_featurepanel_selector_no_context_message,
                buttons: Ext.MessageBox.OK,
                icon: Ext.MessageBox.WARNING
            });
        }
    },

    /**
     * Method: getActiveOwner
     * Return the current activated owner (OpenLayers.Control).
     *
     * Returns
     * activeOwner - {<OpenLayers.Control.*>} Can be :
     *                                  - QueryOnClick
     */
    getActiveOwner: function(){
        for(var i=0, len=this.owners.length; i<len; i++) {
            owner = this.owners[i];
            if(owner.active) {
                return owner;
            }
        }

        return false;
    },

    /**
     * Method: showFeaturePanel
     * Called by an owner.  Displays this panel.
     *
     * Parameters:
     * features - {Array(<OpenLayers.Vector.Feature>)}
     */
    showFeaturePanel: function(features) {
        // remove current store data and populate
        this.store.removeAll();
        this.features = features;
        for (var i=0, nLen = features.length; i<nLen; i++){
            var rFeature = {};
            if (this.featureConfigs[features[i].resource])
            {
                this.features[i].fid = features[i].attributes[this.featureConfigs[features[i].resource].options.fid];
                for (var j=0, nbFields=this.featureConfigs[features[i].resource].options.fields.length; j<nbFields; j++)
                {
                    if (this.featureConfigs[features[i].resource].options.fields[j].type == "key")
                    {
                        if (this.featureConfigs[features[i].resource]['fieldTitlesByName'][this.featureConfigs[features[i].resource].options.fields[j].name])
                        {
                            rFeature["field" + j] = this.featureConfigs[features[i].resource]['fieldTitlesByName'][this.featureConfigs[features[i].resource].options.fields[j].name];
                        }
                        else
                        {
                            rFeature["field" + j] = this.featureConfigs[features[i].resource].options.fields[j].name;
                        }
                    }
                    else
                    {
                        rFeature["field" + j] = features[i].attributes[this.featureConfigs[features[i].resource].options.fields[j].name];
                    }
                }
            }
			
            this.store.add([new Ext.data.Record(rFeature)]);
        }
		
        this.doLayout();
        this.expand();

        // if parent panel is collapsed, expand it also
        if (this.ownerCt){
            this.ownerCt.show();
            this.ownerCt.expand();
        }

        // if only one record and it has a context, execute it.
        if (this.autoExecuteContext &&
            features.length == 1 &&
            (this.featureConfigs[features[0].resource].options.template ||
             this.featureConfigs[features[0].resource].options.method)) {
            this.formCallBack(features[0]);
            if (this.ownerCt && this.ownerCt instanceof Ext.Window) {
                this.ownerCt.hide();
            }
        }
    },

    /**
     * Method: setWindowPosition
     * Sets the position of the window so that it's the farest away form the
     * selected feature(s) to be able to see them.  Called just before showing
     * window.
     *
     * The position is relative to the GeoExt.MapPanel.  Its id must be set to
     * 'gp'+MapName, like : 'gpDefaultMap'.
     *
     * N.B. currently supports only ONE feature
     *
     * Parameters:
     * features - {Array(<OpenLayers.Vector.Feature>)}
     */
    setWindowPosition: function(features) {
        var oMapPanel = Ext.get(this.mappanelid);
        var oMap, feature, oMapCenter, oFeatureCenter, nWinXPos, nWinYPos;

        // currently supports only one feature
        if(this.singlefeature === true) {
            feature = features[0];
        }
        oMap = feature.layer.map;

        // Get the map and feature center
        oMapCenter = oMap.getExtent().getCenterPixel();
        oFeatureCenter = feature.geometry.getBounds().getCenterPixel();

        // X positioning
        if (oFeatureCenter.x >= oMapCenter.x) { // left
            nWinXPos = oMapPanel.getLeft() + this.windowoffset['left'];
        } else { // right
            nWinXPos = oMapPanel.getLeft() + oMap.getSize().w 
                - this.window.width - this.windowoffset['right'];
        }

        // Y positioning
        if (oFeatureCenter.y >= oMapCenter.y) { // bottom
            nWinYPos = oMapPanel.getTop() + oMap.getSize().h 
                - this.window.height - this.windowoffset['bottom'];

        } else { // top
            nWinYPos = oMapPanel.getTop() + this.windowoffset['top'];
        }
        
        this.window.setPosition(nWinXPos,nWinYPos);
    },

    CLASS_NAME: "org.GeoPrisma.FeaturePanel.Selector"
});

Ext.reg('gp_featurepanel_selector', org.GeoPrisma.FeaturePanel.Selector);
