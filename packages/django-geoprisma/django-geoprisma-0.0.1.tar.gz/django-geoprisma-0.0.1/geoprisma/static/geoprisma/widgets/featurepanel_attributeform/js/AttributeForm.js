/* 
   Copyright (c) 2011- MapGears Inc., published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
Ext.namespace("org.GeoPrisma.FeaturePanel.AttributeForm");

org.GeoPrisma.FeaturePanel.AttributeForm = Ext.extend(Ext.form.FormPanel, {

    /*
        const: i18n_form_button_commit_text
        {String} Button text
    */
    i18n_form_button_commit_text : "Commit",
    
    /*
        const: i18n_form_button_commit_tooltip
        {String} Button tooltip
    */
    i18n_form_button_commit_tooltip : "Commit current modifications",
    
    /*
        const: i18n_form_button_cancel_text
        {String} Button text
    */
    i18n_form_button_cancel_text : "Cancel",
    
    /*
        const: i18n_form_button_cancel_tooltip
        {String} Button tooltip
    */
    i18n_form_button_cancel_tooltip : 'Cancel current modifications.  Geometry isn\'t reset.',
    
    /**
     * Property: DEFAULT_WINDOW_OFFSET
     * {Object} The default offset value in pixels of the window.
     */
    DEFAULT_WINDOW_OFFSET: {
        "left": 45,
        "right": 0,
        "top": 30,
        "bottom": 0
    },

    /**
     * Property: DEFAULT_WINDOW_OPTIONS
     * {Object} The default options of the window to be opened
     */
    DEFAULT_WINDOW_OPTIONS: {
        layout: 'fit',
        closable : false,
        closeAction: 'hide',
        width    : 300,
        height   : 300,
        border : false,
        modal: false,
        plain    : true,
        resizable : false,
        autoScroll: true,
        constrain: true,
        region: 'center'
    },

    /**
     * Property: DEFAULT_DEFAULTS
     * {String} Default default properties of the items of this FormPanel
     */
    DEFAULT_DEFAULTS: {
        width: 150,
        editable: false,
        mode: 'local',
        triggerAction: 'all',
        lazyRender: true,
        lazyInit: false,
        listWidth: 150,
        xtype: "textfield"
    },

    /**
     * APIProperty: mappanelid
     * {String} The id of the GeoExt.MapPanel that contains the OpenLayers.Map
     */
    mappanelid: null,

    /**
     * APIProperty: singlefeature
     * {boolean} True if only one feature is displayed at a time, i.e. not 
     *           bbar with previous/next feature.
     */
    singlefeature: true,

    /**
     * APIProperty: owners
     * {Array(<Objects>)} Array that contains the owners of this FeaturePanel.
     */
    owners: [],

    /**
     * Property: window
     * {Ext.Window} The window container created if if this.inwindow=true
     */
    window: null,

    /**
     * APIProperty: windowoffset
     * {Object} The offset value in pixels of the window.
     */
    windowoffset: {},

    /**
     * APIProperty: windowoptions
     * {Object} The options of the window to be opened
     */
    windowoptions: {},

    /**
     * APIProperty: labelWidth
     * {Integer} Default labelWidth property for this FormPanel
     */
    labelWidth: 120,

    /**
     * APIProperty: bodyStyle
     * {String} Default bodyStyle property for this FormPanel
     */
    bodyStyle:'padding:5px 5px 0',

    /**
     * APIProperty: defaults
     * {String} Default properties of the items of this FormPanel
     */
    defaults: {},

    /**
     * APIProperty: inwindow
     * {Boolean} Whether to display the form in a window or not
     */
    inwindow: true,

    /**
     * Property: commiting
     * {Boolean} Used to validate commits made from this FormPanel.
     */
    commiting: false,

    /**
     * APIProperty: builder
     * {org.GeoPrisma.FeaturePanel.AttributeFormBuilder} The builder
     */
    builder: null,

    /** private: method[constructor]
     *  Private constructor override.
     */
    constructor: function(config) {
        
        this.buttons = [{
            text: this.i18n_form_button_commit_text,
            tooltip: this.i18n_form_button_commit_tooltip,
            handler: function(){
                var featurePanel;

                // ExtJS 2.2.1
                if(this.ownerCt.CLASS_NAME == "org.GeoPrisma.FeaturePanel.AttributeForm") {
                    featurePanel = this.ownerCt;
                // ExtJS 3.0.0
                } else if (this.ownerCt.ownerCt.CLASS_NAME ==
                           "org.GeoPrisma.FeaturePanel.AttributeForm"){
                    featurePanel = this.ownerCt.ownerCt;
                } else {
                    return false;
                }

                featurePanel.commit();
                featurePanel.getActiveOwner().getSelectControl().unselectAll();
            }
        },{
            text: this.i18n_form_button_cancel_text,
            tooltip: this.i18n_form_button_cancel_tooltip,
            handler: function(){
                var featurePanel;

                // ExtJS 2.2.1
                if(this.ownerCt.CLASS_NAME == "org.GeoPrisma.FeaturePanel.AttributeForm") {
                    featurePanel = this.ownerCt;
                // ExtJS 3.0.0
                } else if (this.ownerCt.ownerCt.CLASS_NAME ==
                           "org.GeoPrisma.FeaturePanel.AttributeForm"){
                    featurePanel = this.ownerCt.ownerCt;
                } else {
                    return false;
                }

                featurePanel.getActiveOwner().getSelectControl().unselectAll();
            }
        }];

        config['defaults'] = config['defaults'] || [];
        OpenLayers.Util.applyDefaults(config['defaults'], this.DEFAULT_DEFAULTS);

        org.GeoPrisma.FeaturePanel.AttributeForm.superclass.constructor.apply(this, arguments);

        OpenLayers.Util.applyDefaults(this.windowoffset,
                                      this.DEFAULT_WINDOW_OFFSET);

        OpenLayers.Util.applyDefaults(this.windowoptions, 
                                      this.DEFAULT_WINDOW_OPTIONS);

    },

    /**
     * Method: addOwner
     * Called right after this FeaturePanel has been added to an owner.  The
     * owner is added to this.owners.
     *
     * Parameters:
     * Owner - {<OpenLayers.Control.*>} Can be :
     *                                  - EditFeature_Create
     *                                  - EditFeature_Update
     */
    addOwner: function(owner){
        this.owners.push(owner);
    },

    /**
     * Method: getActiveOwner
     * Return the current activated owner (OpenLayers.Control).
     *
     * Returns
     * activeOwner - {<OpenLayers.Control.*>} Can be :
     *                                  - EditFeature_Create
     *                                  - EditFeature_Update
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
     * Method: setSingleFeature
     * Set the singlefeature property.  Can be true or false.  Set by owner.
     *
     * Parameters:
     * singlefeature - {boolean} 
     */
    setSingleFeature: function(singlefeature) {
        this.singlefeature = singlefeature;
    },

    /**
     * Method: showFeaturePanel
     * Called by an owner.  Displays this panel.  If it's in a window, display
     * it.
     *
     * N.B. currently supports only ONE feature
     *
     * Parameters:
     * features - {Array(<OpenLayers.Vector.Feature>)}
     */
    showFeaturePanel: function(features) {

        // currently support one single feature only
        if(!this.singlefeature) {
            return false;
        }

        if(this.singlefeature === true) {
            var feature = features[0];

            if(feature.state != OpenLayers.State.INSERT){
                this.parseFeatureAttributesToFormFields(feature);
            }
        }

        if(this.inwindow){
            // create the window object if it's the first time
            if(!this.window){
                this.windowoptions['items'] = [this];
                this.window = new Ext.Window(this.windowoptions);
            }

            //this.setWindowPosition(features);
            this.window.show();
        } else {
            this.doLayout();
            this.expand();

            // if parent panel is collapsed, expand it also
            if (this.ownerCt){
                this.ownerCt.expand();
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

    /**
     * Method: hideFeaturePanel
     * Called by an owner.  Reset the form and hide this.window (if container
     * is a window.
     */
    hideFeaturePanel: function() {
        this.commiting = false;
        this.builder.commiting = false;

        this.getForm().reset();

        if(this.inwindow){
            this.window.hide();
        }
    },

    /**
     * Method: parseFeatureAttributesToFormFields
     * Copy each feature attributes in this form if it has a corresponding form
     * field.
     *
     * N.B. currently supports only ONE feature
     *
     * Parameters:
     * feature - {<OpenLayers.Vector.Feature>} The feature to be edited
     */
    parseFeatureAttributesToFormFields: function(feature) {
        var aoElements, nElements;
        aoElements = this.items.items;
        nElements = aoElements.length;

        for (var i=0; i<nElements; i++){
            var oElement = aoElements[i];
            var szAttribute = oElement.getName();
            var szValue = null;
            if (oElement.initialConfig.isfid)
            { 
                szValue = feature.fid;              
            }
            else  
            { 
                szValue = feature.attributes[szAttribute];
            }
            oElement.setValue(szValue);
        }
    },

    /**
     * Method: parseFormFieldsToFeatureAttributes
     * Copy each form field value to its corresponding feature attribute.
     *
     * N.B. currently supports only ONE feature
     *
     * Parameters:
     * feature - {<OpenLayers.Vector.Feature>} The feature that was edited
     */
    parseFormFieldsToFeatureAttributes: function(feature){
        var field, id, value;

        for(var i=0; i<this.items.length; i++){
            field = this.items.get(i);
            id = field.getName();
            value = field.getValue();
            feature.attributes[id] = value;
        }
    },

    /**
     * Method: parseFormFieldsToFeatureAttributes
     * Called when the user click this form "Commit" button.  Get the current
     * selected feature, apply the modified attribute values and call
     * this.owner.commit function.
     *
     * N.B. currently supports only ONE feature
     */
    commit: function() {
        var owner = this.getActiveOwner();
        var features = owner.getSelectedFeatures();
        var feature = features[0];

        if(feature.state != OpenLayers.State.INSERT) {
            feature.state = OpenLayers.State.UPDATE;
        }

        this.parseFormFieldsToFeatureAttributes(feature);

        this.commiting = true;
        this.builder.commiting = true;

        owner.commit([feature]);
    },

    CLASS_NAME: "org.GeoPrisma.FeaturePanel.AttributeForm"
});

Ext.reg('gp_featurepanel_attributeform', org.GeoPrisma.FeaturePanel.AttributeForm);
