/* 
   Copyright (c) 2010- Mapgears Inc., published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 

/**
 * APIMethod: show
 * Intelligent way to show a layer, i.e. if it has a 'params' property and 
 * the layer was build from multiple resources, merge new 'params' using 
 * this.layersByResource property.
 *
 * Also force the visibility to true in all cases.
 *
 * Parameter:
 * resourceName - {String} A resource name used if the layer has 'params'
 *                         property.
 */
OpenLayers.Layer.prototype.show = function(resourceName){
    if(resourceName && (typeof(this.params) != 'undefined') &&
       (typeof(this.layersByResource) != 'undefined')){
        params = OpenLayers.Util.upperCaseObject(this.params);
        sublayers = params['LAYERS'];

        sublayerToShow = this.layersByResource[resourceName];

        var p = {};
        p["LAYERS"] = [sublayerToShow];
        this.mergeNewParams(p);
    }

    this.setVisibility(true);
};
