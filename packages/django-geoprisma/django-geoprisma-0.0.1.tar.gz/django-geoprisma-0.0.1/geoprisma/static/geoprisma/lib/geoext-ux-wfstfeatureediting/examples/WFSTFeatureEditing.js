var manager, mapPanel, tree, toolbar, url;

Ext.onReady(function() {
    Ext.QuickTips.init();

    msURL = "http://dev8.mapgears.com/cgi-bin/mswms_gmap_trunk";
    tinyURL = "http://dev8.mapgears.com/cgi-bin/tinyows-trunk";

    // == Map ==
    var options = {
        allOverlays: true,
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        units: "m",
        numZoomLevels: 18,
        maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(-20037508, -20037508,
                                         20037508, 20037508.34)
    };
    map = new OpenLayers.Map('map', options);

    // == Toolbar and Actions ==
    var actions = [];

    // ZoomToMaxExtent control, a "button" control
    action = new GeoExt.Action({
        control: new OpenLayers.Control.ZoomToMaxExtent(),
        map: map,
        text: "max extent",
        tooltip: "zoom to max extent"
    });
    actions.push(action);
    actions.push("-");

    // Navigation control and DrawFeature controls
    // in the same toggle group
    action = new GeoExt.Action({
        text: "nav",
        control: new OpenLayers.Control.Navigation(),
        map: map,
        // button options
        toggleGroup: "myGroup",
        allowDepress: false,
        pressed: true,
        tooltip: "navigate",
        // check item options
        group: "myGroup",
        checked: true
    });
    actions.push(action);
    toolbar = new Ext.Toolbar(actions);

    // == MapPanel ==
    wmsOptions = {isBaseLayer: false, singleTile: true, visibility: false};
    mapPanel = new GeoExt.MapPanel({
        region: "center",
        layers: [
            //new OpenLayers.Layer.OSM(),
            new OpenLayers.Layer.WMS('Bathymetry', msURL, {
                transparent: true, layers: 'bathymetry'},
                Ext.applyIf({visibility: true}, wmsOptions)),
            new OpenLayers.Layer.WMS('Drainage', msURL, {
                transparent: true, layers: 'drainage'}, wmsOptions),
            new OpenLayers.Layer.WMS('Roads', msURL, {
                transparent: true, layers: 'road'}, wmsOptions),
            new OpenLayers.Layer.WMS('Cities', msURL, {
                transparent: true, layers: 'popplace'}, wmsOptions)
        ],
        map: map,
        tbar: toolbar
    });

    tree = new Ext.tree.TreePanel({
        region: 'east',
        root: new GeoExt.tree.LayerContainer({
            text: 'Map Layers',
            layerStore: mapPanel.layers,
            leaf: false,
            expanded: true
        }),
        enableDD: true,
        width: 170
    });

    new Ext.Panel({
        renderTo: "content",
        layout: "border",
        width: 570,
        height: 350,
        items: [mapPanel, tree]
    });

    map.setCenter(new OpenLayers.LonLat(-8005708,6182838), 7);

    // WFSTFeatureEditingManager
    var extWindow = new Ext.Window({
        resizable: true,
        modal: false,
        closable: false,
        closeAction: 'hide',
        width: 550,
        height: 450,
        title: "WFSTFeatureEditing",
        layout: 'fit',
        items: []
    });

    manager = new GeoExt.ux.WFSTFeatureEditingManager({
        "map": mapPanel.map,
        "toolbar": toolbar,
        "url": tinyURL,
        "actionGroup": "myGroup",
        "mainPanelContainer": extWindow,
        "ignoredAttributes": {name:[
            "the_geom", "id", "gid", "fid", "name_e", "name_f"
        ]}
    });
});
