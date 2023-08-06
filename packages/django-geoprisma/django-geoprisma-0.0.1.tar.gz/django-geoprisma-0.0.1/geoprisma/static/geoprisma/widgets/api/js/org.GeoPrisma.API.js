/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma");

/** api: (define)
 *  module = org.GeoPrisma
 *  class = API
 */

/** api: constructor
 *  .. class:: API
 */
org.GeoPrisma.API = Ext.extend(Ext.util.Observable, {

    // API Properties

    /** api: property[mapPanel]
     * :class:``GeoExt.MapPanel``
     * A reference to the MapPanel widget.  If none is providen, then it's
     * guessed.
     */
    mapPanel: null,

    /** api: property[version]
     * ``String``
     * The version number of GeoPrisma.
     */
    version: null,

    // Private

    /** api: property[map]
     * :class:``OpenLayers.Map``
     * A reference to the Map object.
     */
    map: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);

        this.addEvents(
            /** private: event[applyfilters]
             *  Fires when applying one or more filters to one or more
             *  resources.
             */
            "applyfilters",

            /** private: event[setcenter]
             *  Fires when setting a new center location to the map
             */
            "setcenter",

            /** public: event[centerchanged]
             *  Fires when the mapPanel fires the "moveend" event.
             */
            "centerchanged",

            /** public: event[centermarkerchanged]
             *  Fires when the center marker of a ZoomTo widget was added,
             *  modified or removed.
             */
            "centermarkerchanged"
        );
    },

    // Public Methods (API)

    /** public: method[applyFilters]
     *  :param resourceFilters: ``Array``
     *    An array of hash objects that containing the following keys :
     *    - 'resource' : the name of the resource to apply the filter
     *    - 'filter'   : the filter to apply to the resource
     *
     *  This method fires the 'applyfilters' event with the array as 
     *  argument.
     */
    applyFilters: function(resourceFilters) {
        this.fireEvent("applyfilters", resourceFilters);
    },

    /** public: method[applyFilter]
     *  :param resourceFilter: ``Object``
     *    Hash object that contains the following keys :
     *    - 'resource' : the name of the resource to apply the filter
     *    - 'filter'   : the filter to apply to the resource
     *
     *  This method fires the 'applyfilters' event with the resourceFilter added
     *  to an array as the argument.
     */
    applyFilter: function(resourceFilter) {
        this.fireEvent("applyfilters", [resourceFilter]);
    },

    /** public: method[getCenter]
     *  :param displayProj: ``String`` The projection code we want to have the
     *                                 coordinates displayed in.  Defaults to
     *                                 map displayProjection code if set, else
     *                                 map projection.
     *
     *  :return: ``Object`` An object containg the informations about the center
     *                      of the map.
     */
    getCenter: function(displayProj) {
        displayProj = displayProj || this.getDisplayProjection();
        var center = this.map.getCenter();
        return this.getCoordinateInfo(
            center.lon, center.lat, this.map.getProjection(), displayProj);
    },

    /** public: method[setCenter]
     *  :param obj: ``Object``
     *    Hash objects that can contains the following keys :
     *    - 'x'    : (Float) Mandatory. The x coordinate of the center to set
     *    - 'y'    : (Float) Mandatory. The y coordinate of the center to set
     *    - 'zoom' : (Integer) Optional. The zoom level to use
     *    - 'projection' : (String) Optional. The projection of the coordinates
     *
     *  This method fires the 'setcenter' event with the received object as
     *  argument.  If no listener returns false (if no widget actually set the
     *  map center), let the API do it.
     */
    setCenter: function(obj) {
        if (!Ext.isNumber(obj.x) || !Ext.isNumber(obj.y)) {
            return;
        }

        obj.projection = obj.projection || this.map.getProjection();
        obj.zoom = (Ext.isNumber(obj.zoom)) ? obj.zoom : null;

        if (this.fireEvent("setcenter", obj) !== false) {
            // get coordinates in map projection, then set map center
            var pt = this.getTransformedCoords(obj.x, obj.y, obj.projection);
            this.map.setCenter(new OpenLayers.LonLat(pt.x, pt.y), obj.zoom);
        }
    },

    // Public Methods (Util)

    /** public: method[setCenter]
     *  :param x: ``Float`` X coordinate 
     *  :param y: ``Float`` Y coordinate
     *  :param y: ``String`` Projection code of X and Y coordinates
     *  :param y: ``String`` Projection code for display purpose.
     *
     *  This method fires the 'setcenter' event with the receirved object as
     *  argument.
     */
    getCoordinateInfo: function(x, y, source, dest) {
        dest = dest || this.getDisplayProjection();
        return Ext.apply({
            projection: dest,
            zoom: this.map.getZoom()
        }, this.getTransformedCoords(x, y, source, dest));
    },

    /** public: method[getDisplayProjection]
     *  :return: ``String`` The projection code to use by default when
     *                      displaying coordinates
     */
    getDisplayProjection: function() {
        if (this.map.displayProjection) {
            return this.map.displayProjection.getCode();
        } else {
            this.map.getProjection();
        }
    },

    /** public: method[getLayers]
     *  :param option: ``Object``
     *    Hash object containing search options.  Possible keys (all optional)
     *    are :
     *    - resourceName (String) : get layers having the specific resource name
     *    - serviceType (String): get layers only of specific service type
     *  :return:  ``Array`` of :class:``OpenLayers.Layer`` objects.
     *
     *  Returns layers that match the search options defined.
     */
    getLayers: function(options) {
        options = options || {};

        // make sure the mapPanel property is set
        if (!this.mapPanel) {
            this.setMapPanel();
        }

        var layers = this.mapPanel.map.layers;

        // search each criteria defined
        if (options.resourceName) {
            layers = this.getLayersByResourceName(options.resourceName, layers);
        }
        if (options.serviceType) {
            layers = this.getLayersByServiceType(options.serviceType, layers);
        }

        return layers;
    },

    /** public: method[getLayersByResourceName]
     *  :param match: ``String`` resource name the layer must match
     *  :param layers: ``Array`` of :class:``OpenLayers.Layer`` objects.  If not
     *                           defined, then use all map layers.
     *  :return:  ``Array`` of :class:``OpenLayers.Layer`` objects.
     *
     *  Returns layers that matching the specified resource name.
     */
    getLayersByResourceName: function(match, layers) {
        layers = layers || this.mapPanel.map.layers;
        var found = [];
        Ext.each(layers, function(l) {
            l.resources && l.resources.indexOf(match) != -1 && found.push(l);
        }, this);
        return found;
    },

    /** public: method[getLayersByServiceType]
     *  :param match: ``String`` service type the layer must match
     *  :param layers: ``Array`` of :class:``OpenLayers.Layer`` objects.  If not
     *                           defined, then use all map layers.
     *  :return:  ``Array`` of :class:``OpenLayers.Layer`` objects.
     *
     *  Returns layers that matching the specified service type.
     */
    getLayersByServiceType: function(match, layers) {
        layers = layers || this.mapPanel.map.layers;
        var found = [], type;
        Ext.each(layers, function(l) {
            type = (l.servicetype) ? l.servicetype : l.serviceType;
            type && type == match && found.push(l);
        }, this);
        return found;
    },

    /** private: method[getTransformedCoords]
     *  :param x: ``Float`` easting coordinate
     *  :param y: ``Float`` northing coordinate
     *  :param source: ``String`` projection code to use as source
     *  :param dest: ``String`` projection code to use as destination.
     *                          Defaults to map projection.
     *  :return: ``Object`` containing x and y properties
     *
     *  Returns an object containing x and y properties. Transform using
     *  given projections if needed.
     */
    getTransformedCoords: function(x, y, source, dest) {
        dest = dest || this.map.getProjection();
        if (dest === source) {
            return {x: x, y: y};
        } else {
            var transformed = new OpenLayers.LonLat(x, y).transform(
                new OpenLayers.Projection(source),
                new OpenLayers.Projection(dest)
            );
            return {x: transformed.lon, y: transformed.lat};
        }
    },

    /** public: method[setMapPanel]
     *  :param mapPanel: :class:``GeoExt.MapPanel``
     *  
     *  Sets the mapPanel property with providen MapPanel object OR guess one.
     *  Also sets other private properties and listeners related to the
     *  mapPanel.
     */
    setMapPanel: function(mapPanel) {
        this.mapPanel = (mapPanel instanceof GeoExt.MapPanel)
            ? mapPanel : GeoExt.MapPanel.guess();
        this.map = this.mapPanel.map;
        this.map.events.on({
            "moveend": function(a, b, c) {
                this.fireEvent("centerchanged", this.getCenter());
            },
            scope: this
        });
    },

    /** public: method[zoomToFeatureExtent]
     *  :param feature: :class:``OpenLayers.Feature.Vector``
     *  :param maxScale: ``Float`` Max scale allowed to zoom to.
     *  
     *  Zoom to the feature extent OR feature center with limited zoom scale.
     */
    zoomToFeatureExtent: function(feature, maxScale) {
        if (!this.mapPanel) {
            this.setMapPanel();
        }
        var map, bounds, zoom, maxZoom, u;
        if (!feature || !feature.geometry) {
            return;
        }
        map = this.mapPanel.map;
        if (maxScale) {
            bounds = feature.geometry.getBounds();
            zoom = map.getZoomForExtent(bounds);
            maxZoom = map.getZoomForResolution(
                OpenLayers.Util.getResolutionFromScale(maxScale, map.units));
            map.setCenter(
                bounds.getCenterLonLat(),
                (zoom > maxZoom) ? maxZoom : zoom
            );
        } else {
            map.zoomToExtent(feature.geometry.getBounds());
        }
    }
});
