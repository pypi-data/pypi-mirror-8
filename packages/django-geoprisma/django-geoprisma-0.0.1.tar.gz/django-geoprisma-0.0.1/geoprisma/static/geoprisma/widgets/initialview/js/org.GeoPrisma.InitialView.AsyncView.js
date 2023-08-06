/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.InitialView");

/*
 * @requires org.GeoPrisma.InitialView.View.js
 */

/** api: (define)
 *  module = org.GeoPrisma.InitialView
 *  class = AsyncAsync
 */

/** api: constructor
 *  .. class:: AsyncView
 */
org.GeoPrisma.InitialView.AsyncView = Ext.extend(org.GeoPrisma.InitialView.View, {

    // Public Properties (Mandatory)

    /** api: property[filterProperty]
     *  ``String``
     *  Used as 'property' parameter value in the filter to get the features
     */
    filterProperty: null,

    /** api: property[filterValue]
     *  ``String``
     *  Used as 'value' parameter value in the filter to get the features
     */
    filterValue: null,

    /** api: property[layerName]
     *  ``String``
     *  Used as 'featureType' parameter value in the reader (protocol)
     */
    layerName: null,    

    /** api: property[serviceName]
     *  ``String``
     *  Added to the url for the proxy call
     */
    serviceName: null,

    /** api: property[url]
     *  ``String``
     *  The url of the proxy
     */
    url: null,

    // Private Properties

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);

        this.addEvents(
            /** private: event[afterread]
             *  Fires after the read of features is complete.
             */
            "afterread"
        );
    },

    /** private: method[createReader]
     *  Sets the format property using serviceType.
     */
    createReader: function() {
        switch (this.serviceType)
        {
            case "wfs":
                this.reader = new OpenLayers.Protocol.WFS({
                    url: OpenLayers.Util.urlAppend(this.url,
                        OpenLayers.Util.getParameterString({
                            'osmresource': this.resourceName,
                            'osmservice': this.serviceName
                    })),
                    featureType: this.layerName
                })
                break;
        }
    },

    /** private: method[read]
     *  Triggers the Async read request.
     */
    read: function() {
        this.reader.read({
            'filter': new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.EQUAL_TO,
                property: this.filterProperty,
                value: this.filterValue
            }),
            callback: this.onRead,
            scope: this
        });
    },

    /** private: method[onRead]
     *  Callback method of the protocol read.  Sets the features property with
     *  those returned by the request and fires the "afterread" event.
     */
    onRead: function(response) {
        this.features = response.features || [];
        this.fireEvent("afterread", this);
    }
});
