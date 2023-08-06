/**
 * Copyright (c) 2011- Mapgears Inc., published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license.
 */

Ext.namespace("GeoExt.ux.PrintPreviewAction");

/*
 * @requires GeoExt.ux/PrintPreview.js
 */

/** api: (define)
 *  module = GeoExt.ux
 *  class = PrintPreviewAction
 */

/** api: constructor
 *  .. class:: PrintPreviewAction
 */
GeoExt.ux.PrintPreviewAction = Ext.extend(Ext.Action, {

    /* i18n  */

    /** api: config[tooltip] ``String`` i18n */
    tooltip: "Open print dialog",

    /** api: config[windowTitleText] ``String`` i18n */
    windowTitleText: "Print dialog",

    /** api: config[mapTitleText] ``String`` i18n */
    mapTitleText: "Map title",

    /** api: config[activeDrawFeatureControlText] ``String`` i18n */
    activeDrawFeatureControlText: "One draw control is currently active. "+
        "Please, turn it off first.",

    /** api: config[localVectorLayerVisibleText] ``String`` i18n */
    localVectorLayerVisibleText: "An incompatible vector layer currently "
        +"visible.  Please turn it off first",

    /* API */

    /** api: config[defaultOptions]
     * ``Object`` default options for this widget.
     */
    defaultOptions: {
        iconCls: "icon-print"
    },

    /** api: config[mapPanel]
     * :class:`GeoExt.MapPanel` from which to print the layers
     */
    mapPanel: null,

    /** api: config[printCapabilities]
     * ``Object`` Hash of print capabilities used to create the
     *       :class:`GeoExt.data.PrintProvider` object.
     */
    printCapabilities: null,

     /* PRIVATE*/

    /** private: property[window]
     *  :class:`Ext.Window` A reference to the window used to display the print
     *      preview.  Debug purpose only.
     */
    window: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        // private methods
        config.handler = this.handler;
        config.canPrint = this.canPrint;

        // i18n
        Ext.apply(config, Ext.apply(this.defaultOptions, {
            tooltip: this.tooltip,
            windowTitleText: this.windowTitleText,
            mapTitleText: this.mapTitleText,
            activeDrawFeatureControlText: this.activeDrawFeatureControlText,
            localVectorLayerVisibleText: this.localVectorLayerVisibleText
        }));

        arguments.callee.superclass.constructor.call(this, config);
    },

    /** private: method[handler]
     */
    handler: function() {
        if (!this.mapPanel) {
            this.mapPanel = GeoExt.MapPanel.guess();
        }

        if (!this.canPrint()) {
            return false;
        }

        var printProvider = new GeoExt.data.PrintProvider({
            method: "POST",
            capabilities: this.printCapabilities
        });
        var printWindow = new Ext.Window({
            title: this.windowTitleText,
            modal: true,
            border: false,
            resizable: false,
            width: 360,
            autoHeight: true,
            items: new GeoExt.ux.PrintPreview({
                autoHeight: true,
                printMapPanel: {
                    limitScales: true,
                    map: {controls: [
                        new OpenLayers.Control.Navigation({
                            zoomBoxEnabled: false,
                            zoomWheelEnabled: false
                        }),
                        new OpenLayers.Control.PanPanel()
                    ]}
                },
                printProvider: printProvider,
                includeLegend: false,
                mapTitle: this.mapTitleText,
                sourceMap: this.mapPanel
                //,legend: this.legendPanel // not yet supported
            })
        });
        printProvider.on("print", function() {
            this.window.close();
            this.window = null;
        }, {window: printWindow});
        printWindow.show().center();
        this.window = printWindow;
    },

    /** private: method[canPrint]
     *  :return: ``Boolean`` Whether the current map can be printed or not.  
     *
     *  Alerts the reason when the map can't be printed (see below).
     */
    canPrint: function() {
        var cantPrintMessage = "", layer;

        // Can't print if an OpenLayers.Control.DrawFeature control is active
        Ext.each(this.mapPanel.map.controls, function(control){
            if (control instanceof OpenLayers.Control.DrawFeature &&
                control.active) {
                cantPrintMessage = this.activeDrawFeatureControlText;
                return false;
            }
        }, this);
        
        // Can't print if an OpenLayers.Layer.Vector with a protocol or
        // stragegies has features and is visible.
        cantPrintMessage != "" && this.mapPanel.layers.each(function(record) {
            layer = record.getLayer();
            if (layer instanceof OpenLayers.Layer.Vector &&
                layer.getVisibility() &&
                layer.features.length &&
                layer.protocol ||
                (layer.strategies && layers.strategies.length)
            ) {
                cantPrintMessage = this.localVectorLayerVisibleText;
                return false;
            }
        }, this);

        cantPrintMessage != "" && alert(cantPrintMessage);
        return cantPrintMessage == "";
    }
});
