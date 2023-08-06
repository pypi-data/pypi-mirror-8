/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.InitialView");

/*
 * @requires org.GeoPrisma.InitialView.LocalFormat.js
 */

/** api: (define)
 *  module = org.GeoPrisma.InitialView
 *  class = View
 */

/** api: constructor
 *  .. class:: View
 */
org.GeoPrisma.InitialView.View = Ext.extend(Ext.util.Observable, {

    // Public Properties (Mandatory)

    /** api: property[featuresString]
     *  ``String``
     *  A string document containing the features for this view
     */
    featuresString: null,

    /** api: property[mapPanel]
     *  :class:``GeoExt.MapPanel``
     *  A reference to the MapPanel object.
     */
    mapPanel: null,

    // Public Properties (Optional)

    /** api: property[allowLayerToggling]
     *  ``Boolean``
     *  If set, if view is linked to a resource, its layers will have their
     *  visibility set to true.
     */
    allowLayerToggling: true,

    /** api: property[reader]
     *  ``OpenLayers.Format`` or ``org.GeoPrisma.InitialView.LocalFormat`` or
     *  ``OpenLayers.Protocol``
     *  The object used to read the featuresString property (sync) or trigger
     *  read requests when using async.
     */
    reader: null,

    /** api: property[highlight]
     *  ``Boolean``
     *  If set, vector features are added to the map at the features locations
     */
    highlight: false,

    /** api: property[features]
     *  :class:``OpenLayers.Layer.Vector``
     *  The vector layer object used for highlight purpose. Automatically
     *  created if not set.
     */
    highlightLayer: null,

    /** api: property[maxZoom]
     *  ``Integer``
     *  The maximum level that can be zoomed to.
     */
    maxZoom: null,

    /** api: property[highlight]
     *  ``Boolean``
     *  Defaults to false. If set, replaces the map zoomToMaxExtent method for
     *  one recentering on this view instead.
     */
    replaceZoomToMaxExtent: false,

    /** api: property[resourceName]
     *  ``String``
     *  The name of the resource. Only used when using resource views.
     */
    resourceName: null,

    /** api: property[serviceType]
     *  ``String``
     *  The service type used for getting the features. Only used when using
     *  resource views. Also used to set the reader property.
     */
    serviceType: null,

    // Private Properties

    /** private: property[features]
     *  ``Array``
     *  Array of features read from the featuresString property using the reader
     */
    features: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
        this.features = [];
        !this.reader && this.createReader();
    },

    /** private: method[createReader]
     *  Sets the reader property using serviceType.
     */
    createReader: function() {
        switch (this.serviceType)
        {
            case "featureserver":
                this.reader = new OpenLayers.Format.GeoJSON()
                break;
            default:
                this.reader = new org.GeoPrisma.InitialView.LocalFormat();
        }
    },

    /** private: method[read]
     *  Sets the features property by reading the featuresString using the
     *  reader.
     */
    read: function() {
        var featureString = this.featuresString;
        var features = this.reader.read(featureString);
        
        var projCodeSource = this.defaultSRID;
        var projCodeMapDest = this.mapPanel.map.projection.projCode;

        //Si les projections de l'initial view et de la carte sont differentes
        if (projCodeSource && projCodeSource != projCodeMapDest) {
            var projSource = new OpenLayers.Projection(projCodeSource);
            var projMapDest = new OpenLayers.Projection(projCodeMapDest);
            
            //On transforme la projection
            features[0].geometry.transform(projSource,projMapDest);
        }
        this.features = features;
    },

    /** private: method[isValid]
     *  :return: ``Boolean`` Whether this view is valid or not.
     *
     *  A view is valid if it contains at least one feature.
     */
    isValid: function() {
        return this.features.length > 0;
    },

    /** private: method[createHighlightLayer]
     *  Creates a new ``OpenLayers.Layer.Vector`` object for highlight purpose.
     */
    createHighlightLayer: function() {
        this.highlightLayer = new OpenLayers.Layer.Vector("Highlight", {
            styleMap: new OpenLayers.StyleMap({
                graphicName: "cross",
                pointRadius: 10,
                fillColor: "red",
                fillOpacity: 0.5
            }),
            alwaysInRange: true,
            displayInLayerSwitcher: false
        });
        this.mapPanel.map.addLayer(this.highlightLayer);
        this.mapPanel.map.events.on({"unselectallfeatures": function(e) {
            this.highlightLayer.destroyFeatures();
            OpenLayers.Event.stop(e);
        }, scope: this});
    },

    /** private: method[highlightFeatures]
     *  Add view features to the highlightLayer
     */
    highlightFeatures: function() {
        var canAdd = true;
        Ext.each(this.features, function(feature) {
            if (!(feature instanceof OpenLayers.Feature.Vector)) {
                canAdd = false;
                return false;
            }
        }, this);
        canAdd && this.highlightLayer.addFeatures(this.features);
    },

    /** private: method[moveHighlightLayerOnTop]
     *  Move the highlightLayer on top of all others.
     */
    moveHighlightLayerOnTop: function() {
        this.highlightLayer && this.mapPanel.map.setLayerIndex(
            this.highlightLayer,
            this.mapPanel.map.layers.length
        );
    },

    // Public methods

    /** public: method[zoomToFeaturesExtent]
     *  Browse each features of this view and create a bounds containing all
     *  of them. Set the map extent to it.  Make sure it wouldn't exceed the
     *  maxZoom (if set).
     *
     *  Also, if the view is bound to a resource, set the visibility of all its
     *  layers to true, make sure the highlightLayer is on top, manage the
     *  replaceZoomToMaxExtent property and trigger the highlight (if set).
     */
    zoomToFeaturesExtent: function() {
        var bounds, center, map, bounds, zoom;
        map = this.mapPanel.map;
        Ext.each(this.features, function(feature, index, features) {
            if (bounds) {
                bounds.extend((feature instanceof OpenLayers.Bounds)
                    ? feature : feature.geometry.getBounds());
            } else {
                bounds = (feature instanceof OpenLayers.Bounds)
                    ? feature : feature.geometry.getBounds();
            }
        }, this);

        // use center instead of extent maxZoom is set
        if (Ext.isNumber(this.maxZoom)) {
            center = bounds.getCenterLonLat();
            zoom = map.getZoomForExtent(bounds);
            zoom = (zoom == null || zoom > this.maxZoom) ? this.maxZoom : zoom;
        }

        if (map.center) {
            center ? map.setCenter(center, zoom) : map.zoomToExtent(bounds);
            // if map already centered, recenter
        } else {
            // map not centered yet, change map panel center+zoom or extent
            delete this.mapPanel.center;
            delete this.mapPanel.extent;
            delete this.mapPanel.zoom;
            if (center) {
                this.mapPanel.center = center;
                this.mapPanel.zoom = zoom;
            } else {
                this.mapPanel.extent = bounds;
            }
        }

        // if view has resourceName, set all its layer visibility if allowed
        this.allowLayerToggling && this.resourceName && Ext.each(
            GeoPrisma.getLayers({resourceName: this.resourceName}),
            function(layer, index, layers) {
                layer.setVisibility(true);
            },
            this
        );
        // make sure highlightLayer is on top
        this.moveHighlightLayerOnTop();

        // replaceZoomToMaxExtent
        if (this.replaceZoomToMaxExtent) {
            map.zoomToMaxExtent = function() {
                center ? map.setCenter(center, zoom) : map.zoomToExtent(bounds);
            }
        };

        // highlight - if no existing highlightLayer already created
        if (this.highlight) {
            !this.highlightLayer && this.createHighlightLayer();
            this.highlightFeatures();
        }
    }
});
