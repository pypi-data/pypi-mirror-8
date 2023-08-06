/*
   Copyright (c) 2011- Mapgears Inc., published under the BSD license.
   See http://geoprisma.org/license for the full text of the license.
*/
/**
 * @requires OpenLayers/Result
 *
 * Class: OpenLayers.ResultVectorLayer
 * 
 * Inherits from:
 *  - <OpenLayers.Result>
 */
OpenLayers.ResultVectorLayer = OpenLayers.Class({

    /* begin i18n */

    /** api: config[layerNameText] ``String`` i18n */
    layerNameText: "Vector result",

    /* end i18n */

    /**
     * Property: APIProperty: drawMode
     * {string}
     */
    drawMode: null,

    query: null,

    resources: null,

    /**
     * APIProperty: layer
     * {<OpenLayers.Layer.Vector>} The layer in which to display the results
     */
    layer: null,

    /**
     * APIProperty: map
     * {<OpenLayers.Map>} A reference to the map object.
     */
    map: null,

    /**
     * APIProperty: singleMode
     * {Boolean} Defaults to false.  Whether this widget should set the
     *     'singleResource' property upon 'multiple' queries or not.
     */
    singleMode: false,

    /**
     * Property: singleResource
     * {String} If 'singleMode' is set to true, when a query was made in
     *     'multiple' mode, features of this resource only are added to the
     *     layer.  Automatically set when 'singleMode' is set to true.
     */
    singleResource: null,
    
    /**
     * Constructor: OpenLayers.ResultVectorLayer
     * Create a new ResultVectorLayer instance
     *
     * Parameters:
     * options - {Object} An optional object whose properties will be set on
     *     this instance.
     */
    initialize: function(options) {
        OpenLayers.Util.extend(this, options);
        if ((this.layer instanceof OpenLayers.Layer.Vector) === false) {
            this.layer = new OpenLayers.Layer.Vector(this.layerNameText);
            this.map.addLayer(this.layer);
            // move vector layer to top after "printallwidgetexecutions"
            this.map.events.on({
                "printallwidgetexecutions": function(event) {
                    this.map.setLayerIndex(this.layer, this.map.layers.length)
                }, scope: this
            });
        }
        // Before adding a feature, make sure it's valid.  When adding a
        // feature, set the 'singleResource' property.
        this.layer.events.on({"beforefeatureadded": function(e) {
            return this.isValidFeature(e.feature);
        }, "featureadded": function(e) {
            e.feature.resource && this.setSingleResource(e.feature.resource);
        }, scope: this});
    },

    setQuery: function(query){
        this.query = query;
    },

    getResourceByLayer: function(szLayer, szServiceType){
        var szResourceName = 
            this.query.getResourceNameByLayer(szLayer, szServiceType);

        if(!szResourceName){
            return null;
        }

        for(var i=0; i<this.resources.length; i++)
        { 
            var oResource = this.resources[i];
            if(oResource.resource == szResourceName){
                return oResource;
            }
        } 

        return null;  
    },
    
    /**
     * Method: resetPanel
     * Called by the query as soon as the user clicks the map.  Remove all
     *     features binded to a resource (coming from a query widget) from the
     *     layer, thus keeping those coming from other widgets such as the
     *     redlining.
     * 
     * Also, reset the 'singleResource' property if query is not in 'multiple'
     *     mode.
     *
     * options     - {<Object>} Hash of options.  Possible keys are :
     *               - modifiers : the query modifiers
     */
    resetPanel: function(options) {
        options = options || {};
        // remove only the features having a resource property set
        var features = [];
        for (var i=0, iLen=this.layer.features.length; i<iLen; i++) {
            this.layer.features[i].resource &&
                features.push(this.layer.features[i]);
        }
        this.layer.removeFeatures(features);
        this.singleMode === true && options.modifiers &&
            options.modifiers.multiple === false && this.resetSingleResource();
    },

    /**
     * Method: showReult
     * Called by the query as soon as all responses were parses to features.
     * Add all valid features to the vector layer.
     *
     * Parameters:
     * features    - {Array of <OpenLayers.Feature.Vector>} 
     * htmlResults - {Array of <Object>} Objects returned by queries using
     *                                   'info_format' equal to 'text/html'.
     *                                   Not supported by this wiget.
     */
    showResult: function(features, htmlResults) {
        this.layer.addFeatures(features);
        if (this.layer.features.length) {
            // make sure the result layer is on top of all other layers
            this.map.setLayerIndex(this.layer, this.map.layers.length);
        }
    },

    /**
     * Method: isValidFeature
     * A feature is valid if :
     *   - it has geometry
     *   - if it's binded to a resource, it must be binded to this widet
     *     resources as well
     *   - if it's binded to a resource, if 'singleResource' is set, then the
     *     feature's resource must be equal to the 'singleResource'
     * 
     * Parameters:
     * feature    - {<OpenLayers.Feature.Vector>}
     * 
     * Returns:
     * {Boolean} Whether the feature is valid or not.
     */
    isValidFeature: function(feature) {
        // validate geometry
        var isValid = feature.geometry instanceof OpenLayers.Geometry;
        // validate feature resource
        if (isValid && feature.resource) {
            isValid = OpenLayers.Util.indexOf(
                this.resources, feature.resource) != -1;
        }
        // validate 'singleResource' if set
        if (isValid && feature.resource && this.singleResource !== null) {
            isValid = this.singleResource === feature.resource;
        }
        return isValid;
    },

    /**
     * Method: setSingleResource
     * Sets the 'singleResource' property if in 'singleMode' and if
     *     'singleResource' is not already set.  Also sets the query
     *     'multiQueryResource' property.
     *
     * Parameters:
     * resource - {Stirng} The name of the resource.
     */
    setSingleResource: function(resource) {
        if (this.singleMode === true && this.singleResource === null) {
            this.singleResource = resource;
            this.query.multiQueryResource = resource;
        }
    },

    /**
     * Method: resetSingleResource
     * Resets the 'singleResource' property to null. Also reset the query
     *     'multiQueryResource' property.
     *
     * Parameters:
     * resource - {Stirng} The name of the resource.
     */
    resetSingleResource: function() {
        this.singleResource = null;
        this.query.multiQueryResource = null;
    },
    
    CLASS_NAME: "OpenLayers.ResultVectorLayer"
});
