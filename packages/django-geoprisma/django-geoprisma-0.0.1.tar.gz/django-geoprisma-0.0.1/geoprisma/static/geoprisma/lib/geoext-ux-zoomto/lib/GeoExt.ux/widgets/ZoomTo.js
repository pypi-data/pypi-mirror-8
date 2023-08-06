/**
 * Copyright (c) 2008-2010 The Open Source Geospatial Foundation
 * 
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

Ext.namespace("GeoExt.ux")

/*
 * @requires GeoExt/widgets/Action.js
 */

/** api: (define)
 *  module = GeoExt.ux
 *  class = ZoomTo
 */

/** api: constructor
 *  .. class:: ZoomTo 
 */
GeoExt.ux.ZoomTo = Ext.extend(Ext.Action, {

    /* begin i18n */
    /** api: config[zoomToText] ``String`` i18n */
    zoomToText: "ZoomTo",

    /** api: config[xCoordinateText] ``String`` i18n */
    xCoordinateText: "X coordinate",

    /** api: config[yCoordinateText] ``String`` i18n */
    yCoordinateText: "Y coordinate",

    /** api: config[projectionText] ``String`` i18n */
    projectionText: "Projection",

    /** api: config[invalidEntryText] ``String`` i18n */
    invalidEntryText: "invalid entry",

    /** api: config[widgetTitleText] ``String`` i18n */
    widgetTitleText: "ZoomTo widget",

    /** api: config[destroyMarkerActionText] ``String`` i18n */
    destroyMarkerActionText: "Remove +",

    /** api: config[closeActionText] ``String`` i18n */
    closeActionText: "Close",

    /** api: config[zoomActionText] ``String`` i18n */
    zoomActionText: "Zoom",

    /** api: config[errorText] ``String`` i18n */
    errorText: "Error",

    /** api: config[missingProjectionText] ``String`` i18n */
    missingProjectionText: "The projection is missing.",

    /** api: config[missingCoordsText] ``String`` i18n */
    missingCoordsText: "Missing or invalid coordinates.",

    /** api: config[outOfRangCoordsText] ``String`` i18n */
    outOfRangCoordsText: "Coordinates are out of current extent range.",
    /* end i18n */

    // Public Properties

    /** public: property[autoHideWindowOnZoom]
     *  ``Boolean``
     *  If set to true, hides the window after recentering.
     */
    autoHideWindowOnZoom: true,

    /** public: property[defaultZoomLevel]
     *  ``Integer``
     */
    defaultZoomLevel: null,

    /** public: property[defaultZoomLevel]
     *  ``Boolean``
     *  Defaults to false.  If set to true, the center marker can be dragged.
     */
    enableDrag: false,

    /** public: property[showCenter]
     *  ``Boolean``
     *  If set to true, shows a red cross marker on the center of the map
     *  after recentering.
     */
    showCenter: true,

    /** public: property[useIcons]
     *  ``Boolean``
     *  If set to true, enables the use of image icons.  Must be combined with
     *  a .css (see in resources/css).
     */
    useIcons: true,

    // Private Properties

    /** private: property[currentProjection]
     *  ``String``
     *  Automatically set to a projection code from the comboBox on select.
     */
    currentProjection: null,

    /** private: property[dragControl]
     *  ``OpenLayers.Control.Drag``
     *  Used to drag the center marker around after recentering.  The position
     *  displayed in the fields is automatically changed according to its new
     *  position.
     */
    dragControl: null,

    /** private: property[form]
     *  ``Ext.form.FormPanel``
     */
    form: null,

    /** private: property[manager]
     *  ``GeoExt.ux.ZoomToManager``
     *  Used to fire events for exernal components to listen to this widget
     */
    manager: null,

    /** private: property[map]
     *  ``OpenLayers.Map``
     */
    map: null,

    /** private: property[projectionStore]
     *  ``Ext.data.SimpleStore``
     */
    projectionStore: null,

    /** private: property[window]
     *  ``Ext.Window``
     */
    window: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);

        this.initMap();
        arguments.callee.superclass.constructor.call(this, config);
        this.setHandler(this.onActionClick, this);

        if (this.useIcons === true) {
            this.setIconClass("gx-zoomto-recenteroncoords");
        } else {
            this.setText(this.zoomToText);
        }

        this.createWindow();
        this.manager = new GeoExt.ux.ZoomToManager({zoomTo: this});
    },

    /** private: method[initMap]
     *  Convenience method to make sure that the map object is correctly set.
     */
    initMap: function() {
        if (this.map instanceof GeoExt.MapPanel) {
            this.map = this.map.map;
        }

        if (!this.map) {
            this.map = GeoExt.MapPanel.guess().map;
        }

        // if no toggleGroup was defined, set to this.map.id
        if (!this.toggleGroup) {
            this.toggleGroup = this.map.id;
        }
    },

    /** private: method[onActionClick]
     *  Called when action is clicked.
     */
    onActionClick: function() {
        this.window.show();
    },

    /** private: method[createWindow]
     *  Creates a new Ext.Window object containing all fields used to zoom
     */
    createWindow: function() {
        if (!this.projectionStore) {
            this.projectionStore = new Ext.data.SimpleStore({
                fields: ['projection'],
                data : [
                    ['EPSG:4326'],
                    ['EPSG:900913']
                ]
            });
        }

        // get first value of store as default value
        var defaultProj = this.projectionStore.data.items[0].data[
            this.projectionStore.getAt(0).fields.get(0)['name']
        ];
        this.currentProjection = defaultProj;

        // FormPanel
        this.form = new Ext.form.FormPanel({
            border: false,
            plain: true,
            defaults: {width: 170},
            defaultType: 'textfield',
            labelAlign: 'top',
            bodyStyle:'padding:5px 5px 0',
            items: [{
                    fieldLabel: this.projectionText,
                    name: 'projection',
                    value: defaultProj,
                    xtype: 'combo',
                    store: this.projectionStore,
                    displayField: 'projection',
                    typeAhead: true,
                    mode: 'local',
                    forceSelection: true,
                    triggerAction: 'all',
                    allowBlank: false,
                    invalidText: this.invalidEntryText,
                    emptyText: "",
                    selectOnFocus:true,
                    listeners: {
                        "select": this.onProjectionSelect,
                        scope: this
                    }
                },{
                    fieldLabel: this.xCoordinateText,
                    name: 'coordx'
                },{
                    fieldLabel: this.yCoordinateText,
                    name: 'coordy' 
                }
            ]
        });

        var windowButtons = [];

        // remove marker button (optional)
        if (this.showCenter === true) {
            windowButtons.push({
                text: this.destroyMarkerActionText,
                scope: this,
                handler: function(){
                    this.destroyMarker();
                    this.dragControl && this.dragControl.deactivate();
                }
            });
        }

        // zoom button
        windowButtons.push({
            text: this.zoomActionText,
            scope: this,
            handler: function(){
                this.recenter(this.form.getForm().getValues());
            }
        });

        // Window with buttons
        this.window = new Ext.Window({
            title: this.widgetTitleText,
            layout: 'form',
            width: 200,
            autoHeight: true,
            height: 'auto',
            closeAction: 'hide',
            modal: false,
            plain: false,
            resizable: false,
            buttonAlign: 'center',
            items: [this.form],
            buttons: windowButtons
        });
    },

    /** private: method[onProjctionSelect]
     *  :param comboBox: ``Ext.form.ComboBox``
     *  :param record: ``Ext.data.Record``
     *  :param index: ``Integer``
     *  
     *  Callback method of the projection comboBox "select" event.  Manage
     *  projection change and reproject the coordinates if any.
     */
    onProjectionSelect: function(comboBox, record, index) {
        var newProj = record.get("projection");
        if (this.currentProjection == newProj) {
            return;
        }
        // manage projection change
        var oldProj = this.currentProjection;
        var values = this.form.getForm().getValues();
        if (values.coordx != "" && values.coordy != "") {
            var point = this.getTransformedCoords(
                values.coordx, values.coordy, oldProj, newProj);
            this.setValues({coordx: point.x, coordy: point.y});
        }
        this.currentProjection = newProj;
    },

    /** public: method[recenter]
     *  :param values: ``Object`` Hash of values to uze to recenter.  Possible
     *                            values are :
     *    - coordx     : (Float) Mandatory. The X coordinate
     *    - coordy     : (Float) Mandatory. The Y coordinate
     *    - projection : (String) Mandatory.  The projection code of the
     *                   coordinates
     *    - zoom       : (Integer) Optional.  The zoom level to use
     *  
     *  Recenters map using user-provided coordinates and scale.
     */
    recenter: function(values) {
        if (values.projection == "") {
            this.showError(this.missingProjectionText);
            return false;
        }

        // make sure the window is rendered first because this method is public
        // and could be called before the action button was clicked
        if (!this.window.rendered) { 
            this.window.render(Ext.getBody()); 
        } 

        var transformedCoords = this.getTransformedCoords(
            values.coordx, values.coordy, values.projection
        );

        var x = transformedCoords['x'];
        var y = transformedCoords['y'];
        
        if (this.checkCoords(x, y)) {
            
            var zoom;

            if (Ext.isNumber(values.zoom)) {
                // use user-provided zoom
                zoom = values.zoom;
            } else if (this.scales && values.scaleValue) {
                // use user-provided scale to calculate zoom
                resolution = OpenLayers.Util.getResolutionFromScale(values.scaleValue,
                this.map.units);
                zoom = this.map.getZoomForResolution(resolution);
            } else if (this.defaultZoomLevel) {
                zoom = this.defaultZoomLevel;
            }

            this.recenterOnCoords(x, y, zoom);
        }
    },

    /** public: method[setValues]
     *  :param values: ``Object`` Hash of values to uze to recenter.  See
     *                            above 'recenter' method to know possible keys
     *  
     *  Sets values for fields in basic form in bulk.  Also set current
     *  projection if set in values.
     */
    setValues: function(values) {
        if (values.projection) {
            this.currentProjection = values.projection;
        }
        this.form.getForm().setValues(values);
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

    /** private: method[checkCoords]
     *  Checks that submitted coordinates are well-formatted and within the map
     *      bounds.
     *
     *  Parameters:
     *  x {Float} - easting coordinate
     *  y {Float} - northing coordinate
     *
     *  Returns: 
     *  {Boolean}
     */
    checkCoords: function(x, y) {
    
        if (!x || !y) {
            this.showError(this.missingCoordsText);
            return false;
        }

        var maxExtent = this.map.getMaxExtent();
    
        if (x < maxExtent.left || x > maxExtent.right ||
            y < maxExtent.bottom || y > maxExtent.top) {
            this.showError(this.outOfRangCoordsText);
            return false;
        }
    
        return true;
    },

    /** private: method[recenterOnCoords]
     *  Recenters on given coordinates and zoom level
     *
     *  Parameters:
     *  x -    {Float}   easting coordinate
     *  y -    {Float}   northing coordinate
     *  zoom - {Integer} zoom level (optional)
     */
    recenterOnCoords: function(x, y, zoom) {
        
        // use default zoom level if provided in widget config, 
        // else keep current zoom level
        if (typeof(zoom) == 'undefined') {
            zoom = (typeof(this.defaultZoom) != 'undefined') 
                   ? this.defaultZoom : this.map.getZoom()
        }

        if (this.showCenter) {
            // display a symbol on the new center point
            this.showCenterMark(x, y);
        }

        this.map.setCenter(new OpenLayers.LonLat(x, y), zoom);

        if (this.autoHideWindowOnZoom === true) 
        {
            this.window.hide();
        }
    },

    /** private: method[showCenterMark]
     *  Materializes new center with a cross
     *
     *  Parameters:
     *  x - {Float} easting coordinate
     *  y - {Float} northing coordinate
     */
    showCenterMark: function(x, y) {
        this.prepareVectorLayer();
        this.enableDrag && this.prepareDragControl();

        var features = [
            new OpenLayers.Feature.Vector(
                new OpenLayers.Geometry.Point(x, y),
                { type: this.symbol || 'cross' }
            )
        ];

        this.vectorLayer.addFeatures(features);
        this.manager.fireEvent("markerchanged", features[0]);
    },

    /** private: method[prepareVectorLayer]
     *  Adds a layer for displaying the center symbol. If it is already set,
     *  removes existing features.
     */
    prepareVectorLayer: function() {
        if (this.vectorLayer) {
            this.destroyMarker();
        } else {
            var styles = new OpenLayers.StyleMap({
                "default": OpenLayers.Util.extend({
                    // retrieved from symbol type attribute
                    graphicName: "${type}",
                    pointRadius: 10,
                    fillColor: "red",
                    fillOpacity: 1
                }, this.centerMarkStyles)
            });

            this.vectorLayer = new OpenLayers.Layer.Vector(
                "Center Symbol", {
                    styleMap: styles,
                    alwaysInRange: true
                }
            );

            this.map.addLayer(this.vectorLayer);
        }
    },

    /** private: method[prepareVectorLayer]
     *  Adds a layer for displaying the center symbol. If it is already set,
     *  removes existing features.
     */
    prepareDragControl: function() {
        if (!this.dragControl) {
            this.dragControl = new OpenLayers.Control.DragFeature(
                this.vectorLayer, {
                    onDrag: this.onMarkerDrag,
                    zoomToWidget: this
                }
            );
            this.map.addControl(this.dragControl);
        }
        this.dragControl.activate();
    },

    /** private: method[onMarkerDrag]
     *  Callback method of the drag control. Triggered when the marker is
     *  dragged.
     */
    onMarkerDrag: function(feature, pixel) {
        var me = this.zoomToWidget;
        var point = me.getTransformedCoords(
            feature.geometry.x,
            feature.geometry.y,
            me.map.getProjection(),
            me.form.getForm().getValues().projection
        );
        me.setValues({
            coordx: point.x,
            coordy: point.y
        });
        me.manager.fireEvent("markerchanged", feature);
    },

    /** private: method[destroyMarker]
     *  Removes existing features from vector layer
     */
    destroyMarker: function() {
        if (this.vectorLayer) {
            this.vectorLayer.destroyFeatures();
        }
        this.manager.fireEvent("markerchanged", false);
    },

    /** private: method[showError]
     *  Displays an error message
     *
     *  Parameters:
     *  msg - {String} message
     *  title - {String} box title
     */
    showError: function(msg, title) {
        title = title || this.errorText;
        Ext.Msg.alert(title, msg);
    }
});
