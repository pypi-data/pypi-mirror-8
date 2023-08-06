/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license.
 *
 * The code of this widget was borrowed from the GXP library at the following
 * version, which was published under the BSD license at that time :
 * 
 * Commit : a56125b1ff578110bc39f4ac76312eab0fc46073
 * Author : Bart Van den Eijnden
 * Date : Wed Mar 23 17:11:55 2011 +0100
 */

Ext.namespace("org.GeoPrisma.ApplyFilter");

/** api: (define)
 *  module = org.GeoPrisma.ApplyFilter
 *  class = WFSFeatureGrid
 */

/** api: constructor
 *  .. class:: WFSFeatureGrid
 */
org.GeoPrisma.ApplyFilter.WFSFeatureGrid = Ext.extend(gxp.grid.FeatureGrid, {

   // i18n

    /** api: property[zoomButtonTooltipText] ``String`` i18n */
    zoomButtonTooltipText: "Zoom to feature extent",

    // Public Properties (Mandatory)

    /** api: property[pageSize]
     *  ``Integer``
     *  Sets the pageSize property of the PagingToolbar object.
     */
    pageSize: null,

    // Public Properties (Optional)

    /** api: property[maxZoomScale]
     *  ``Float``
     *  The maximum scale allowed to zoom in to.
     */
    maxZoomScale: null,

    // Public Properties (Default)

    /** api: property[border]
     *  ``Boolean``
     *  Default value for this parameter.
     */
    border: false,

    /** api: property[enableHdMenu]
     *  ``Boolean``
     *  Default value for this parameter (header menus disabled).
     */
    enableHdMenu: false,

    // Private Properties

    /** private: property[isNewFilter]
     *  ``Boolean``
     *  Flag used when to notice the setting of a new filter.  When a new
     *  filter is set, this property is set.  On request complete, the
     *  "filterset" event is fired and this property is unset.
     */
    isNewFilter: false,

    /** private: property[pagingToolbar]
     *  :class:``Ext.PagingToolbar``
     *  Paging toolbar used to navigate features through the grid
     */
    pagingToolbar: null,

    // Private Methods

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        this.createPagingToolbar();
        arguments.callee.superclass.constructor.call(this, config);

        this.addEvents(
            /** private: event[filterset]
             *  Fires after a new filter was set and the store received
             *  features.
             */
            "filterset"
        );

        this.store.on("beforeload", this.onStoreBeforeLoad, this);
        this.pagingToolbar = this.getBottomToolbar();
    },

    /** private: method[createPagingToolbar]
     *  Creates and applies a new PagingToolbar object to this grid as its
     *  bottom toolbar.
     */
    createPagingToolbar: function() {
        Ext.apply(this, {
            bbar: new Ext.PagingToolbar({
                xtype: 'paging',
                store: this.store,
                displayInfo: true,
                pageSize: this.pageSize,
                listeners: {
                    beforechange: function(This, params) {
                        this.store.proxy.protocol.options = Ext.apply(
                            this.store.proxy.protocol.options, {
                                startIndex: params.start+1,
                                maxFeatures : params.limit
                            }
                        );
                    }
                }
            })
        });
    },

    /** private: method[createColumnModel]
     *  :arg store: ``GeoExt.data.FeatureStore``
     *  :return: ``Ext.grid.ColumnModel``
     *  Clone with some manual overrides of the superconstructor
     *  createColumnModel method.  The overrides include column title and witdth
     *  detection from store fields.
     */
    createColumnModel: function(store) {
        function getRenderer(format) {
            return function(value) {
                //TODO When http://trac.osgeo.org/openlayers/ticket/3131
                // is resolved, change the 5 lines below to
                // return value.format(format);
                var date = value;
                if (typeof value == "string") {
                     date = Date.parseDate(value.replace(/Z$/, ""), "c");
                }
                return date ? date.format(format) : value;
            };
        }
        // override : 'title' and 'width' added
        var columns = [], name, type, xtype, format, renderer, title, width;

        // override : first added column is a "zoomToFeatureExtent" button
        columns.push({
            header: "",
            xtype: "actioncolumn",
            width: 32,
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                var id = Ext.id();
                (function(id, grid, rowIndex) {
                    new Ext.Button({
                        iconCls: 'org-geoprisma-applyfilter-wfsfeaturegrid-zoombutton',
                        tooltip: grid.zoomButtonTooltipText,
                        renderTo: id,
                        scope: {record: record, grid: this, rowIndex: rowIndex},
                        handler: function(button, event) {
                            this.grid.getSelectionModel().selectRow(
                                this.rowIndex);
                            GeoPrisma.zoomToFeatureExtent(
                                this.record.getFeature(),
                                this.grid.maxZoomScale
                            );
                        }
                    });
                }).defer(25, this, [id, this, rowIndex]);
                return '<div id="'+ id +'">';
            },
            scope: this
        });

        (this.schema || store.fields).each(function(f) {
            if (this.schema) {
                name = f.get("name");
                // override start
                title = f.get("title");
                width = f.get("width");
                // override end
                type = f.get("type").split(":").pop();
                format = null;
                switch (type) {
                    case "date":
                        format = this.dateFormat;
                    case "datetime":
                        format = format ? format : this.dateFormat + " " + this.timeFormat;
                        xtype = undefined;
                        renderer = getRenderer(format);
                        break;
                    case "boolean":
                        xtype = "booleancolumn";
                        break;
                    case "string":
                        xtype = "gridcolumn";
                        break;
                    default:
                        xtype = "numbercolumn";
                }
            } else {
                name = f.name;
                // override start
                title = f.title;
                width = f.width;
                // override end
            }
            if (this.ignoreFields.indexOf(name) === -1) {
                columns.push({
                    dataIndex: name,
                    // override start
                    header: title || name,
                    width: width ? width : undefined,
                    sortable: false,
                    // override end
                    xtype: xtype,
                    format: format,
                    renderer: xtype ? undefined : renderer
                });
            }
        }, this);
        return new Ext.grid.ColumnModel(columns);
    },

    /** private: method[onStoreBeforeLoad]
     *  Callback method of the store "beforeload" event.
     *
     *  First, it triggers a WFS GetFeature request with "resultType = hits"
     *  to set store "totalLength" property to the total number of features
     *  the query would return without paging.
     * 
     *  Then, the actual request is made using the current startIndex and the
     *  maxFeatures.
     */
    onStoreBeforeLoad: function() {
        // get total number of features matching the current filter and load
        // the store with the appended total
        this.store.proxy.protocol.read({
            filter: this.getFilter(),
            readOptions: {output: "object"},
            resultType: "hits",
            maxFeatures: null,
            startIndex: 1,
            callback: function(response) {
                this.store.un("beforeload", this.onStoreBeforeLoad, this);
                this.store.load({
                    callback: function (records, options, success) {
                        if (success) {
                            this.store.totalLength = options.numberOfFeatures;
                            this.pagingToolbar.onLoad(this.store, records, {
                                params : {
                                    start: this.getStartIndex() - 1,
                                    limit: this.getMaxFeatures()
                                }
                            });
                            this.isNewFilter && this.fireEvent(
                                "filterset", this.store.totalLength);
                        }
                        this.isNewFilter = false;
                        this.store.on(
                            "beforeload",
                            this.onStoreBeforeLoad,
                            this
                        );
                    },
                    scope: this,
                    numberOfFeatures: response.numberOfFeatures,
                    store: this.store
                });
            },
            scope: this
        });
        return false;
    },

    /** private: method[resetStartIndex]
     *  Resets the startIndex option in the protocol to 1.
     */
    resetStartIndex: function() {
        this.store.proxy.protocol.options.startIndex = 1;
    },

    // API Methods

    /** api: method[getFilter]
     *  :return: ``OpenLayers.Filter``
     *  Returns current filter set in the protocol.
     */
    getFilter: function() {
        return this.store.proxy.protocol.filter;
    },

    /** api: method[setFilter]
     *  :param filter: ``OpenLayers.Filter``
     *  Sets the store filter.
     */
    setFilter: function(filter) {
        this.store.setOgcFilter(filter);
    },

    /** api: method[resetFilter]
     *  Sets the store filter as null, thus reseting it.
     */
    resetFilter: function() {
        this.setFilter(null);
    },

    /** api: method[getMaxFeatures]
     *  :return: ``Integer``
     *  Returns current maxFeatures option set in the protocol
     */
    getMaxFeatures: function() {
        return this.store.proxy.protocol.options.maxFeatures;
    },  

    /** api: method[getStartIndex]
     *  :return: ``Integer``
     *  Returns current startIndex option set in the protocol
     */
    getStartIndex: function() {
        return this.store.proxy.protocol.options.startIndex;
    },

    /** api: method[triggerFilterRequest]
     *  :arg filter: ``OpenLayers.Filter`` New filter to use
     *  
     *  This method sets a new filter to use for the request, resets the
     *  startIndex back to 1 and finally load the store.
     */
    triggerFilterRequest: function(filter) {
        this.isNewFilter = true;
        this.setFilter(filter);
        this.resetStartIndex();
        this.store.load();
    }
});
