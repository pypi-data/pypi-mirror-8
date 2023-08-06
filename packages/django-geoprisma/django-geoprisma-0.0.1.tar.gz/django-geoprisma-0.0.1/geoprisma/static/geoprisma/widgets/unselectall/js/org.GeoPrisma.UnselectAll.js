/* 
   Copyright (c) 2009-2012 Mapgears Inc.
   Published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/

Ext.namespace("org.GeoPrisma")

/*
 * @requires GeoExt/widgets/Action.js
 */

/** api: (define)
 *  module = org.GeoPrisma
 *  class = UnselectAll
 */

/** api: constructor
 *  .. class::  UnselectAll
 */
org.GeoPrisma.UnselectAll = Ext.extend(Ext.Action, {

    /* begin i18n */
    /** api: config[unselectAllText] ``String`` i18n */
    unselectAllText: "Deselect All",
    /* end i18n */

    /** private: property[map]
     *  ``OpenLayers.Map``
     */
    map: null,

    /** private: property[useIcons]
     *  ``Boolean``
     *  If set to true, enables the use of image icons.  Must be combined with
     *  a .css (see in resources/css).
     */
    useIcons: true,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);

        arguments.callee.superclass.constructor.call(this, config);
        this.setHandler(this.onActionClick, this);

        if (this.useIcons === true) {
            this.setIconClass("gp-unselectall");
        } else {
            this.setText(this.unselectAllText);
        }
    },

    /** private: method[onActionClick]
     *  Called when action is clicked.
     */
    onActionClick: function() {
        for (i=0, len=this.map.controls.length; i<len; i++) {
            if (this.map.controls[i].CLASS_NAME ==
                "OpenLayers.Control.SelectFeature") {
                this.map.controls[i].unselectAll();
            }
        }

        this.map.events.triggerEvent("unselectallfeatures", {});
    }
});
