/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma");

/*
 * @requires GeoExt.ux.ZoomTo.js
 * @requires org.GeoPrisma.API.js
 */

/** api: (define)
 *  module = org.GeoPrisma
 *  class = ZoomToPlugin
 */

/** api: constructor
 *  .. class:: ZoomToPlugin
 */
org.GeoPrisma.ZoomToPlugin = Ext.extend(Ext.util.Observable, {

    // Public Properties (Mandatory)

    /** private: property[zoomTo]
     *  ``GeoExt.ux.ZoomTo``
     *  The ZoomTo widget to link this plugin to.
     */
    zoomTo: null,

    // Private Properties

    /** private: property[api]
     *  ``org.GeoPrisma.API``
     *  A reference to the GeoPrisma object (instance of org.GeoPrisma.API)
     */
    api: null,

    /** private: property[map]
     *  ``OpenLayers.Map``
     *  A reference to the Map object
     */
    map: null,

    /** private: method[constructor]
     *  This class is a superconstructor only.
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);

        // references
        this.api = GeoPrisma;
        this.map = this.api.mapPanel.map;

        // events listeners
        this.api.on("setcenter", this.setCenter, this);
        this.zoomTo.manager.on("markerchanged", this.onMarkerChanged, this);
    },

    /** public: method[onMarkerChanged]
     *  :param feature: ``OpenLayers.Feature.Vector`` or ``false``
     *  
     *  Callback method of the ZoomToManager "markerchanged" event.  This
     *  fires the api "centermarkerchanged" event with a center coordinates
     *  informations as argument using receive feature.
     */
    onMarkerChanged: function(feature) {
        var fields = (feature === false) ? {} : {
            x: feature.geometry.x,
            y: feature.geometry.y,
            projection: this.map.getProjection(),
            zoom: this.map.getZoom()
        };
        this.api.fireEvent("centermarkerchanged", fields);
    },

    /** public: method[setCenter]
     *  :param object: ``Object``
     *    Hash objects that can contains the following keys :
     *    - 'x'    : (Float) Mandatory. The x coordinate of the center to set
     *    - 'y'    : (Float) Mandatory. The y coordinate of the center to set
     *    - 'zoom' : (Integer) Optional. The zoom level to used when recentering
     *    - 'projection' : (String) Optional. The projection of the coordinates
     *  :return: ``Boolean``
     *
     *  Callback method of the API "setcenter" event.  This method calls the
     *  ZoomTo widget recenter method using parameters received in the object.
     *  Returns false on success to stop the event.
     */
    setCenter: function(object) {
        if (Ext.isNumber(object.x) && Ext.isNumber(object.y)) {
            var values = {
                coordx: object.x,
                coordy: object.y,
                projection: object.projection || this.map.getProjection(),
                zoom: (Ext.isNumber(object.zoom)) ? object.zoom : null
            };
            this.zoomTo.recenter(values);
            this.zoomTo.setValues(values);

            return false;
        }
    }
});
