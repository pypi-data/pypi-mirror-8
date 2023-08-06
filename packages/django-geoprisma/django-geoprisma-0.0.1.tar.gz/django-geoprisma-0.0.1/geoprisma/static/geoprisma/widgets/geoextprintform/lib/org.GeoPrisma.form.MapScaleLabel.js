/**
 * Copyright (c) 2009-2011 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.form");

/** api: (define)
 *  module = org.GeoPrisma.form
 *  class = MapScaleLabel
 */

/** api: constructor
 *  .. class:: MapScaleLabel
 */
org.GeoPrisma.form.MapScaleLabel = Ext.extend(Ext.form.Label, {

    /* i18n */

    /** api: property[fieldLabel] ``String`` i18n */
    fieldLabel: "Current Map Display",

    /** api: property[differentScalesTooltipText] ``String`` i18n */
    differentScalesTooltipText: "<b>Warning</b> : Print and map scales are " +
        "different. The map in the PDF may differ from the one currently " +
        "visible",

    /** api: property[sameScalesTooltipText] ``String`` i18n */
    sameScalesTooltipText: "Print and map scales are the same.",

    /* API Properties (Mandatory) */

    /** api: property[map]
     * ``:class: OpenLayers.Map``
     * The map object in which to add the scale control.
     */
    map: null,

    /** api: property[printPage]
     * ``:class: GeoExt.data.PrintPage``
     * The print page widget controling the scale.
     */
    printPage: null,

    /* API Properties (Optional) */

    /** api: property[geodesic]
     * ``Boolean`` Used to set the geodesic property of the scale control.
     */
    geodesic: false,

    /** api: property[differentScalesCls]
     * ``String`` Class name used when both map and page scales are different.
     */
    differentScalesCls: "gx-geoextprintform-mapscalelabel-differentscales",

    /** api: property[sameScalesCls]
     * ``String`` Class name used when both map and page scales are the same.
     */
    sameScalesCls: "gx-geoextprintform-mapscalelabel-samescales",

    /* Private Properties */

    /** api: property[scaleControl]
     * ``:class: OpenLayers.Control.Scale``
     * The scale control created by this widget.
     */
    scaleControl: null,

    /** api: property[sameScales]
     * ``Boolean`` Used to avoid managing scales more than one time.
     */
    sameScales: true,

    /** api: property[tooltip]
     * ``:class: Ext.ToolTip``
     */
    tooltip: null,

    /** private: method[constructor]
     *  This class is a superconstructor only.
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);

        this.addClass(this.sameScalesCls);
        this.on("afterrender", this.onAfterRender, this);
    },

    /** private: method[onAfterRender]
     *  Called on "afterrender" event fired for this object.  Create a scale
     *  control, a tooltip, then listen to map "moveend" event and printPage
     *  "change" event to manage the scales accordingly.
     */
    onAfterRender: function() {
        // scale control
        this.scaleControl = new OpenLayers.Control.Scale(null, {
            geodesic: this.geodesic,
            div: this.getEl()
        });
        this.map.addControl(this.scaleControl);

        // tooltip
        this.tooltip = this.getNewToolTip();

        // event listeners
        this.map.events.on({
            "moveend": this.onMapMoveEnd,
            "scope": this
        });
        this.printPage.on("change", this.onPrintPageChange, this);
    },

    /** private: method[onMapMoveEnd]
     *  Called on map "moveend" event fired. Manage the scales accordingly.
     */
    onMapMoveEnd: function() {
        this.manageScales();
    },

    /** private: method[onPrintPageChange]
     *  :param mods: ``Object`` A hash of modifications made to the printPage.
     *  Called on printPage "change" event fired. Manage the scales accordingly
     *  if the modification made was 'scale'.
     */
    onPrintPageChange: function(mods) {
        if (mods && mods.scale) {
            this.manageScales();
        }
    },

    /** private: method[manageScales]
     *  Get both map and printPage scales. If they are different, create and
     *  bind a tooltip, else remove it. Also, set cls accordingly.
     */
    manageScales: function() {
        var pageScale = Math.round(this.printPage.scale.get("value"));
        var mapScale = Math.round(this.map.getScale());
        var differentScales = pageScale != mapScale;

        if (differentScales && this.sameScales) {
            this.sameScales = false;
            this.manageToolTip();
            this.removeClass(this.sameScalesCls);
            this.addClass(this.differentScalesCls);
        } else if (!differentScales && !this.sameScales) {
            this.sameScales = true;
            this.manageToolTip();
            this.removeClass(this.differentScalesCls);
            this.addClass(this.sameScalesCls);
        }
    },

    /** private: method[manageToolTip]
     *  Change the content of the tooltip according to the sameScales property
     */
    manageToolTip: function() {
        var tooltipText = (this.sameScales)
            ? this.sameScalesTooltipText : this.differentScalesTooltipText;
        if (this.tooltip.rendered) {
            this.tooltip.update(tooltipText);
        } else {
            this.tooltip.html = tooltipText;
        }
    },

    /** private: method[getNewToolTip]
     *  :return: ``:class: Ext.ToolTip`` A tooltip containing a warning message.
     */
    getNewToolTip: function() {
        return new Ext.ToolTip({
            target: this.getEl(),
            anchor: 'top',
            anchorOffset: 85,
            dismissDelay: 0,
            html: this.sameScalesTooltipText
        });
    }
});
