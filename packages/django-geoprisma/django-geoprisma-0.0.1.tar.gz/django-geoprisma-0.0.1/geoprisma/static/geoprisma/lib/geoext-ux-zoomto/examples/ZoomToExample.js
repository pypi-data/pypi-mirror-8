var zoomTo, mapPanel, toolbar;

Ext.onReady(function() {

    Ext.QuickTips.init();

    var options = {
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        units: "m",
        numZoomLevels: 18,
        maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(-20037508, -20037508,
                                         20037508, 20037508.34)
    };
    map = new OpenLayers.Map('map', options);

    toolbar = new Ext.Toolbar();

    mapPanel = new GeoExt.MapPanel({
        region: "center",
        layers: [
            new OpenLayers.Layer.Google("Google Physical",{'sphericalMercator': true, type: G_PHYSICAL_MAP})
        ],
        map: map,
        tbar: toolbar
    });

    projStore = new Ext.data.SimpleStore({
        fields: ['projection'],
        data : [
            ['EPSG:4326'],
            ['EPSG:900913'],
            ['EPSG:42304']
        ]
    });

    /* ZoomTo widget */
    zoomTo = new GeoExt.ux.ZoomTo({
        'projectionStore': projStore,
        'defaultZoomLevel': 10,
        'map': map
    });
    toolbar.add(zoomTo);

    new Ext.Panel({
        renderTo: "content",
        layout: "border",
        width: 500,
        height: 350,
        items: [mapPanel]
    });

    map.setCenter(new OpenLayers.LonLat(-10762333.581055,5968203.1676758), 4);
});
