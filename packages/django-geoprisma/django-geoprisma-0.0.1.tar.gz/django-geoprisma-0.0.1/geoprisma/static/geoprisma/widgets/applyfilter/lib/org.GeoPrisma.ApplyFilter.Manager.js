/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.ApplyFilter");

/*
 * @requires gxp.data.WFSFeatureStore.js
 * @requires gxp.data.WFSProtocolProxy.js
 * @requires gxp.grid.FeatureGrid.js
 * @requires org.GeoPrisma.ApplyFilter.Resource.js
 * @requires org.GeoPrisma.ApplyFilter.SLDSetter.js
 * @requires org.GeoPrisma.ApplyFilter.TabPanelContainer.js
 * @requires org.GeoPrisma.ApplyFilter.WFSFeatureGrid.js
 */

/** api: (define)
 *  module = org.GeoPrisma.ApplyFilter
 *  class = Manager
 */

/** api: constructor
 *  .. class:: Manager
 */
org.GeoPrisma.ApplyFilter.Manager = Ext.extend(Ext.util.Observable, {

    // CONSTANTS

    DEFAULT_IGNORED_FIELDS: ["geom", "geometry", "the_geom"],

    // i18n

    /** api: property[progressBarText] ``String`` i18n */
    progressBarText: "completed",

    /** api: property[progressBoxTitleText] ``String`` i18n */
    progressBoxTitleText: "Please wait...",

    // public properties (Mandatory)

    /** api: property[mapPanel]
     *  :class:`GeoExt.MapPanel`
     *  A reference to the MapPanel object.
     */
    mapPanel: null,

    /** api: property[proxyURL]
     *  ``String``
     *  The url of the proxy.
     */
    proxyURL: null,

    // public properties (Optional)

    /** api: property[ignoredFields]
     *  ``Array``
     *  An array of fields to ignored, i.e. not to display in the grid.
     *  Defaults to DEFAULT_IGNORED_FIELDS.
     */
    ignoredFields: null,

    /** api: property[maxZoomScale]
     *  ``Float``
     *  The maximum scale allowed to zoom in to.
     */
    maxZoomScale: null,

    /** api: property[pageSize]
     *  ``Integer``
     *  The maximum number of features each WFS GetFeature request should
     *  return.  It also sets the pageSize property of PagingToolbar objects.
     */
    pageSize: 10,

    // private properties

    /** private: property[grandTotalLength]
     *  ``Integer``
     *  Counter that keeps track of the total number of features returned by
     *  all requests.
     */
    grandTotalLength: null,

    /** private: property[messagePanel]
     *  :class:``org.GeoPrisma.ApplyFilter.MessagePanel``
     *  A panel used to display warning and error messages.  Added to the tab
     *  panel.
     */
    messagePanel: null,

    /** private: property[progressBox]
     *  ``Ext.Window``
     *  Shown while querying.  Contains a ``Ext.ProgressBar`` object.
     */
    progressBox: null,

    /** private: property[progressBar]
     *  ``Ext.ProgressBar``
     *  Used to show the progress of the received queries.
     */
    progressBar: null,

    /** private: property[receivedRequests]
     *  ``Integer``
     *  Counter that keeps track of the number of requests received.
     */
    receivedRequests: null,

    /** private: property[resources]
     *  ``Object``
     *  A hash of :class:`org.GeoPrisma.ApplyFilter.Resource` objects where the
     *  key is equal to the resource name.
     */
    resources: null,

    /** private: property[resources]
     *  :class:`org.GeoPrisma.ApplyFilter.TabPanelContainer`
     *  The tab panel containing
     *  :class:`org.GeoPrisma.ApplyFilter.WFSFeatureGrid` panels.
     */
    tabPanel: null,

    /** private: property[totalRequests]
     *  ``Integer``
     *  Counter that keeps track of the number of requests sent.
     */
    totalRequests: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
        this.resources = {};
        if (this.ignoredField) {
            this.ignoredFields = [this.ignoredField];
            delete this.ignoredField;
        }
        this.ignoredFields = this.ignoredFields || this.DEFAULT_IGNORED_FIELDS;

        this.messagePanel = new org.GeoPrisma.ApplyFilter.MessagePanel();
        this.tabPanel = new org.GeoPrisma.ApplyFilter.TabPanelContainer({
            items: [this.messagePanel]
        });

        // listen to GeoPrisma "applyfilters" to apply the filters to the
        // according resources.
        GeoPrisma.on("applyfilters", this.onApplyFilters, this);
    },

    /** public: method[manageResource]
     *  :param resource: ``Object`` A hash object containing infos about
     *                              the resource
     *
     *  This method creates a :class:`org.GeoPrisma.ApplyFilter.Resource` object
     *  using the given hash.  Add it to the resource list and add its created
     *  grid to the tabPanel.
     */
    manageResource: function(resource) {
        Ext.applyIf(resource, {
            proxyURL: this.proxyURL,
            map: this.mapPanel.map,
            maxFeatures: this.pageSize,
            maxZoomScale: this.maxZoomScale,
            defaultIgnoredFields: this.ignoredFields
        });

        // create the resource object and append it to the resources hash
        var resourceObject = new org.GeoPrisma.ApplyFilter.Resource(resource);
        this.resources[resourceObject.getName()] = resourceObject;

        // add the resource grid to the tab panel
        this.tabPanel.add(resourceObject.grid);

        // listen to resource grid "filterset" event
        resourceObject.grid.on("filterset", this.onResourceFilterSet, {
            manager: this,
            resourceObject: resourceObject
        });
    },

    /** public: method[manageResource]
     *  :return: :class:`org.GeoPrisma.ApplyFilter.TabPanelContainer`
     *
     *  Returns the component that needs to be drawn by Ext.
     */
    getDrawComponent: function() {
        return this.tabPanel;
    },

    /** private: method[afterAllFilterSet]
     *  Called after all "filterset" callback received.
     * 
     *  - Show the tapPanel owner container if records were returned 
     *  - Close the progress box currently visible
     *  - Show message if no records, else hide messagePanel
     */
    afterAllFilterSet: function() {
        this.grandTotalLength && this.toggleOwnerCt(this.grandTotalLength);
        this.tabPanel.onTabChange();
        this.stopProgress();
        // show message panel if no results
        if (!this.grandTotalLength) {
            this.messagePanel.show();
            this.tabPanel.unhideTabStripItem(this.messagePanel);
            this.messagePanel.setNoResultMessage();
        }
    },

    /** private: method[onApplyFilters]
     *  :arg resourceFilters: ``Array``
     *    An array of hash objects containing the following key:value :
     *    - resource (String) the resource name to apply the filter
     *    - filter (OpenLayers.Filter): filter to apply
     *  
     *  Callback method of the event GeoPrisma singleton 'applyfilters' object.
     *  Delegate each filter received to the according resource.
     */
    onApplyFilters: function(resourceFilters) {
        var resource;
        this.reset();
        this.toggleOwnerCt(true);
        Ext.each(resourceFilters, function(rf) {
            resource = this.resources[rf.resource];
            if (resource) {
                this.totalRequests++;
                resource.grid.show();
                this.tabPanel.unhideTabStripItem(resource.grid);
                resource.setFilter(rf.filter);
            }
        }, this);
        this.startProgress();
    },

    /** private: method[onResourceFilterSet]
     *  :arg totalLength: ``Integer`` The number of hits the filter returned
     *                                for the resource.
     *  
     *  Scope (this) has two properties :
     *  - manager (org.GeoPrisma.ApplyFilter.Manager) : this manager
     *  - resourceObject (org.GeoPrisma.ApplyFilter.Resource) : the resource
     *
     *  This method checks of the filter applied to a resource returned
     *  records.  If it did, show the tab and its content, else hide them.
     *
     *  Also, upon receiving all these callbacks, call the "afterAllFilterSet"
     *  method.
     */
    onResourceFilterSet: function(totalLength) {
        var m = this.manager, r = this.resourceObject;
        if (totalLength) {
            m.grandTotalLength += totalLength;
        } else {
            r.grid.hide();
            m.tabPanel.hideTabStripItem(r.grid);
        }

        m.receivedRequests++;
        m.updateProgress();
        m.receivedRequests == m.totalRequests && m.afterAllFilterSet();
    },

    /** private: method[reset]
     *  Reset all private properties used for request purpose.  Also resets
     *  every resources applied filters.
     */
    reset: function() {
        // local properties
        this.totalRequests = 0;
        this.receivedRequests = 0;
        this.grandTotalLength = 0;

        // if ownerCt of tabPanel is a Ext.TabPanel, set tabPanel as active tab
        this.tabPanel.ownerCt instanceof Ext.TabPanel &&
            this.tabPanel.ownerCt.setActiveTab(this.tabPanel);

        // hide message panel
        this.messagePanel.hide();
        this.tabPanel.hideTabStripItem(this.messagePanel);

        // resources
        var resource;
        for (var resourceName in this.resources) {
            resource = this.resources[resourceName];
            resource.reset();
            resource.grid.hide();
            this.tabPanel.hideTabStripItem(resource.grid);
        }
    },

    /** private: method[toggleOwnerCt]
     *  :arg visibility: ``Boolean`` Whether to show the container or hide it.
     *  Toggles the visibility of the tapPanel owner container.
     */
    toggleOwnerCt: function(visibility) {
        // owner container toggling
        var ownerCt = this.tabPanel.ownerCt;

        if (!ownerCt) {
            return;
        }

        if (visibility) {
            ownerCt instanceof Ext.Window
                ? ownerCt.show() : ownerCt.expand(false);
        } else {
            ownerCt instanceof Ext.Window
                ? ownerCt.hide() : ownerCt.collapse(false);
        }
    },

    /** private: method[startProgress]
     *  Create a new message box containing a progress bar.
     */
    startProgress: function() {
        if (!this.totalRequests) {
            return;
        }
        this.progressBar = new Ext.ProgressBar({cls:'left-align'});
        this.progressBox = new Ext.Window({
            title: this.progressBoxTitleText,
            width: 200,
            modal: true,
            items: [this.progressBar]
        });
        this.progressBox.show();
        this.updateProgress();
    },

    /** private: method[updateProgress]
     *  Update the progress bar using currently received and total requests.
     */
    updateProgress: function() {
        if (!this.progressBar) {
            return;
        }
        var ratio = this.receivedRequests / this.totalRequests;
        var text = [];
        text.push(Math.round(ratio * 100));
        text.push("%");
        text.push(this.progressBarText);
        this.progressBar.updateProgress(ratio, text.join(" "));
    },

    /** private: method[stopProgress]
     *  Close the message box containing the progress bar.
     */
    stopProgress: function() {
        this.progressBox && this.progressBox.close();
        this.progressBox = null;
        this.progressBar = null;
    }
});
