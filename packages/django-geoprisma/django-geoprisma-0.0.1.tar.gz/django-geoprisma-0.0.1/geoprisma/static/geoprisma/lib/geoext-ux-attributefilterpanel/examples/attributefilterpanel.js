/**
 * Copyright (c) 2008-2010 The Open Source Geospatial Foundation
 * 
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

 /** api: example[attribute filter panel]
  *  Attribute Filter Panel
  *  ----------------------
  *  ...
  */

var map, mapPanel;

Ext.onReady(function() {

	var layers = [];

	// base WMS layer
	layers.push(new OpenLayers.Layer.WMS("OpenLayers WMS",
		"http://tilecache.osgeo.org/wms-c/Basic.py",
		{layers: "basic"} 
    ));
	
	/*
	var vecLayer = new OpenLayers.Layer.GML(
		"geobidule",
		"geobidule.json",
		{ format: OpenLayers.Format.GeoJSON }
	);
	*/

	var filterStrategy = new OpenLayers.Strategy.Filter();
	
	var vecLayer = (
		new OpenLayers.Layer.Vector(
			"geobidule",
			{
				strategies: [
					new OpenLayers.Strategy.Fixed(),
					filterStrategy
				],
				protocol: new OpenLayers.Protocol.HTTP({
					url: "geobidule.json",
					format: new OpenLayers.Format.GeoJSON()
				}),
				filter: null
			}
		)
	);

	layers.push(vecLayer);
	
	// HACK: since setting the layer's filter has no effect when
	// using a simple GeoJSON file (no server-side filtering is done),
	// we use an OpenLayers.Strategy.Filter to filter the features
	// client-side; this event handler ensures that the strategy's filter
	// is updated when the layer's filter is.
	vecLayer.events.register("refresh", null, function() {
		filterStrategy.setFilter(vecLayer.filter);
	});

    map = new OpenLayers.Map({
        projection: new OpenLayers.Projection("EPSG:4326")
    });

    mapPanel = new GeoExt.MapPanel({
        region: "center",
        center: [-72.172623, 45.280564],
        zoom: 8,
        map: map
    });

    map.addLayers(layers);

	var filterPanel = new GeoExt.ux.form.AttributeFilterPanel({
		layer: vecLayer,
		title: "Attribute Filter Panel",
		labelAlign: 'top',
		items: [
			{
				xtype: "textfield",
				name: "name__like",
				fieldLabel: "Name is like"
			},
			{
				xtype: "textfield",
				name: "color__eq",
				fieldLabel: "Color equals"
			},
			{
				xtype: "textfield",
				name: "price__gt",
				fieldLabel: "Price is greater than"
			},
			{
				xtype: "textfield",
				name: "name__le",
				fieldLabel: "Size is less than or equal"
			},
			{
				xtype: "datefield",
				name: "construction_date__ge",
				fieldLabel: "Construction_date is greater than or equal",
				format: "Y-m-d"
			}
		],
		region: "east",
		width: 300
	});
	
	filterPanel.addButton({
		// TODO: make buttons' text configurable (i18n)
		text: "Filter",
		handler: function() {
			// trigger filter request, the options passed to doAction
			// are passed to the protocol's read method, so one
			// can register a read callback here
			var o = {
				callback: function(response) {
				},
				logicalOp: "&&",
				ignoreEmptyFields: true
			};
			this.filter(o);
		},
		scope: filterPanel
	});
	filterPanel.addButton({
		// TODO: make buttons' text configurable (i18n)
		text: "Reset",
		handler: function() {
			var o = {
				callback: function(response) {
				},
				formPanel: filterPanel
			};
			this.reset(o);
		},
		scope: filterPanel
	});
	
	
	// bind the layer to a FeatureStore so its feature attributes
	// can be displayed in a grid panel
	/*
	// FIXME: store is not synchronized with the layer features... why?
	var vecStore = new GeoExt.data.FeatureStore({
		layer: vecLayer,
		fields: [
			{name: 'name', type: 'string'},
			{name: 'color', type: 'string'},
			{name: 'size', type: 'string'},
			{name: 'price', type: 'string'},
			{name: 'construction_date', type: Ext.data.Types.DATE, dateFormat: 'Y-m-d'}
		]
	});
	
	var gridPanel = new Ext.grid.GridPanel({
		title: "Feature Grid",
		region: "south",
		store: vecStore,
		height: 150,
		columns: [{
			header: "name",
			width: 200,
			dataIndex: "name"
		}, {
			header: "color",
			width: 100,
			dataIndex: "color"
		}, {
			header: "size",
			width: 100,
			dataIndex: "size"
		}, {
			header: "price",
			width: 100,
			dataIndex: "price"
		}, {
			header: "construction_date",
			width: 200,
			dataIndex: "construction_date"
		}],
		sm: new GeoExt.grid.FeatureSelectionModel() 
	});
	*/
	
    new Ext.Viewport({
        layout: "fit",
        hideBorders: true,
        items: {
            layout: "border",
            items: [
                mapPanel, filterPanel, /* gridPanel, */ {
                    contentEl: "desc",
                    region: "west",
                    width: 250,
                    bodyStyle: {padding: "5px"}
                }
            ]
        }
    });

    //map.setCenter(new OpenLayers.LonLat(-7924121.1710935, 6185868.5449234), 6);
});
