/* 
   Copyright (c) 2010- Mapgears Inc., published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/**
 * APIMethod: getLayerByResource
 * Get a layer with resource matching the given resource in its resources
 * array.
 *
 * Parameter:
 * match - {String} A resource name.  If no layers are found, an empty array is
 *                  returned.
 * serviceType - {String} (Optional) A service type name.  If defined, the layer
 *                        must also be of this type.
 *
 * Returns:
 * {Array(<OpenLayers.Layer>)} A array of layers matching the given resource
 *     name.  An empty array is returned if no matches are found.
 */
OpenLayers.Map.prototype.getLayersByResource = function(match, serviceType){
    var layers = [];
    for(var i=0; i<this.layers.length; i++){
        layer = this.layers[i];
        
        if(!layer.resources){
            continue;
        }
        
        if(OpenLayers.Util.indexOf(layer.resources, match) == -1){
            continue;
        }

        layerServiceType = (layer.servicetype) ? layer.servicetype : layer.serviceType;
        if(serviceType && layerServiceType != serviceType){
            continue;
        }
        
        layers.push(layer);
    }
    return layers;
};

/**
 * Constant: EVENT_TYPES
 * Add 'GeoPrisma' specific map event types.
 * - unselectallfeatures
 * - printallwidgetexecutions : called after printAllWidgetExecutions
 */
OpenLayers.Map.prototype.EVENT_TYPES =
    OpenLayers.Map.prototype.EVENT_TYPES.concat(['unselectallfeatures',
                                                 'printallwidgetexecutions']);

/**
 * APIMethod: getMaxExtent
 * Parameters:
 * options - {Object} 
 * 
 * Allowed Options:
 * restricted - {Boolean} If true, returns restricted extent (if it is 
 *     available.)
 *
 * Returns:
 * {<OpenLayers.Bounds>} The maxExtent property as set on the current 
 *     baselayer, unless the 'restricted' option is set, in which case
 *     the 'restrictedExtent' option from the map is returned (if it
 *     is set), or unless 'allOverlays' is true for the map, in which
 *     case the maxExtent property of the map is returned.
 *
 * Override until fixed in OpenLayers, see :
 *     http://trac.osgeo.org/openlayers/ticket/2178
 */
OpenLayers.Map.prototype.getMaxExtent = function (options) {
    var maxExtent = null;
    if(options && options.restricted && this.restrictedExtent){
        maxExtent = this.restrictedExtent;
    } else if (this.baseLayer != null && !this.allOverlays) {
        maxExtent = this.baseLayer.maxExtent;
    }  else {
        maxExtent = this.maxExtent;
    } 
    return maxExtent;
}
