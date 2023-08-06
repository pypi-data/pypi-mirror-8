/**
 * Copyright (c) 2009-2011 Mapgears Inc.
 *
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license.
 */

Ext.namespace("org.GeoPrisma.EditFeature");

/** api: (define)
 *  module = org.GeoPrisma.EditFeature
 *  class = Confirm
 */

/** api: constructor
 *  .. class:: Confirm
 */

var lastEditFeaturePopup = null;

org.GeoPrisma.EditFeature.Confirm = Ext.extend(Ext.util.Observable, {

    /* i18n */

    /** api: property[popupTitleText] ``String`` i18n */
    popupTitleText: "Confirm",

    /** api: property[popupText] ``String`` i18n */
    popupText: "Confirm modifications ?",

    /** api: property[confirmButtonText] ``String`` i18n */
    confirmButtonText: "Commit",

    /** api: property[cancelButtonText] ``String`` i18n */
    cancelButtonText: "Cancel",

    /* API Properties (Mandatory) */

    /** api: property[editFeature]
     * ``OpenLayers.Control.EditFeature``
     * The editfeature control this confirm widget needs to be binded to.
     */
    editFeature: null,

    /* Private Properties */

    /** api: property[layer]
     * ``OpenLayers.Layer.Vector`` A quick reference to the layer
     */
    layer: null,

    /** api: property[popup]
     * ``GeoExt.Popup``
     *  The popup containing 'confirm' and 'cancel' buttons shown on feature
     *  select
     */
    popup: null,

    /** api: property[selectControl]
     * ``OpenLayers.Control.Select`` A quick reference to the select control
     */
    selectControl: null,

    /** api: property[cancel]
     * ``Boolean``
     *  Used to let the editfeature control know to cancel the modifications.
     *  Defaults to true, which means that by default modifications are not
     *  saved unless the user click the "ok" button of the popup.
     */
    cancel: true,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
        this.editFeature && this.bindEditFeature();
    },

    /** private: method[constructor]
     *  Set this widget private properties and listen to editfeature control
     *  "activate" and "deactivate" events to manage the confirm popup opening
     *  and closing.
     *
     *  When using this widget, the editfeature "SelectFeature" can't no longer
     *  unselect a feature by clicking out of it.
     */
    bindEditFeature: function() {
        this.editFeature.confirm = this;
        this.layer = this.editFeature.layer;
        this.selectControl = this.editFeature.getSelectControl();
        this.selectControl.toggle = false;
        this.selectControl.clickout = false;
        this.editFeature.events.on({
            "activate": this.onEditFeatureActivate,
            "deactivate": this.onEditFeatureDeactivate,
            "scope": this
        });
    },

    /** private: method[onEditFeatureActivate]
     *  Called on editfeature "activate" event trigger.  Add layer listeners.
     */
    onEditFeatureActivate: function() {
        this.layer.events.on(this.getLayerEventListeners());
    },

    /** private: method[onEditFeatureDeactivate]
     *  Called on editfeature "deactivate" event trigger.  Remove layer
     *  listeners.
     */
    onEditFeatureDeactivate: function() {
        this.layer.events.un(this.getLayerEventListeners());
    },

    /** private: method[onEditFeatureDeactivate]
     *  :return: ``Object`` The hash of layer listeners to add/remove.
     */
    getLayerEventListeners: function() {
        return {
            "beforefeaturemodified": this.openPopup,
            "afterfeaturemodified": this.closePopup,
            "scope": this
        }
    },

    /** private: method[openPopup]
     *  Open a popup on the bottom-middle part of the map viewport which
     *  contains the "confirm" and "cancel" buttons.
     */
    openPopup: function() {
        var mapExtent = this.layer.map.getExtent().scale(0.9);
        var location = new OpenLayers.LonLat(
            mapExtent.left + ((mapExtent.right - mapExtent.left) / 20),
            mapExtent.bottom
        );
        if (lastEditFeaturePopup && lastEditFeaturePopup.hide) {
            lastEditFeaturePopup.hide();
        }
        this.popup = new GeoExt.Popup({
            title: this.popupTitleText,
            html: this.popupText,
            location: location,
            map: this.layer.map,
            maximizable: false,
            collapsible: false,
            closable: false,
            width: 180,
            layout: 'fit',
            buttons: [{
                text: this.confirmButtonText,
                handler: function() {
                    if (!this.editFeature.getSelectedFeatures().length) {
                        alert('Une erreur est survenue lors de l\'utilisation de l\'outil et la sélection a été perdu. Veuillez recommencer.');
                        lastEditFeaturePopup.hide();
                        this.editFeature.deactivate();
                        this.editFeature.activate();
                    }
                    this.cancel = false;
                    this.selectControl.unselectAll();
                    this.cancel = true;
                },
                scope: this
            }, {
                text: this.cancelButtonText,
                handler: function() {
                    this.selectControl.unselectAll();
                    lastEditFeaturePopup.hide();
                    if (!this.editFeature.getSelectedFeatures().length) {
                        this.editFeature.deactivate();
                        this.editFeature.activate();
                    }
                },
                scope: this
            }]
        });
        this.popup.show();
        this.popup.unanchorPopup();
        lastEditFeaturePopup = this.popup;

        // make sure no other feature can be selected by deactivating the
        // feature handler of the select control
        this.selectControl.handlers.feature.deactivate();
    },

    /** private: method[closePopup]
     *  Close the popup.
     */
    closePopup: function(object) {
        this.popup.close();
        this.popup = null;

        // re-enable the feature handler
        this.selectControl.active &&
            this.selectControl.handlers.feature.activate();
    }
});
