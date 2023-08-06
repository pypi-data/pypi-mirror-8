Ext.namespace("org.GeoPrisma.FeaturePanel");

org.GeoPrisma.FeaturePanel.AttributeFormBuilder = Ext.extend(Ext.util.Observable, {

    singlefeature: true,

    owners: null,

    resourceFields: null,

    constructor: function(config) {
        config = config || {};
        Ext.apply(this, config);

        this.owners = [];
        this.resourceFields = {};

        org.GeoPrisma.FeaturePanel.AttributeFormBuilder.superclass.constructor.apply(this, arguments);
    },

    addOwner: function(owner) {
        this.owners.push(owner);
    },

    setSingleFeature: function(singlefeature) {
        this.singlefeature = singlefeature;
    },

    showFeaturePanel: function(features, owner) {
        if(!this.singlefeature) {
            return false;
        }

        var feature = features[0];
        // vector layers always have only one resource
        var resource = feature.layer.resources[0];
        var attributeForm;

        if (!feature.layer.featurepanel_attributeform) {
            var options = {
                'items': this.getItemsFromResourceFields(resource),
                'builder': this
            };
            attributeForm =
                new org.GeoPrisma.FeaturePanel.AttributeForm(options);
            attributeForm.addOwner(owner);
        } else {
            attributeForm = feature.layer.featurepanel_attributeform;
            if (OpenLayers.Util.indexOf(attributeForm.owners, owner) == -1) {
                attributeForm.addOwner(owner);
            }
        }

        feature.featurepanel_attributeform = attributeForm;
        feature.layer.featurepanel_attributeform = attributeForm;

        attributeForm.showFeaturePanel([feature]);
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
        if (feature.featurepanel_attributeform) {
            feature.featurepanel_attributeform.hideFeaturePanel();
        }
    },

    getItemsFromResourceFields: function(resource) {
        var items = [];
        if (this.resourceFields[resource]) {
            var fields;

            if (this.resourceFields[resource]['field']) {
                fields = [this.resourceFields[resource]['field']];
            } else {
                fields = this.resourceFields[resource];
            }

            Ext.each(fields, function(field, index) {
                items.push({"name": field.name, "fieldLabel": field.title});
            });
        }
        return items;
    },

    addResourceFields: function(options) {
        this.resourceFields[options.resource] = options.fields;
    }

});

Ext.reg(
    'gp_featurepanel_attributeformbuilder',
    org.GeoPrisma.FeaturePanel.AttributeFormBuilder
);

