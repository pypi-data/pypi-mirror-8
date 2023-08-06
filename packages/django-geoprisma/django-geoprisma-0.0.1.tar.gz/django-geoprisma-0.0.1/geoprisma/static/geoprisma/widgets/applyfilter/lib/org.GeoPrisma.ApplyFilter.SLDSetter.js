/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.ApplyFilter");

/** api: (define)
 *  module = org.GeoPrisma.ApplyFilter
 *  class = SLDSetter
 */

/** api: constructor
 *  .. class:: SLDSetter
 */
org.GeoPrisma.ApplyFilter.SLDSetter = Ext.extend(Ext.util.Observable, {

    // Public Properties (Mandatory)

    /** api: property[layer]
     *  :class:``OpenLayers.Layer.WMS``
     *  The WMS layer object in which to set the SLD
     */
    layer: null,

    /** api: property[layerName]
     *  ``String``
     *  The layer name param (from WMS DataStore)
     */
    layerName: null,

    /** api: property[name]
     *  :class:`OpenLayers.Map`
     *  A reference to the Map object.
     */
    map: null,

    /** api: property[originalSLD]
     *  ``Object``
     *  Contains the original style layer descriptor for the WMS layer.  Used
     *  to get the same style when applying a new SLD filter.
     */
    originalSLD: null,

    /** api: property[format]
     *  :class:``OpenLayers.Format.SLD``
     *  Used to write SLD document strings when applying a new SLD filter.
     */
    format: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
    },

    /** public: method[triggerFilterRequest]
     *  :param filter: :class:``OpenLayers.Filter``
     *
     *  Creates a sld document string out of a filter and apply it.
     */
    triggerFilterRequest: function(filter) {
        this.setSLD(this.createSLD(filter));
    },

    /** public: method[triggerFilterRequest]
     *  :param filter: :class:``OpenLayers.Filter``
     *  :return: ``String`` The SLD document string created
     *
     *  Creates a sld document string out of a filter.
     */
    createSLD: function(filter) {
        filter = filter || new OpenLayers.Filter();

        var sld = {version: "1.0.0", namedLayers: {}};

            var name = this.layerName;
            sld.namedLayers[name] = {name: name, userStyles: []};
            var rules = [];

            Ext.each(this.getOriginalRules(), function(oRule, index, oRules) {
                var cloneRule = oRule.clone();
                if (oRule.filter) {
                    cloneRule.filter = new OpenLayers.Filter.Logical({
                        type: OpenLayers.Filter.Logical.AND,
                        filters: [filter.clone(), oRule.filter.clone()]
                    });
                } else {
                    cloneRule.filter = filter.clone();
                }
                rules.push(cloneRule);

            }, this);
            
            sld.namedLayers[name].userStyles.push({
                name: 'default',
                rules: rules
            });

        return this.format.write(sld);
    },

    /** public: method[getOriginalRules]
     *  :return: ``Array``
     *  
     *  Get the rules for the first user style defined in original SLD object.
     */
    getOriginalRules: function() {
        return this.originalSLD.namedLayers[this.layerName].userStyles[0].rules;
    },

    /** public: method[resetSLD]
     *  Set current SLD as an empty string, thus reseting it.
     */
    resetSLD: function() {
        this.setSLD("");
    },

    /** public: method[setSLD]
     *  :param sld: ``String`` The SLD document to apply to the layer
     *
     *  Set the SLD_BODY parameter of the layer and force redrawing it.
     */
    setSLD: function(sld) {
        this.layer.mergeNewParams({SLD_BODY: sld});
        this.layer.redraw(true);
    }
});
