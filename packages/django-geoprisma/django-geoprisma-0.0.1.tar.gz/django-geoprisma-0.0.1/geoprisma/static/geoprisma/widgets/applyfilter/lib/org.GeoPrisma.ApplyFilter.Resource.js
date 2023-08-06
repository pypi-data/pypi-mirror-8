/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.ApplyFilter");

/** api: (define)
 *  module = org.GeoPrisma.ApplyFilter
 *  class = Resource
 */

/** api: constructor
 *  .. class:: Resource
 */
org.GeoPrisma.ApplyFilter.Resource = Ext.extend(Ext.util.Observable, {

    // Public Properties (Mandatory)

    /** api: property[defaultIgnoredFields]
     *  ``Array``
     *  An array of fields to ignore. Is automatically populated from the
     *  manager (widget) ignored fields.
     */
    defaultIgnoredFields: null,

    /** api: property[name]
     *  :class:`OpenLayers.Map`
     *  A reference to the Map object.
     */
    map: null,

    /** api: property[name]
     *  ``String``
     *  The resource name taken from GeoPrisma config
     */
    name: null,

    /** api: property[proxyURL]
     *  ``String``
     *  The url of the proxy.
     */
    proxyURL: null,

    /** api: property[wfsDescribeFeatureTypeResponseText]
     *  ``String``
     *  The response text of a WFS DescribeFeatureType query for this resource.
     *  Used to create the attribute store and the grid fields and columns.
     */
    wfsDescribeFeatureTypeResponseText: null,

    /** api: property[wfsLayerName]
     *  ``String``
     *  The layer name of the WFS Datastore.  Used as the "typename" property
     *  for the feature store.
     */
    wfsLayerName: null,

    /** api: property[wfsServiceName]
     *  ``String``
     *  The name of the WFS service used by this resource.
     */
    wfsServiceName: null,

    /** api: property[wmsGetStylesResponseText]
     *  ``String``
     *  The response text of a WMS GetStyles query for this resource.
     *  Used to get the original style descriptors for when applying a new SLD
     *  to the WMS Layer.
     */
    wmsGetStylesResponseText: null,

    /** api: property[wmsLayerName]
     *  ``String``
     *  The layer name of the WMS Datastore.
     */
    wmsLayerName: null,

    // Public Properties (Optional)

    /** api: property[fields]
     *  ``Object``
     *  Hash of fields taken from GeoPrisma config where the key equals to
     *  its name and value equals to a hash representing a field having the
     *  following possible keys :
     *  - name (String) The name of the field
     *  - title (String) The title of the field
     *  - options (Object) Hash of field options
     */
    fields: null,

    /** api: property[options]
     *  ``Object``
     *  Hash of options taken from the resource GeoPrisma config
     */
    options: null,

    /** api: property[maxFeatures]
     *  ``Integer``
     *  The maximum number of features each WFS GetFeature request should
     *  return.  It also sets the pageSize property of the grid.
     */
    maxFeatures: 10,

    /** api: property[maxZoomScale]
     *  ``Float``
     *  The maximum scale allowed to zoom in to.
     */
    maxZoomScale: null,

    /** api: property[styleMap]
     *  :class:``OpenLayers.StyleMap``
     *  A stylemap object to use instead of the one created by default.
     */
    styleMap: null,

    /** api: property[title]
     *  ``String``
     *  The resource title taken from GeoPrisma config
     */
    title: null,

    // Private Properties

    /** private: property[attributes]
     *  :class:`GeoExt.data.AttributeStore`
     *  Stores the attributes of the resource.  Obtained from a WFS 
     *  DescribeFeatureType request result string.
     */
    attributes: null,

    /** private: property[grid]
     *  :class:`org.GeoPrisma.ApplyFilter.WFSFeatureGrid`
     *  The grid panel used by this resource to dump results from WFS requests.
     */
    grid: null,

    /** private: property[sldSetter]
     *  :class:`org.GeoPrisma.ApplyFilter.SLDSetter`
     *  The SLDSetter object used by this resource.
     */
    sldSetter: null,

    /** private: property[vector]
     *  :class:``OpenLayers.Layer.Vector``
     *  The vector layer object created to draw features in current grid page.
     */
    vector: null,

    /** private: property[wmsLayerObject]
     *  :class:``OpenLayers.Layer.WMS``
     *  A reference to the WMS layer object having 'wms' service type.  Used for
     *  visibility toggling.
     */
    wmsLayerObject: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);

        this.defaultIgnoredFields = this.defaultIgnoredFields || [];
        this.fields = this.fields || {};
        this.options = (this.options && !Ext.isArray(this.options))
            ? this.options : {};
        this.createAttributeStore();
        this.createVectorLayer();
        this.createWFSFeatureGrid();
        this.findWMSLayerObject();
        this.createSLDSetter();
    },

    /** private: method[createAttributeStore]
     *  Creates a new GeoExt.data.AttributeStore object using the WFS
     *  DescribeFeatureType response text property of this resource.
     */
    createAttributeStore: function() {
        this.attributes = new GeoExt.data.AttributeStore({
            data: this.wfsDescribeFeatureTypeResponseText
        });
    },

    /** private: method[createSLDSetter]
     *  Creates a new org.GeoPrisma.ApplyFilter.SLDSetter object for this
     *  resource. Used to manage SLD requests of the WMS layer.
     */
    createSLDSetter: function() {
        var format = new OpenLayers.Format.SLD({
            srsName: this.map.getProjection()
        });
        this.sldSetter = new org.GeoPrisma.ApplyFilter.SLDSetter({
            map: this.map,
            // could do this in sld setter instead START...
            format: format,
            originalSLD: format.read(this.wmsGetStylesResponseText),
            // END
            layer: this.wmsLayerObject,
            layerName: this.wmsLayerName            
        });
    },

    /** private: method[createVectorLayer]
     *  Creates a new OpenLayers.Layer.Vector object for this resource and add
     *  it to the map. Used to highlight features on the current page of the
     *  grid.
     */
    createVectorLayer: function() {
        this.vector = new OpenLayers.Layer.Vector(this.getTitle(), {
            displayInLayerSwitcher: false,
            styleMap: this.styleMap || this.createStyleMap(),
            visibility: false
        });
        this.map.addLayer(this.vector);
    },

    /** private: method[findWMSLayerObject]
     *  Find the OpenLayers.Layer.WMS object using servicetype 'wms' for this
     *  resource.
     */
    findWMSLayerObject: function() {
        var layers = GeoPrisma.getLayers({
            resourceName: this.getName(),
            serviceType: "wms"
        });
        if (layers && layers.length == 1) {
            this.wmsLayerObject = layers[0];
        }
    },

    /** public: method[createStyleMap]
     *  :return: ``OpenLayers.StyleMap`` The default StyleMap object created
     *                                   for the vector layer.
     *
     *  Creates and return an OpenLayers.StyleMap object if none was provided
     *  for this resource.
     */
    createStyleMap: function() {
        var commonSymbolizers = {
            "fillOpacity": 0,
            "strokeWidth": 2
        };
        var defaultSymbolizers = Ext.applyIf(Ext.applyIf({
            // unique "default" symbolizers here...
        }, commonSymbolizers), OpenLayers.Feature.Vector.style['default']);
        var selectSymbolizers = Ext.applyIf(Ext.applyIf({
            // unique "select" symbolizers here...
        }, commonSymbolizers), OpenLayers.Feature.Vector.style['select']);

        return new OpenLayers.StyleMap({
            "default": defaultSymbolizers,
            "select": selectSymbolizers
        });
    },

    /** private: method[createWFSFeatureGrid]
     *  Creates a new org.GeoPrisma.ApplyFilter.WFSFeatureStore object for this
     *  resource and all its required elements :
     *  - a gxp.data.WFSFeatureStore
     *  - fields title and width detection
     *  - ignoredField(s)
     */
    createWFSFeatureGrid: function() {
        var store = new gxp.data.WFSFeatureStore({
            featureType: this.wfsLayerName,
            fields: this.getFieldsFromAttributes(),
            layer: this.vector,
            proxy: {
                protocol: {
                    startIndex: 1,
                    maxFeatures: this.maxFeatures,
                    srsName: this.map.getProjection()        
                }
            },
            url: Ext.urlAppend(this.proxyURL,
                OpenLayers.Util.getParameterString({
                    "osmresource": this.getName(),
                    "osmservice": this.getWFSServiceName()
                })
            )
        });

        // browse the store fields.  If the according resource field has a
        // "title" and/or "width" set, set it in the store field as well.
        // This is then used when creating the grid columns.
        var name, rField, field;
        store.fields.each(function(field) {
            name = field.name;
            rField = this.fields[name];
            if (rField) {
                if (rField.title) {
                    field.title = rField.title;
                }
                if (rField.options && Ext.isNumber(rField.options.width)) {
                    field.width = rField.options.width;
                }
            }
        }, this);

        // check for resource ignoredField or ignoredFields option.  Use it
        // else use default
        var ignoredFields;
        if (this.options.ignoredField) {
            this.options.ignoredFields = [this.options.ignoredField];
            delete this.options.ignoredField;
        }
        if (this.options.ignoredFields) {
            if (!Ext.isArray(this.options.ignoredFields)) {
                ignoredFields = [];
                for (var key in this.options.ignoredFields) {
                    ignoredFields.push(this.options.ignoredFields[key]);
                }
            } else {
                ignoredFields = this.options.ignoredFields;
            }
        } else {
            ignoredFields = this.defaultIgnoredFields;
        }

        this.grid = new org.GeoPrisma.ApplyFilter.WFSFeatureGrid({
            // property of gpx.grid.FeatureGrid is ignore, not ignored
            ignoreFields: ignoredFields,
            layer: this.vector,
            maxZoomScale: this.maxZoomScale,
            pageSize: this.maxFeatures,
            store: store,
            title: this.getTitle()
        });
    },

    /** private: method[getFieldsFromAttributes]
     *  :return: ``Array``
     *  Browse each records inside the GeoExt.data.AttributeStore object and
     *  push a new field hash object for each one.
     */
    getFieldsFromAttributes: function() {
        var fields = [];
        this.attributes.each(function(attribute) {
            fields.push({"name": attribute.get("name")});
        }, this);
        return fields;
    },

    /** public: method[reset]
     *  Reset all elements related to filtering for this resource.
     */
    reset: function() {
        this.vector.setVisibility(false);
        this.grid.resetFilter();
        this.grid.getStore().removeAll();
        this.sldSetter.resetSLD();
    },

    /** private: method[setFilter]
     *  :arg filter: ``OpenLayers.Filter`` Filter object to apply on both SLD
     *                                     and WFS.
     *
     *  This method apply the received filter to both WMS and WFS sides.  It
     *  also makes sure that the WMS Layer is visible.
     */
    setFilter: function(filter) {
        this.wmsLayerObject && this.wmsLayerObject.setVisibility(true);

        // apply WFS filter on both grid and sldSetter
        this.grid.triggerFilterRequest(filter);
        this.sldSetter.triggerFilterRequest(filter);
    },

    // Public Methods

    /** public: method[getName]
     *  :return: ``String`` The name of this resource.
     */
    getName: function() {
        return this.name;
    },

    /** public: method[getTitle]
     *  :return: ``String`` The title of this resource OR the name if it
     *                      doesn't have any
     */
    getTitle: function() {
        return this.title || this.name;
    },

    /** public: method[getWFSServiceName]
     *  :return: ``String`` The name of the WFS Service used by this resource.
     */
    getWFSServiceName: function() {
        return this.wfsServiceName;
    }
});
