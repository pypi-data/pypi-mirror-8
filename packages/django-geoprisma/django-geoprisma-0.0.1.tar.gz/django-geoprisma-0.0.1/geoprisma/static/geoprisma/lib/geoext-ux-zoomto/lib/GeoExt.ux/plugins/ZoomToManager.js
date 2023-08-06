/**
 * Copyright (c) 2008-2012 The Open Source Geospatial Foundation
 * 
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

Ext.namespace("GeoExt.ux");

/*
 * @requires GeoExt.ux/widgets/ZoomTo.js
 */

/** api: (define)
 *  module = GeoExt.ux
 *  class = ZoomToManager
 */

/** api: constructor
 *  .. class:: ZoomToManager
 */
GeoExt.ux.ZoomToManager = Ext.extend(Ext.util.Observable, {

    /** api: property[zoomTo]
     * :class:``GeoExt.ux.ZoomTo``
     * A reference to the ZoomTo widget.  Mandatory.
     */
    zoomTo: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
        this.addEvents(
            /** private: event[markerchanged]
             *  Fired by zoomTo when adding, removing or dragging the marker
             */
            "markerchanged"
        );
    }
});
