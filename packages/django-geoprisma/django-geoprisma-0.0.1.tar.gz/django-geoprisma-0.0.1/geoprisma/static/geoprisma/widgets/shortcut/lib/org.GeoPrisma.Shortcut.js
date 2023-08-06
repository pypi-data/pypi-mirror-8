/* 
   Copyright (c) 2009-2012 Boreal - Information Strategies
   Published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/

Ext.namespace("org.GeoPrisma");

/** api: (define)
 *  module = org.GeoPrisma
 *  class = Shortcut
 */

/** api: constructor
 *  .. class:: Shortcut
 *  Display a list of elements based on a AJAX request and recenters on the
 *  selected element.
 */
org.GeoPrisma.Shortcut = Ext.extend(Ext.form.ComboBox, {
    
    /*
        const: i18n_please_wait
        {String} Wait message, for initial dataStore row        
    */
    i18n_please_wait : 'Please wait...',
    
    /**
     * Property: triggerAction
     * {String} - Default triggerAction value.
     */
    triggerAction: 'all',

    /**
     * Property: displayField
     * {String} - Default displayField value.
     */
    displayField: 'text',

    /**
     * Property: valueField
     * {String} - Default valueField value.
     */
    valueField: 'value',

    /**
     * Property: mode
     * {String} - Default mode value.
     */
    mode: 'local',

    /**
     * APIProperty: defaultZoom
     * {Integer} - Zoom level used if no zoom level is provided by the user
     */
    defaultZoom: null,

    /**
     * APIProperty: emptyText
     * {String} - Default emptyText value while loading the data.
     */
    emptyText: "Loading...",

    /**
     * APIProperty: emptyTextAfterLoading
     * {String} - Empty text to display in the ComboBox after the data has
     *            finished loading.
     */
    emptyTextAfterLoading: null,

    /**
     * Property: listeners
     * {Object} - Contains functions called on specific combobox events.
     */
    listeners: {
        select: function(combo, record) {
            this.recenterOnGeometry(record.get('geometry'));
//  Checks if the highlight node exists in the configuration and is set to true
        if (this.highlight)
        {
            this.highlightOnGeometry(record.get('feature'));
        }

        }
    },

    /**
     * Property: APIProperty: map
     * {<OpenLayers.Map>}
     */
    map: null,

    /**
     * Property: APIProperty: layers
     * {Array(<OpenLayers.Layer>)} - Get automatically filled with layers that
     *                               has this.resourceName
     */
    layers: null,

    /**
     * Property: APIProperty: maxFeatures
     * {integer} - The maximum number of features returned by the AJAX request.
     */
    maxFeatures: null,

    /**
     * Property: APIProperty: resourceName
     * {string} - The name of the Resource from the config file.
     */
    resourceName: null,
    
    /**
     * Property: APIProperty: serviceName
     * {string} - The name of the Service from the config file.
     */
    serviceName: null,

    /**
     * Property: APIProperty: layerName
     * {string} - The name of the layer from the DataStore in the config file.
     *            Comes from the servicetype.
     */
    layerName: null,

    /**
     * Property: format
     * {string} - The default format value.  Only used when using
     *            'featureserver' servicetype.
     */
    format: "GeoJSON",

    /**
     * APIProperty: url
     * {string} - The url of the Proxy.
     */
    url: null,

    /**
     * APIProperty: field
     * {string} - The field to display in the combobox.
     */
    field: null,

    /**
     * APIProperty: serviceType
     * {string} - The type of service to use.  Can be : 'featureserver' or 'wfs'
     */
    serviceType: null,

    /** private: method[constructor]
     *  Private constructor override.
     */
    constructor: function(config) {
        config = config || {};
        var store = new Ext.data.SimpleStore({
            fields: ['geometry', 'value', 'text'],
            data : [['foo', this.i18n_please_wait, this.i18n_please_wait]]
        });
        config['store'] = store;

        // if an emptyText is defined, it was also defined as a 
        // emptyTextAfterLoading, so remove it.
        if(config['emptyText']){
            delete config['emptyText'];
        }

        arguments.callee.superclass.constructor.call(this, config);

        this.on("afterrender", this.loadData, this);
    },

    /**
     * Method: loadData
     * Called after the ComboBox has been rendered.
     *
     * Send the request that will load the data to populate the ComboBox.
     */
    loadData : function() {
        switch (this.serviceType) {
            case "featureserver":
                var url = this.url;

                url += "/"+this.layerName+"/";
                url += "all."+this.format+"?";

                if(this.maxFeatures != null && this.maxFeatures != ""){
                    url += "maxfeatures="+this.maxFeatures;            
                }

                var objParams = {
                    'osmresource': this.resourceName,
                    'osmservice': this.serviceName,
                    'osmtoken': this.token
                };

                var strParams = OpenLayers.Util.getParameterString(objParams);
                if(strParams.length > 0) {
                    var strSeparator = (url.indexOf('?') > -1) ? '&' : '?';
                    url += strSeparator + strParams;
                }

                OpenLayers.Request.GET({
		    url:url,
		    params:'',
		    scope:this,
		    callback:function(response) {
			this.populateComboBox(new OpenLayers.Format.GeoJSON().read(response.responseText));
		    }
                });
                break;
            case "wfs":
                var protocol = new OpenLayers.Protocol.WFS({
                    url: OpenLayers.Util.urlAppend(this.url,
                        OpenLayers.Util.getParameterString({
                            'osmresource': this.resourceName,
                            'osmservice': this.serviceName
                    })),
                    featureType: this.layerName
                });

                protocol.read({
                    'filter': new OpenLayers.Filter.Spatial({
                        type: OpenLayers.Filter.Spatial.BBOX,
                        value: this.map.getMaxExtent(),
                        projection: this.map.getProjection()
                    }),
                    callback: function(response) {
                        this.populateComboBox(response.features);
                    },
                    scope: this
                });
                break;
        }
    },

    /**
     * Method: sortByFieldValue
     *
     * Parameters :
     * a {string}
     * b {string}
     *
     * Returns :
     * {Array} - Sorted array
     */
    sortByFieldValue: function(a, b) {
        if (a.fieldvalue == null){a.fieldvalue = "N/A"; return 1;}
        if (b.fieldvalue == null){b.fieldvalue = "N/A"; return -1;}
        var x = a.fieldvalue;
        var y = b.fieldvalue;
		if (x.toLowerCase)
		{
			x = x.toLowerCase();
		}
		if (y.toLowerCase)
		{
			y = y.toLowerCase();
		}
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    },

    /**
     * Method: populateComboBox
     * Populate the combobox droplist with features
     *
     * Parameters:
     * features - {Array} of OpenLayers.Feature.Vector objects
     */
    populateComboBox: function(features) {
        var data = [];

        if (!features || features.length == 0){
            return;
        }

        // data array building...
        for (var i=0, nLen = features.length; i<nLen; i++){
            var geometry = features[i].geometry;

            if (geometry.CLASS_NAME != "OpenLayers.Geometry.Point") {
                geometry = geometry.getBounds();
            }

            data.push({
              'geometry': geometry,
              'fieldvalue': features[i].attributes[this.field],
              'feature': features[i]
            });
        }

        // sort the data
        data.sort(this.sortByFieldValue);

        // remove current store data and populate
        this.store.removeAll();
        for (var i=0, nLen = data.length; i<nLen; i++){
            this.store.add([
                new Ext.data.Record({
                    'geometry': data[i]['geometry'],
                    'text'    : data[i]['fieldvalue'],
                    'value'   : data[i]['fieldvalue'],
                    'feature'   : data[i]['feature']
                })
            ]);
        }

        // Loading is finished.  Set a new empty text.
        this.setRawValue(this.emptyTextAfterLoading);
        this.emptyText = this.emptyTextAfterLoading; // For when user clear raw value
    },

    /**
     * Method: recenterOnCoords
     * Recenters on given coordinates and zoom level
     *
     * Parameters:
     * x - {Float} easting coordinate
     * y - {Float} northing coordinate
     * zoom - {Integer} zoom level (optional)
     */
    recenterOnCoords: function(x, y, zoom) {
        
        // use default zoom level if provided in widget config, 
        // else keep current zoom level
        if (typeof(zoom) == 'undefined') {
            zoom = (typeof(this.defaultZoom) != 'undefined') 
                   ? this.defaultZoom : this.map.getZoom()
        }

        this.map.setCenter(new OpenLayers.LonLat(x, y), zoom);
    },

    /** 
     * Method: recenterOnBbox 
     * Recenters on given bounds 
     * 
     * Parameters: 
     * bbox - {<OpenLayers.Bounds>} 
     */ 
    recenterOnBbox: function(bbox) { 
        if (this.showCenter) { 
            // display a symbol on the center point of the bbox 
            var lonlat = bbox.getCenterLonLat(); 
            this.showCenterMark(lonlat.lon, lonlat.lat); 
        }   
  
        this.map.zoomToExtent(bbox); 
    },

    /**
     * Method: recenterOnGeometry
     * Recenters on given geometry
     *
     * Parameters:
     * geometry - {<OpenLayers.Geometry>}
     */
    recenterOnGeometry: function(geometry) {
        if (geometry.CLASS_NAME == "OpenLayers.Geometry.Point") {
            this.recenterOnCoords(geometry.x, geometry.y);
        } else {
            // means it's an OpenLayers.Bounds object
            this.recenterOnBbox(geometry);
        }

        this.activateResources();
    },

     /**
     * Method: highlightOnGeometry
     * Highlights the given geometry
     *
     * Parameters:
     * geometry - {<OpenLayers.Geometry>}
     */
    highlightOnGeometry: function(feature) {

     var layers = this.map.getLayersByResource(this.resourceName,this.serviceType);
     
     this.highlightFeature = function (layer, fid) { 
                            for(var i = 0; i<layer.features.length;++i) {         
                                        if (layer.features[i].fid == fid) {         
                                            FeatureSelectControl.highlight(layer.features[i]);
                                            break;             
                                        }
                             }
      };

      this.unhighlightFeature = function (layer, fid) { 
                            for(var i = 0; i<layer.features.length;++i) {         
                                        if (layer.features[i].fid == fid) {         
                                            FeatureSelectControl.unhighlight(layer.features[i]);
                                            break;             
                                        }
                             }
        };

     if (layers[0] != null) {

        // alert("Case existing FS layer");
        var FeatureSelectControl = new OpenLayers.Control.SelectFeature(layers[0], {});
       

        this.map.addControl(FeatureSelectControl);
        FeatureSelectControl.unselectAll();
        FeatureSelectControl.activate();
        
       
         var callback = function() { 
            this.highlightFeature(layers[0],feature.fid);
         };

        var callback2 = function() { 
            this.unhighlightFeature(layers[0],feature.fid);
        };
        
        layers[0].events.register("loadend", this, callback);
        layers[0].events.register("click", this, callback2); 

      }
      else 
      {
        // alert("Case no existing FS layer");

        var s = new OpenLayers.Util.applyDefaults({
            fillColor: "#0000FF",
            strokeColor: "#0000FF",
            strokeWidth: 2
        }, OpenLayers.Feature.Vector.style["default"]);

      
        var myStyles = new OpenLayers.StyleMap(s);

        if (this.hilites == null)
        {
            this.hilites = new OpenLayers.Layer.Vector(
                "TempHighlight", 
                {styleMap: myStyles, displayInLayerSwitcher: false}
            );
            this.map.addLayer(this.hilites);
        }
        else 
        {
            this.hilites.removeFeatures(this.hilites.features);   
        }
        this.hilites.addFeatures([feature]);

        var FeatureSelectControl = new OpenLayers.Control.SelectFeature(this.hilites, {});
       

        this.map.addControl(FeatureSelectControl);
        FeatureSelectControl.unselectAll();
        FeatureSelectControl.activate();

        this.highlightFeature(this.hilites,feature.fid);
        
        var callback3 = function() { 
            var layer = this.hilites;
                            if (layer) {
                                layer.destroy();
                                this.hilites = null;
                            }
        };

        this.hilites.events.register("click", this, callback3);


      }
    },


    /**
     * Method: activateResources
     * Called when this widget is used.  "Activate" specific resources or
     * the same resources it uses when defined.  The real action made is to 
     * show the revelent OpenLayers.Layer objects.
     */
    activateResources: function() {
        var layers;

        // if selfActivate is set, search 
        if (this.selfActivate){
            layers = this.map.getLayersByResource(this.resourceName);

            for(var i=0, len=layers.length; i<len; i++){
                layers[i].show(this.resourceName);
            }
        }

        if (this.activeResources){
            for(var resourceKey in this.activeResources){
                layers = [];

                var resource = this.activeResources[resourceKey];
                var resourceName = resource['name'];

                if(resource['servicetypes']) {
                    var serviceTypes = resource['servicetypes'];
                    for(var serviceTypeKey in serviceTypes){
                        serviceType = serviceTypes[serviceTypeKey];
                        foundLayers = this.map.getLayersByResource(
                            resourceName, serviceType);
                        layers = layers.concat(foundLayers);
                            
                    }
                } else {
                    layers = this.map.getLayersByResource(resourceName);
                }

                for(var i=0, len=layers.length; i<len; i++){
                    layers[i].show(resourceName);
                }
            }
        }
    }
});
