/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.ApplyFilter");

/** api: (define)
 *  module = org.GeoPrisma.ApplyFilter
 *  class = TabPanelContainer
 */

/** api: constructor
 *  .. class:: TabPanelContainer
 */
org.GeoPrisma.ApplyFilter.TabPanelContainer = Ext.extend(Ext.TabPanel, {

    // i18n

    /** api: property[title] ``String`` i18n */
    title: "Filter result",

    // API Properties, default values
    
    /** api: property[autoScroll]
     *  ``Boolean``
     *  Default value for this parameter.
     */
    autoScroll: true,

    /** api: property[border]
     *  ``Boolean``
     *  Default value for this parameter.
     */
    border: false,

    /** api: property[enableTabScroll]
     *  ``Boolean``
     *  Default value for this parameter.
     */
    enableTabScroll: true,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
        this.on("tabchange", this.onTabChange, this);
    },

    /** private: method[onTabChange]
     *  :param tabPanel: ``org.GeoPrisma.ApplyFilter.TabPanel``
     *  :param activeTab: ``org.GeoPrisma.ApplyFilter.WFSFeatureGrid``
     *
     *  Callback method of the "tabchange" event.  Used to toggle the visibility
     *  of vector layers. Only the active panel (active tab) has its vector
     *  layer visible.
     *  
     *  Also called after all filter requests were completed.
     */
    onTabChange: function(tabPanel, activeTab) {
        activeTab = activeTab || this.activeTab;
        this.items.each(function(panel) {
            panel.layer && panel.layer.setVisibility(activeTab == panel);
        }, this);
    }
});
