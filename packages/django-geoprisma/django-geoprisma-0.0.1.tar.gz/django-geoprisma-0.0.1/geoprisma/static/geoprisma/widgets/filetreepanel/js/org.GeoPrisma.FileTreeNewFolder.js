/**
 * Copyright (c) 2009-2011 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma");

/*
 * @requires org.GeoPrisma.FileTreePlugin.js
 */

/** api: (define)
 *  module = org.GeoPrisma
 *  class = FileTreeNewFolder
 */

/** api: constructor
 *  .. class:: FileTreeNewFolder
 */
org.GeoPrisma.FileTreeNewFolder = Ext.extend(org.GeoPrisma.FileTreePlugin, {

    /* i18n */

    /** api: property[actionText] ``String`` i18n */
    actionText: "New Folder",

    /** api: property[actionTooltipText] ``String`` i18n */
    actionTooltipText: "Create an new folder in current selected directory",

    /* API Properties */

    /** api: property[actionIconCls]
     * ``String``
     * The class name to use for the new folder action 'iconCls' property.
     */
    actionIconCls: "icon-folder-add",

    /* Methods */

    /** private: method[init]
     */
    init: function(fileTreePanel) {
        org.GeoPrisma.FileTreeNewFolder.superclass.init.call(
            this, fileTreePanel
        );

        // before creating a new folder, add the 'osmresource' parameter to the
        // newdirUrl
        this.fileTreePanel.on({
            "beforenewdir": function(sm, node) {
                var resource = this.getNodeOSMResource(node);
                this.fileTreePanel.newdirUrl = Ext.urlAppend(
                    this.fileTreePanel.url,
                    "osmresource=" + resource
                );
            },
            scope: this
        });

        // when a new folder is created, set its 'osmresource' parameter the
        // the same as its parent node
        this.fileTreePanel.on({
            "newdir": function(sm, node) {
                var resource = this.getNodeOSMResource(node.parentNode);
                this.setNodeOSMResource(node, resource);
            },
            scope: this
        });
    },

    /** private: method[actionHandler]
     *  The handler called by this plugin action.  Create a new directory in
     *  currently selected branch node.
     */
    actionHandler: function() {
        var node = this.getSelectedBranchNode();
        node && this.fileTreePanel.createNewDir(node);
    }
});
