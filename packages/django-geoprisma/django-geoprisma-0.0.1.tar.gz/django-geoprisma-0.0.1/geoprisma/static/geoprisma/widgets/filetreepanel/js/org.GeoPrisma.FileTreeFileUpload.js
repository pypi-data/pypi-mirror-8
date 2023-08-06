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
 *  class = FileTreeFileUpload
 */

/** api: constructor
 *  .. class:: FileTreeFileUpload
 */
org.GeoPrisma.FileTreeFileUpload = Ext.extend(org.GeoPrisma.FileTreePlugin, {

    /* Constants */

    /** private: property[UPLOAD_PANEL_WINDOW_DEFAULT_OPTIONS]
     *  ``Object``
     *  The default options to use for the upload panel window.
     */
    UPLOAD_WINDOW_DEFAULT_OPTIONS: {
        width: 500,
        layout: "fit",
        closeAction: "hide",
        iconCls: 'icon-upload'
    },

    /* i18n */

    /** api: property[actionText] ``String`` i18n */
    actionText: "Upload",

    /** api: property[actionTooltipText] ``String`` i18n */
    actionTooltipText: "Upload new files in selected directory",

    /** api: property[windowTitleText] ``String`` i18n */
    windowTitleText: "Upload",

    /* API Properties */

    /** api: property[actionIconCls]
     * ``String``
     * The class name to use for the upload action 'iconCls' property.
     */
    actionIconCls: "icon-upload",

    /* API Properties  */

    /** api: property[uploadPanelOptions]
     * ``Object``
     * Additional hash of options used when creating the upload panel. 
     */
    uploadFormOptions: null,

    /** api: property[uploadPanelWindowOptions]
     * ``Object``
     * Additional hash of options used when creating the upload panel window. 
     */
    uploadWindowOptions: null,

    /* Private Properties */

    /** private: property[uploadForm]
     *  ``Ext.form.FormPanel``
     *  The UploadForm created by this plugin.
     */
    uploadForm: null,

    /** private: property[uploadWindow]
     *  ``Ext.Window``
     *  The Window containing the UploadForm created by this plugin.
     */
    uploadWindow: null,

    /* Methods */

    /** private: method[init]
     */
    init: function(fileTreePanel) {
        org.GeoPrisma.FileTreeFileUpload.superclass.init.call(
            this, fileTreePanel
        );
        // when the treePanel selection changes, set current path accordingly
        this.fileTreePanel.getSelectionModel().on({
            selectionchange: function(sm, node) {
                node && this.setPath(this.getPath(node));
                node && this.setResource(this.getNodeOSMResource(node));
            },
            scope: this
        });
    },

    /** private: method[actionHandler]
     *  The handler called by this plugin action.  Create the upload form and
     *  its window if they are not yet created, else simply show the window.
     */
    actionHandler: function() {
        if (!this.uploadWindow) {
            this.uploadForm = new org.GeoPrisma.form.FileUploadFormPanel({
                url: this.fileTreePanel.url,
                listeners: {
                    "afterrender": this.onUploadFormAfterRender,
                    scope : this
                }
            });
            this.uploadForm.on(
                'commitsuccess', this.onUploadFormCommitSuccess, this);

            this.uploadWindow = new Ext.Window(Ext.applyIf(
                Ext.applyIf({
                    items: [this.uploadForm],
                    title: this.windowTitleText
                }, this.uploadWindowOptions),
            this.UPLOAD_WINDOW_DEFAULT_OPTIONS));
        }
        this.uploadWindow.show();
    },

    /** private: method[setPath]
     *  :param path: ``String``
     *  
     */
    setPath: function(path) {
        this.uploadForm && this.uploadForm.setPath(path);
    },

    setResource: function(resource) {
        this.uploadForm && this.uploadForm.setResource(resource);
    },

    onUploadFormAfterRender: function() {
        var node = this.fileTreePanel.getSelectionModel().getSelectedNode();
        node && this.setPath(this.getPath(node));
        node && this.setResource(this.getNodeOSMResource(node));
    },

    /** private: method[onUploadFormCommitSuccess]
     *  Triggered on form panel "commitsuccess" event triggered.  Reload the
     *  node to fetch the newly added elements.
     */
    onUploadFormCommitSuccess: function() {
        var node = this.getSelectedBranchNode();
        node && node.reload();
    }
});
