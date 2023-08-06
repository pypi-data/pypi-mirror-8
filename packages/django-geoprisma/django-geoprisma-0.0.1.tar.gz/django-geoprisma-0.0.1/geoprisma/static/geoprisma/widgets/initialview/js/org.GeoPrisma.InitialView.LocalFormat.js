/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.InitialView");

/** api: (define)
 *  module = org.GeoPrisma.InitialView
 *  class = LocalFormat
 */

/** api: constructor
 *  .. class:: LocalFormat
 */
org.GeoPrisma.InitialView.LocalFormat = Ext.extend(Ext.util.Observable, {

    /** private: method[read]
     *  :param text: ``String`` A document string containing features
     *  :return: ``Array`` of OpenLayers.Feature.Vector or OpenLayers.Bounds
     *  
     *  Read the text string and return the array of features/bounds.
     */
    read: function(text) {
        var features = [];
        var array = text.split(",");
        switch (array.length)
        {
            case 2:
                features.push(new OpenLayers.Feature.Vector(
                    new OpenLayers.Geometry.Point(array[0], array[1])
                ));
                break;
            case 4:
                features.push(OpenLayers.Bounds.fromArray(array));
                break;
        }
        return features;
    }
});
