/**
 * Copyright (c) 2009-2011 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma");

/*
 * @requires Ext.ux.FileTreePanel.js
 */

/** api: (define)
 *  module = org.GeoPrisma
 *  class = FileTreePlugin
 */

/** api: constructor
 *  .. class:: FileTreePlugin
 */
org.GeoPrisma.FileTreePlugin = Ext.extend(Ext.util.Observable, {

    /* i18n */

    /** api: property[actionText] ``String`` i18n */
    actionText: null,

    /** api: property[actionTooltipText] ``String`` i18n */
    actionTooltipText: null,

    /* API Properties */

    /** api: property[actionIconCls]
     * ``String``
     * The class name to use for the action 'iconCls' property.
     */
    actionIconCls: null,

    /* Private Properties */

    /** private: property[action]
     *  ``Ext.Action``
     *  The action created by this plugin.
     */
    action: null,

    /** private: property[fileTreePanel]
     *  ``Ext.ux.FileTreePanel``
     *  The FileTreePanel widget to link this plugin to.
     */
    fileTreePanel: null,

    /** private: method[constructor]
     *  This class is a superconstructor only.
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
    },

    /** private: method[init]
     *  Call all action initialization methods.
     */
    init: function(fileTreePanel) {
        this.fileTreePanel = fileTreePanel;
        this.initActionCreation();
        this.initActionToolbarAddition();
        this.initActionToggling();
    },

    /** private: method[actionHandler]
     *  The handler called by this plugin action.
     */
    actionHandler: function() {},

    /** private: method[initActionCreation]
     *  Creates the plugin action using set properties.
     */
    initActionCreation: function() {
        this.action = new Ext.Action({
            text: this.actionText,
            tooltip: this.actionTooltipText,
            iconCls: this.actionIconCls,
            disabled: true,
            handler: this.actionHandler,
            scope: this
        });
    },

    /** private: method[initActionToolbarAddition]
     *  Add the plugin action to the FileTreePanel existing top toolbar.
     */
    initActionToolbarAddition: function() {
        var tbar = this.fileTreePanel.getTopToolbar();
        if (tbar.rendered || !tbar.buttons) {
            tbar.add(this.action);
        } else {
            tbar.buttons.push(this.action);
        }
    },

    /** private: method[initActionToggling]
     *  Listen to the FileTreePanel selection model selection change to enable
     *  or disable the action button.
     */
    initActionToggling: function() {
        this.fileTreePanel.getSelectionModel().on({
            selectionchange: function(sm, node) {
                this.action.setDisabled(node ? false : true);
            },
            scope: this
        });
    },

    /** public: method[getPath]
     *  :param node: ``Ext.tree.AsyncTreeNode`` A tree node.
     *  :return: ``String`` The path of the node.
     *
     *  Returns the path of a node.
     */
    getPath: function(node) {
        var path;
        if (node) {
            path = this.fileTreePanel.getPath(node);
            if(node.isLeaf()) {
                path = path.replace(/\/[^\/]+$/, '', path);
            }
        }
        return path;
    },

    /** public: method[getCurrentNodeOSMResource]
     *  :return: ``String`` The resource name of the node.
     *
     *  Returns the resource name of the currently selected node.
     */
    getCurrentNodeOSMResource: function() {
        var resource, node;
        node = this.fileTreePanel.getSelectionModel().getSelectedNode();
        if (node) {
            resource = this.getNodeOSMResource(node);
        }
        return resource;
    },

    /** public: method[getNodeOSMResource]
     *  :param node: ``Ext.tree.AsyncTreeNode`` A tree node.
     *  :return: ``String`` The resource name of the node.
     *
     *  Returns the resource name of a node.
     */
    getNodeOSMResource: function(node) {
        var resource;
        if (node && node.attributes && node.attributes.osmresource) {
            resource = node.attributes.osmresource;
        }
        return resource;
    },

    /** public: method[getNodeOSMResource]
     *  :return: ``Ext.tree.AsyncTreeNode`` A tree node.
     *
     *  Returns currently selected branch node, which means if the node is a
     *  leaf, returns its parents else return itself.
     */
    getSelectedBranchNode: function() {
        var node = this.fileTreePanel.getSelectionModel().getSelectedNode();
        if (node) {
            node = (node.isLeaf()) ? node.parentNode : node
        }
        return node;
    },

    /** public: method[setNodeOSMResource]
     *  :param node: ``Ext.tree.AsyncTreeNode`` A tree node.
     *  :param resource: ``String`` A resource name
     *
     *  Set the resource name of a node.
     */
    setNodeOSMResource: function(node, resource) {
        if (node && node.attributes && node.attributes) {
            node.attributes.osmresource = resource;
        }
    }
});
