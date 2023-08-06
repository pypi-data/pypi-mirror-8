/**
 * Copyright (c) 2009-2011 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.form");

/*
 * @requires Ext.ux.form.FileUploadField.js
 */

/** api: (define)
 *  module = org.GeoPrisma
 *  class = FileTreeFileUpload
 */

/** api: constructor
 *  .. class:: FileTreeFileUpload
 */

org.GeoPrisma.form.FileUploadFormPanel = Ext.extend(Ext.FormPanel, {

    /* Constants */

    /** private: property[CUSTOM_EVENTS]
     *  ``Array(String)`` Array of custom events used by this widget
     */
    CUSTOM_EVENTS: [
        "commitsuccess",
        "commitfail"
    ],

    /* i18n  */

    /** api: property[selectFileText] ``String`` i18n */
    selectFileText: "Select a file",

    /** api: property[fileText] ``String`` i18n */
    fileText: "File",

    /** api: property[uploadText] ``String`` i18n */
    uploadText: "Upload",

    /** api: property[resetText] ``String`` i18n */
    resetText: "Reset",

    /** api: property[uploadingText] ``String`` i18n */
    uploadingText: "Uploading your file",

    /** api: property[commitSuccessText] ``String`` i18n */
    commitSuccessText: "Success",

    /** api: property[commitSuccessMessageText] ``String`` i18n */
    commitSuccessMessageText: "Upload successfully completed",

    /** api: property[commitFailText] ``String`` i18n */
    commitFailText: "Failure",

    /** api: property[commitFailMessageText] ``String`` i18n */
    commitFailMessageText: "An error occured.  Server replied : ",

    /** api: property[unknownFailMessageText] ``String`` i18n */
    unknownFailMessageText: "An unknown error occured.",

    /** api: property[pleaseWaitText] ``String`` i18n */
    pleaseWaitText: "Please wait...",

    /* API Properties (mandatory) */

    /** api: property[url]
     *  ``String`` The url used to commit
     */
    url: null,

    /* API Properties (optional) */

    /** api: property[showSuccess]
     *  ``Boolean`` Whether to show a popup when a file was successfully
     *              uploaded or not
     */
    showSuccess: false,

    /** api: property[fileUpload]
     *  ``Boolean`` 
     */
    fileUpload: true,

    /** api: property[frame]
     *  ``Boolean`` Default frame value for this widget.
     */
    frame: true,

    /** api: property[autoHeight]
     *  ``Boolean`` Default autoHeight value for this widget.
     */
    autoHeight: true,

    /** api: property[bodyStyle]
     *  ``Boolean`` Default bodyStyle value for this widget.
     */
    bodyStyle: 'padding: 10px 10px 0 10px;',

    /** api: property[labelWidth]
     *  ``Boolean`` Default labelWidth value for this widget.
     */
    labelWidth: 50,

    /** api: property[defaults]
     *  ``Boolean`` Default defaults value for this widget.
     */
    defaults: {
        anchor: '95%',
        allowBlank: false,
        msgTarget: 'side'
    },

    /** api: property[border]
     *  ``Boolean`` Default border value for this widget.
     */
    border: false,


    /* Private properties*/

    /** private: property[path]
     *  ``String``
     *  The path in which to upload the file.
     */
    path: null,

    /** private: property[resource]
     *  ``String``
     *  The resource parameter to use when uploading a file.
     */
    resource: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        this.initMyItems();
        this.initMyButtons();
        arguments.callee.superclass.constructor.call(this, config);
        this.addEvents(this.CUSTOM_EVENTS);
    },

    /** private: method[initMyItems]
     *  Create and add the items of this widget : a Ext.ux.form.FileUploadField.
     */
    initMyItems: function() {
        Ext.apply(this, {items: [{
            xtype: 'fileuploadfield',
            id: 'form-file',
            emptyText: this.selectFileText,
            fieldLabel: this.fileText,
            name: 'x-filename',
            buttonText: '',
            buttonCfg: {
                iconCls: 'icon-upload'
            }
        }]});
    },

    /** private: method[initMyButtons]
     *  Create and add the buttons of this widget : an "upload" button that
     *  that takes care of the commits and errors, and a "reset" button to
     *  reset the form.
     */
    initMyButtons: function() {
        Ext.apply(this, {buttons: [{
            text: this.uploadText,
            handler: function(){
                if(this.getForm().isValid()){
                    this.getForm().submit({
                        url: this.url,
                        waitMsg: this.uploadingText,
                        params: {
                            "cmd": "upload",
                            "path": this.path,
                            "osmresource": this.resource,
                            "dir": "."
                        },
                        success: function(fp, o) {
                            var decodedResponse = Ext.util.JSON.decode(
                                o.response.responseText
                            );
                            if (decodedResponse.success === false) {
                                this.onFailure(this, o);
                            } else if (decodedResponse.success === true) {
                                this.showSuccess && Ext.MessageBox.show({
                                    title: this.commitSuccessText,
                                    msg: this.commitSuccessMessageText,
                                    buttons: Ext.MessageBox.OK,
                                    icon: Ext.MessageBox.INFO
                                });
                                this.events && this.fireEvent("commitsuccess");
                                this.getForm().reset();
                                this.ownerCt.hide();
                            }
                        },
                        failure: this.onFailure,
                        scope: this
                    });
                }
            },
            scope: this
        },{
            text: this.resetText,
            handler: function() {
                this.getForm().reset();
            },
            scope: this
        }]});
    },

    /** private: method[onFailure]
     *  :param fp: ``Ext.form.FormPanel`` This widget
     *  :param o: ``Object`` The response object returned by the server.
     *
     *  Look for an error message in the response and show it, else show the
     *  generic "unknown" error message.
     */
    onFailure: function(fp, o) {
        this.el.unmask();
        var decodedResponse = Ext.util.JSON.decode(
            o.response.responseText
        );
        var message = (decodedResponse.success === false)
            ? this.commitFailMessageText + decodedResponse.errors.message
            : this.unknownFailMessageText;
        this.displayErrorMessage(message);
        this.events && this.fireEvent("commitfail");
    },

    /** private: method[displayErrorMessage]
     *  :param message: ``String`` The error message to display
     *  Show an error message popup.
     */
    displayErrorMessage: function(message) {
        Ext.MessageBox.show({
            title: this.commitFailText,
            msg: message,
            buttons: Ext.MessageBox.OK,
            icon: Ext.MessageBox.ERROR
        });
    },

    /** private: method[setPath]
     *  :param path: ``String`` A path string
     *  Sets the path parameter value if path is set, else reset it.
     */
    setPath: function(path) {
        if (path) {
            this.path = path;
        } else {
            this.path = null;
        }
    },

    /** private: method[setResource]
     *  :param resource: ``String`` A resource name
     *  Sets the resource parameter value if resource is set, else reset.
     */
    setResource: function(resource) {
        if (resource) {
            this.resource = resource;
        } else {
            this.resource = null;
        }
    }
});
