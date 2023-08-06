/* 
   Copyright (c) 2011- Mapgears Inc., published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
Ext.namespace("org.GeoPrisma.FeaturePanel.CustomForm");

org.GeoPrisma.FeaturePanel.CustomForm = Ext.extend(Ext.Window, {
    
    width: 500,

    height: 500,

    border: false,

    modal: false,

    resizable: false,

    autoScroll: true,

    constrain: true,

    bottomToolbarOptions: null,

    /**
     * APIProperty: owners
     * {Array(<Objects>)} Array that contains the owners of this FeaturePanel.
     */
    owners: [],

    /**
     * Property: commiting
     * {Boolean} Used to validate commits made from this FormPanel.
     */
    commiting: false,

    /** private: method[constructor]
     *  Private constructor override.
     */
    constructor: function(config) {
        Ext.apply(this, config);
        var bottomToolbarOptions =
            this.bottomToolbarOptions || {buttonAlign: 'right'};
        Ext.apply(this, {bbar: new Ext.Toolbar(bottomToolbarOptions)});
        org.GeoPrisma.FeaturePanel.CustomForm.superclass.constructor.apply(this, arguments);
        this.on("beforeclose", this.onBeforeClose, this);
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
        var feature = features[0];

        // copy features info to form here...

        this.show();
    },

    /**
     * Method: hideFeaturePanel
     * Called by an owner.  Reset the form and hide this.window (if container
     * is a window.
     */
    hideFeaturePanel: function() {
        this.commiting = false;
        this.close();
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

        // copy stuff to feature here

        this.commiting = true;

        owner.commit([feature]);
    },

    onBeforeClose: function(window) {
        var activeOwner = this.getActiveOwner();
        activeOwner && activeOwner.getSelectControl().unselectAll();
    },

    getSelectedFeature: function() {
        var feature;
        var owner = this.getActiveOwner();

        if (owner) {
            var features = owner.getSelectedFeatures();
            feature = features[0];
        }

        return feature;
    },

    CLASS_NAME: "org.GeoPrisma.FeaturePanel.CustomForm"
});

Ext.reg('gp_featurepanel_form', org.GeoPrisma.FeaturePanel.CustomForm);
