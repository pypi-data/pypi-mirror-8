/**
 * Copyright (c) 2008-2009 The Open Source Geospatial Foundation
 *
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

/** api: example[ShortcutCombo]
 *  Shortcut Combo
 *  ---------------------
 *  Combo to present shortcuts to the user
 */

var mapPanel;

Ext.onReady(function() {
    var map = new OpenLayers.Map();
    var layer = new OpenLayers.Layer.OSM("OSM");
    map.addLayer(layer);

    var shortcutCombo = new GeoExt.ux.ShortcutCombo({
        map: map,
        store: GeoExt.ux.ShortcutCombo.countryStore,
        bboxField: 'bbox',
        bboxSrs: 'EPSG:900913'
    });

    new GeoExt.ux.ShortcutCombo({
        map: map,
        renderTo: 'shortcutcombo',
        store: GeoExt.ux.ShortcutCombo.countryStore,
        bboxField: 'bbox',
        bboxSrs: 'EPSG:900913'
    });

    mapPanel = new GeoExt.MapPanel({
        title: "GeoExt MapPanel with Shortcut Combo",
        renderTo: "mappanel",
        height: 400,
        width: 600,
        map: map,
        tbar: [shortcutCombo]
    });
});
