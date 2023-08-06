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
 *  class = FileTreeCascade
 */

/** api: constructor
 *  .. class:: FileTreeNewFolder
 */
org.GeoPrisma.FileTreeCascade = Ext.extend(org.GeoPrisma.FileTreePlugin, {

    /* Public Properties */

    /** api: property[separator]
     * ``String``
     * The separator to use when splitting the path string to get the directory
     * and file names.
     */
    separator: "/",

    /* Private Properties */

    /** private: property[path]
     *  ``Array``
     *  The split path
     */
    path: null,

    /** private: property[nextIndex]
     *  ``Integer``
     *  The index used when looking in the path
     */
    nextIndex: null,

    /** private: property[currentNode]
     *  ``Ext.tree.AsyncTreeNode``
     *  The current node in which we look for a child having the next path text
     */
    currentNode: null,

    /* Methods */

    /** private: method[init]
     */
    init: function(fileTreePanel) {
        org.GeoPrisma.FileTreeNewFolder.superclass.init.call(
            this, fileTreePanel
        );
        this.path = [];
        this.fileTreePanel.gpCascadePlugin = this;
    },

    /** public: method[cascadePath]
     *  :param path: ``String``
     *  Cascade the FileTreePanel using a path string.  It's first exploded into
     *  an array, then we look for each node one by one. 
     */
    cascadePath: function(path) {
        path = path || "";
        this.reset();
        this.path = path.split(this.separator);
        this.path.length && this.findNextNode();
    },

    /** private: method[initActionCreation]
     *  This plugin has no action
     */
    initActionCreation: function() {},

    /** private: method[initActionToolbarAddition]
     *  This plugin has no action
     */
    initActionToolbarAddition: function() {},

    /** private: method[initActionToggling]
     *  This plugin has no action
     */
    initActionToggling: function() {},

    /** private: method[reset]
     *  Resets the index and set the current node to the root node of the
     *  FileTreePanel.  Also collapses all rootNode child nodes.
     */
    reset: function() {
        this.nextIndex = 1;
        this.currentNode = this.fileTreePanel.getRootNode();
        this.collapseChildNodes(this.currentNode);
    },

    /** private: method[findNextNode]
     *  Browse the current node children.  Look for the one having the same
     *  text as the one we're currently searching (in the path array using the
     *  nextIndex property).
     *
     *  When the according child is found, set it as the new 'currentNode', then
     *  repeat the process by calling this same function.  If the node doesn't
     *  have child nodes yet, expand it first.
     */
    findNextNode: function() {
        var found = false;
        this.currentNode.eachChild(function(node) {
            if (node.text == this.path[this.nextIndex]) {
                found = true;
                this.currentNode = node;
                this.nextIndex++;
                return false;
            }
        }, this);

        if (found) {
            if (this.currentNode.childNodes.length) {
                this.expandNode(this.currentNode);
                this.findNextNode();
            } else if (this.currentNode.isLeaf()) {
                this.currentNode.ensureVisible();
            } else {
                this.currentNode.on("load", function() {
                    this.findNextNode();
                }, this);
                this.expandNode(this.currentNode);
            }
        } else {
            // the node wasn't found
        }
    },

    /** private: method[expandNode]
     *  :param node: ``Ext.tree.AsyncTreeNode``
     *  Expand the node without animation and make sure it's visible after.
     */
    expandNode: function(node) {
        node.expand(false, false, function(node) {
            node.ensureVisible();
        }, this);
    },

    /** private: method[collapseChildNodes]
     *  :param node: ``Ext.tree.AsyncTreeNode``
     *  Collapse child nodes and their child nodes as well of a specific node
     *  without the animation.
     */
    collapseChildNodes: function(node) {
        node.eachChild(function(childNode) {
            childNode.collapse(true, false);
        }, this);
    }
});
