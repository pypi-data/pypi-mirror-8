/**
 * Copyright (c) 2008-2011 The Open Source Geospatial Foundation
 *
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

/**
 * @include GeoExt/widgets/MapPanel.js
 * @include GeoExt/widgets/Popup.js
 */

/** api: (define)
 *  module = GeoExt
 *  class = TemplatePopup
 *  base_link = `Ext.Window <http://dev.sencha.com/deploy/dev/docs/?class=Ext.Window>`_
 */
Ext.namespace("GeoExt");

/** api: example
 *  Sample code to create a templated popup from data associated with a feature:
 *
 *  .. code-block:: javascript
 *
 *      var popup = new GeoExt.TemplatePopup({
 *          map: map,
 *          width: 200,
 *          tpl: "<div>Popup content</div>",
 *      });
 */

/** api: constructor
 *  .. class:: TemplatePopup(config)
 *
 *      TemplatePopups are a specialized widget that uses
 *      a template to format attributes from an OGC OWS layer in
 *      a popup. Upon initialization, it detects any wfs layers
 *      and attaches a select control to trigger a popup.
 */
GeoExt.TemplatePopup = Ext.extend(GeoExt.Action, {

    /** api: config[map]
     *  ``OpenLayers.Map`` or :class:`GeoExt.MapPanel`
     *  The map that popups will be anchored to.
     */
    map: null,

    /** api: config[autoDetectLayer]
     * ``Boolean``
     * define if the script receive or not layers to use
     */
    autoDetectLayer: true,

    /** api: config[queryVisible]
     * ``Boolean``
     * define if queries exclude hidden layers
     */
    queryVisible: true,

    /** api: config[url]
     * ``String``
     * define if the script receive or not layers to use
     */
    url: null,

    /** api: config[layers]
     * ``Array``
     * An array of layers to use
     */
    layers: null,
    
    /** api: config[tpl]
     *  ``Object``  a hash of  html templates for the feature attributes,
     *  each formatted according to the Ext.XTemplate rules.
     *  The keys should match specific wfs layer names. The 'default'
     *  template is used for any non-matched layers.
     */
    tpl: {
        'default':'TemplatePopup: Please define a default template'
    },

    defaultOptions: {
        autoDetectLayer: true,
        layers: [],
        hover: false,
        autoEnable: false,
        mode: 'wfs'
    },

    /** private: method[constructor]
     *  Initializes the widget.
     */
    constructor: function(config) {
        config = Ext.apply(this.defaultOptions, config);
        if(config.map instanceof GeoExt.MapPanel) {
            config.map = config.map.map;
        }
        this.map = config.map;
        this.control = config.control;
        this.tpl = config.tpl;
        this.mode = config.mode;
        this.url = config.url;
        this.autoDetectLayer = config.autoDetectLayer;
        this.queryVisible = config.queryVisible;
        this.tplCompiled = new Ext.XTemplate(this.tpl['default']).compile();
        this.layers = config.layers;
        
        //collect wfs layers and attach event
        var resources = [];
        
        if (this.autoDetectLayer) {
            for (var i=0, len = this.map.layers.length; i < len; i++) {
                var layer = this.map.layers[i];
                if (this.mode == 'wfs') {
                    if (layer.CLASS_NAME == 'OpenLayers.Layer.WFS' ||
                    (layer.protocol &&
                        layer.protocol.CLASS_NAME.substr(0,23) == 'OpenLayers.Protocol.WFS')) {
                        this.layers.push(layer);
                        resources.concat(layer.resource);
                        layer.events.on({
                            scope: this,
                            featureselected: function(e) {
                                this.formatFeature(e.feature);
                            }
                        });
                    }
                } else {
                    if (layer.CLASS_NAME == 'OpenLayers.Layer.WMS') {
                        this.layers.push(layer);
                        resources.concat(layer.resource);
                    }
                }
            };
        }
        if (!config.control) {
            if (this.mode == 'wfs') {
                config.control = new OpenLayers.Control.SelectFeature(
                    this.layers,
                    {hover: config.hover}
                );
            } else {
                config.control = new OpenLayers.Control.TemplatePopupWMSGetFeatureInfo({
                    url: this.url || (OpenLayers.Util.isArray(this.layers[0].url) ? this.layers[0].url[0] : this.layers[0].url),
                    layers: this.layers,
                    infoFormat: "application/vnd.ogc.gml",
                    hover: config.hover,
                    queryVisible: this.queryVisible,
                    eventListeners: {
                        scope: this,
                        getfeatureinfo: function(e) {
                            if (e.features && e.features.length) {
                                this.formatFeature(e.features[0]);
                            }
                        }
                    }
                });
            }
        }

        arguments.callee.superclass.constructor.call(this, config);

        //start listening
        if (config.autoEnable) {
            this.control.activate();
        }
    },

    /** private: method[getFeature]
     *  Executes when a feature is selected.
     */
    formatFeature: function(feature) {
        //1. get feature attributes
        var content, properties = feature.attributes;

        //Fix pour les url django
        String.prototype.insertAt=function(index, string) { 
            return this.substr(0, index) + string + this.substr(index);
        }
        var ind1 = feature.attributes['htmlImages'].indexOf("proxy.php");
        properties['htmlImages'] = properties['htmlImages'].insertAt(ind1,baseUrl);
        var ind2 = feature.attributes['htmlImages'].lastIndexOf("proxy.php");
        properties['htmlImages'] = properties['htmlImages'].insertAt(ind2,baseUrl);

        //2. apply returned values to template
        var templateName = feature.layer?feature.layer.name:feature.type;
        
        if (this.tpl[templateName]) {
            content = new Ext.XTemplate(this.tpl[templateName]).apply(properties);
        } else {
            content = this.tplCompiled.apply(properties);
        }
        var that = this;
        //3. fill popup with result
        //anchor to feature lonlatgml_geometriesâ—Š for wfs, bbox center for wms
        var position = feature.lonlat?feature:feature.bounds.getCenterLonLat();
        new GeoExt.Popup({
            location: position,
            map: this.map,
            width:this.width,
            html: content,
            maximizable: true,
            collapsible: true,
            listeners: {
                close: function() {
                  if (feature.layer) {
                    if(OpenLayers.Util.indexOf(feature.layer.selectedFeatures,
                                               feature) > -1) {
                        that.control.unselect(feature);
                    }
                  }
                }
            }
        }).show();
    },

    /** api: method[addTemplate]
     *  add an additional key to the template hash.
     */
    addTemplate: function(layerName, template) {
        this.tpl[layerName] = template;
    }

});

/** api: xtype = gx_template_popup */
Ext.reg('gx_template_popup', GeoExt.TemplatePopup);
