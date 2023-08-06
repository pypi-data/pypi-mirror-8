/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
 /*
  Class: OpenLayers.Control.Click
    Todo: rename class

  Inherits From:
   - {OpenLayers.Control}
*/ 
 OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {                
    
    /*
        const: i18n_please_wait
        {String} Popup title        
    */
    i18n_popup_title : 'Coordinates',
     
     defaultHandlerOptions: {
        'single': true,
        'double': false,
        'pixelTolerance': 0,
        'stopSingle': false,
        'stopDouble': false
    },

    displayProjectionString: null,

    displayProjection: null,

    initialize: function(options) {
        this.handlerOptions = OpenLayers.Util.extend(
            {}, this.defaultHandlerOptions
        );
        OpenLayers.Control.prototype.initialize.apply(
            this, arguments
        ); 
        this.handler = new OpenLayers.Handler.Click(
            this, {
                'click': this.onClick,
                'dblclick': this.onDblclick 
            }, this.handlerOptions
        );
        if (this.displayProjectionString) {
            this.displayProjection = new OpenLayers.Projection(
                this.displayProjectionString
            );
        }
    }, 

    onClick: function(evt) {
        var featurepoint;
        var lonlat = this.map.getLonLatFromViewPortPx(evt.xy);
        var mypoint=new OpenLayers.Geometry.Point(lonlat.lon, lonlat.lat);

        // create a vector layer, add a feature into it
    	var vectorLayer = new OpenLayers.Layer.Vector(
            "GetMousePosition",
            {displayInLayerSwitcher: false}
        );

    	vectorLayer.addFeatures(
            featurepoint=new OpenLayers.Feature.Vector(mypoint)
    	);

        this.map.addLayer(vectorLayer);

        // reproject message if necessary
        if (this.displayProjection) {
            lonlat = lonlat.transform(
                this.map.getProjectionObject(), this.displayProjection);
        }
        var msg=lonlat.lon + " E, " + lonlat.lat + " N";

        if (this.displayProjection) {
            msg += "<br />Projection : " + this.displayProjectionString;
        }

		
        // create select feature control
        // define "createPopup" function

        var popup;
        popup = new GeoExt.Popup({
            title: this.i18n_popup_title,
            location: featurepoint,
            width: 200,
            html: msg,
            collapsible: true,
            map: this.map
        });

        popup.on({
            close: function() {
                this.map.removeLayer(featurepoint.layer);
            }
        });

        popup.show();

		//Ext.Msg.alert('X Y coords', msg);
    }
});
