/**
 * Copyright (c) 2008-2010 The Open Source Geospatial Foundation
 *
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

/** api: (define)
 *  module = GeoExt.ux.form
 *  class = AttributeFilterPanel
 *  base_link = `Ext.form.FormPanel <http://dev.sencha.com/deploy/dev/docs/?class=Ext.form.FormPanel>`_
 */

/**
 * @include GeoExt/ux/widgets/form/AttributeFilterBasicForm.js
 */

Ext.namespace("GeoExt.ux.form");

/** api: example
 *  Sample code showing how to use a GeoExt ux attribute filter panel.
 *
 *  .. code-block:: javascript
 *
 *      var filterPanel = new GeoExt.ux.form.AttributeFilterPanel({
 *          renderTo: "filterpanel",
 *          layer: myVectorLayer,    // vector layer to apply the filter on
 *          items: [{
 *              xtype: "textfield",
 *              name: "name__ilike",
 *              fieldLabel: "Mountain name",
 *              
 *          }, {
 *              xtype: "textfield",
 *              name: "elevation__ge",
 *              value: "2000"
 *          }]
 *      });
 *
 *      formPanel.addButton({
 *          text: "filter",
 *          handler: function() {
 *              this.filter();
 *          },
 *          scope: filterPanel
 *      });
 */

/** api: constructor
 *  .. class:: FormPanel(config)
 *
 *      A specific ``Ext.form.FormPanel`` whose internal form is a
 *      :class:`GeoExt.ux.form.AttributeFilterBasicForm` instead of
 *      ``Ext.form.BasicForm``.
 *      One would use this form to apply attribute filters on a
 *      vector layer (``OpenLayers.Layer.Vector``).
 *
 *      Look at :class:`GeoExt.ux.form.FormToFilter` to understand how
 *      form fields must be named for appropriate filters to be
 *      passed to the layer.
 */
GeoExt.ux.form.AttributeFilterPanel = Ext.extend(Ext.form.FormPanel, {
	
	/** api: config[layer]
	 *  ``OpenLayers.Layer.Vector`` The vector layer to apply the filter to
	 */
	 layer: null,

    /** private: method[createForm]
     *  Create the internal :class:`GeoExt.ux.form.AttributeFilterBasicForm`
     *  instance.
     */
    createForm: function() {
        delete this.initialConfig.listeners;
        return new GeoExt.ux.form.AttributeFilterBasicForm(null, this.initialConfig);
    },

    /** api: method[filter]
     *  :param options: ``Object`` The options passed to the
     *      :class:`GeoExt.ux.form.FilterAction` constructor.
     *
     *  Shortcut to the internal form's filter method.
     */
    filter: function(options) {
        this.getForm().filter(options);
    },
    
    /** api: method[reset]
     *  :param options: ``Object`` The options passed to the
     *      :class:`GeoExt.ux.form.ResetAction` constructor.
     *
     *  Shortcut to the internal form's reset method.
     */
    reset: function(options) {
    	this.getForm().reset(options);
    }
});

/** api: xtype = gxux_attributefilterpanel */
Ext.reg("gxux_attributefilterpanel", GeoExt.ux.form.AttributeFilterPanel);
