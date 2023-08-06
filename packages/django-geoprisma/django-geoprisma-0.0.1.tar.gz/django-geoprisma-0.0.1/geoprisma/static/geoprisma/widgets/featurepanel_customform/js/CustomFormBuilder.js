Ext.namespace("org.GeoPrisma.FeaturePanel");

org.GeoPrisma.FeaturePanel.CustomFormBuilder = Ext.extend(Ext.util.Observable, {

    CUSTOM_FORM_ID: 'featurepanel_customform_id',

    singlefeature: true,

    owners: null,

    resourceFields: null,

    constructor: function(config) {
        config = config || {};
        Ext.apply(this, config);

        this.owners = [];
        this.resourceFields = {};

        org.GeoPrisma.FeaturePanel.CustomFormBuilder.superclass.constructor.apply(this, arguments);
    },

    addOwner: function(owner) {
        this.owners.push(owner);
    },

    setSingleFeature: function(singlefeature) {
        this.singlefeature = singlefeature;
    },

    showFeaturePanel: function(features, owner) {
        var feature = features[0];
        // vector layers always have only one resource
        var resource = feature.layer.resources[0];
        var options = {id: this.CUSTOM_FORM_ID, autoLoad: {
            url: this.getFullRequestString(feature, owner),
            scripts: true
        }};
        var customform = new org.GeoPrisma.FeaturePanel.CustomForm(options);
        customform.addOwner(owner);
        feature.featurepanel_customform = customform;
        customform.showFeaturePanel([feature]);
    },
        
    getActiveOwner: function(){
        for(var i=0, len=this.owners.length; i<len; i++) {
            owner = this.owners[i];
            if(owner.active) {
                return owner;
            }
        }

        return false;
    },

    hideFeaturePanel: function(feature) {
        if (feature.featurepanel_customform) {
            feature.featurepanel_customform.hideFeaturePanel();
        }
    },

    getFullRequestString: function(feature, owner) {
        return OpenLayers.Util.urlAppend(
            this.formURL, OpenLayers.Util.getParameterString({
                'osmfeaturefid': feature.fid,
                'osmresource': owner.resource,
                'osmcustomformid': this.CUSTOM_FORM_ID
            })
        );
    }

});

Ext.reg(
    'gp_featurepanel_customformbuilder',
    org.GeoPrisma.FeaturePanel.CustomFormBuilder
);

