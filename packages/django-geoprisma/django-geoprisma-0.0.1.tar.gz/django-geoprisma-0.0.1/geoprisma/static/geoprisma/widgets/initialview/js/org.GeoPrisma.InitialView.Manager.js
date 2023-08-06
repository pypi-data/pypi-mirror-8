/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.InitialView");

/*
 * @requires org.GeoPrisma.InitialView.LocalFormat.js
 * @requires org.GeoPrisma.InitialView.View.js
 */

/** api: (define)
 *  module = org.GeoPrisma.InitialView
 *  class = Manager
 */

/** api: constructor
 *  .. class:: Manager
 */
org.GeoPrisma.InitialView.Manager = Ext.extend(Ext.util.Observable, {

    // Public Properties (Mandatory)

    /** api: property[mapPanel]
     *  :class:`GeoExt.MapPanel`
     *  A reference to the MapPanel object.
     */
    mapPanel: null,

    // Public Properties (Optional)

    /** api: property[allowLayerToggling]
     *  ``Boolean``
     *  Sets the allowLayerToggling of created views.
     */
    allowLayerToggling: true,

    /** api: property[highlight]
     *  ``Boolean``
     *  Sets highlight property of created views.
     */
    highlight: false,

    /** api: property[highlightLayer]
     *  :class:``OpenLayers.Layer.Vector``
     *  A vector layer to use for highlight purpose for created views.
     */
    highlightLayer: null,

    /** api: property[localViewField]
     *  ``String``
     *  The url parameter to set in order to use local views. Defaults to
     *  "localViewField"
     */
    localViewField: "localViewField",

    /** api: property[localViews]
     *  ``Array``
     *  Array of local views.  Each are a comma separated string reprensenting
     *  locations.  Can have 2 (LonLat) or 4 (Bounds) coordinates.
     */
    localViews: null,

    /** api: property[maxZoom]
     *  ``Integer``
     *  The maximum level that can be zoomed to by this widget.
     */
    maxZoom: null,

    /** api: property[highlight]
     *  ``Boolean``
     *  Defaults to false. If set, replaces the map zoomToMaxExtent method for
     *  one recentering on the view instead.
     */
    replaceZoomToMaxExtent: false,

    // Private Properties

    /** api: property[reqSent]
     *  ``Integer``
     *  Number of requests sent.  Only used when using AsyncViews.
     */
    reqSent: null,

    /** api: property[reqReceived]
     *  ``Integer``
     *  Number of request callbacks received.  Only used when using AsyncViews.
     */
    reqReceived: null,

    /** api: property[views]
     *  ``Array``
     *  Array of ``org.GeoPrisma.InitialView.View`` objects. Populated by
     *  the addView method.
     */
    views: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
        this.views = [];
        this.reqSent = 0;
        this.reqReceived = 0;
        if (this.localView) {
            this.localViews = [this.localView];
            delete this.localView;
        }
        this.localViews = this.localViews || [];
    },

    /** private: method[getViewDefaultOptions]
     *  :return: ``Object`` Hash of options
     *
     *  Returns a hash of default options to use when creating new
     *  ``org.GeoPrisma.InitialView.View`` objects.
     */
    getViewDefaultOptions: function() {
        return {
            allowLayerToggling: this.allowLayerToggling,
            highlight: this.highlight,
            highlightLayer: this.highlightLayer || null,
            mapPanel: this.mapPanel,
            maxZoom: this.maxZoom,
            replaceZoomToMaxExtent: this.replaceZoomToMaxExtent
        }
    },

    /** private: method[onMapPanelAfterRender]
     *  Callback method of the "afterrender" event fired for the MapPanel.
     *  Listen to the MapPanel container "afterlayout" event if MapPanel is
     *  not yet ready to be recentered.
     */
    onMapPanelAfterRender: function() {
        if(!this.mapPanel.ownerCt) {
            this.zoomToViewExtent();
        } else {
            this.mapPanel.ownerCt.on({
                "afterlayout": this.onMapPanelOwnerCtAfterLayout,
                scope: this
            });
        }
    },

    /** private: method[onMapPanelOwnerCtAfterLayout]
     *  Callback method of the "afterlayout" event fired for the MapPanel
     *  container.  From that moment on, the MapPanel is ready to be recentered,
     *  so trigger the zoomToViewExtent method.
     */
    onMapPanelOwnerCtAfterLayout: function() {
        var width = this.mapPanel.getInnerWidth() -
            this.mapPanel.body.getBorderWidth("lr");
        var height = this.mapPanel.getInnerHeight() -
            this.mapPanel.body.getBorderWidth("tb");
        if (width > 0 && height > 0) {
            this.mapPanel.ownerCt.un(
                "afterlayout", this.onMapPanelOwnerCtAfterLayout, this);
            this.zoomToViewExtent();
        }
    },

    // Public methods

    /** public: method[createLocalView]
     *  :param index: ``Integer`` The index of the local view
     *
     *  Add a new ``org.GeoPrisma.InitialView.View`` object using the localView
     *  at the specified index.
     */
    createLocalView: function(index) {
        this.localViews[index] &&
            this.createView({featuresString: this.localViews[index]});
    },

    /** public: method[createView]
     *  :param viewOptions: ``Object`` A hash of options for the view
     *
     *  Create a new ``org.GeoPrisma.InitialView.View`` object using options and
     *  default options and ad .
     */
    createView: function(viewOptions) {
        this.addView(new org.GeoPrisma.InitialView.View(
            Ext.applyIf(this.getViewDefaultOptions(), viewOptions)));
    },

    /** public: method[createAsyncView]
     *  :param viewOptions: ``Object`` A hash of options for the view
     *
     *  Pushes the view in the view array and trigger its read method
     */
    createAsyncView: function(viewOptions) {
        this.reqSent++;
        var view = new org.GeoPrisma.InitialView.AsyncView(
            Ext.applyIf(this.getViewDefaultOptions(), viewOptions));
        view.on("afterread", function() {
            this.reqReceived++;
            this.setCenter();
        }, this);
        this.addView(view);
    },

    /** public: method[addView]
     *  :param view: ``org.GeoPrisma.InitialView.View``
     *
     *  Pushes the view in the view array and trigger its read method
     */
    addView: function(view) {
        this.views.push(view);
        view.read();
    },

    /** public: method[setCenter]
     *  Is called once in the widget 'printWidgetExecution' method and also
     *  once per asyncView callback received.
     *  
     *  When all sent requests were received or if none, trigger the
     *  zoomToViewExtent method.  If the map has no baseLayer yet, it must
     *  triggered after the map is ready (for it to have a size and scales set).
     */
    setCenter: function() {
        if (this.reqSent != this.reqReceived) {
            return;
        }
        if (this.reqSent === 0 && !this.mapPanel.map.baseLayer) {
            this.mapPanel.on("afterrender", this.onMapPanelAfterRender, this);
        } else {
            this.zoomToViewExtent();
        }
    },

    /** public: method[zoomToViewExtent]
     *  Browse each ``org.GeoPrisma.InitialView.View`` that were created.  The
     *  first one being valid is then used to set the map center.
     */
    zoomToViewExtent: function() {
        Ext.each(this.views, function(view, index, views) {
            if (view.isValid()) {
                view.zoomToFeaturesExtent();
                return false;
            }
        }, this);
    }
});
