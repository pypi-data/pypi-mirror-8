/**
 * Copyright (c) 2008-2010 The Open Source Geospatial Foundation
 *
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

/**
 * @include GeoExt/ux/widgets/form/FilterAction.js
 * @include GeoExt/ux/widgets/form/ResetAction.js
 */

/** api: (define)
 *  module = GeoExt.ux.form
 *  class = AttributeFilterBasicForm
 *  base_link = `Ext.form.BasicForm <http://dev.sencha.com/deploy/dev/docs/?class=Ext.form.BasicForm>`_
 */

Ext.namespace("GeoExt.ux.form");

/** api: constructor
 *  .. class:: AttributeFilterBasicForm(config)
 *
 *      A specific ``Ext.form.BasicForm`` whose doAction method creates
 *      a :class:`GeoExt.ux.form.FilterAction` if it is passed the string
 *      "filter" as its first argument.
 *
 *      In most cases one would not use this class directly, but
 *      :class:`GeoExt.ux.form.AttributeFilterPanel` instead.
 */
GeoExt.ux.form.AttributeFilterBasicForm = Ext.extend(Ext.form.BasicForm, {

	/** api: config[layer]
	 *  ``OpenLayers.Layer.Vector`` The vector layer to apply a filter to
	 */
	 layer: null,

	/** api: method[doAction]
	 *  :param action: ``String or Ext.form.Action`` Either the name
	 *      of the action or a ``Ext.form.Action`` instance.
	 *  :param options: ``Object`` The options passed to the Action
	 *      constructor.
	 *  :return: :class:`GeoExt.ux.form.AttributeFilterBasicForm` This form.
	 *
	 *  Performs the action, if the string "filter" is passed as the
	 *  first argument then a :class:`GeoExt.ux.form.FilterAction` is created.
	 *  If the string "reset" is passed, then a
	 *  :class:`GeoExt.ux.form.ResetAction` is created.
	 */
	doAction: function(action, options) {
		if(action == "filter") {
			options = Ext.applyIf(options || {}, {
				layer: this.layer
			});
			action = new GeoExt.ux.form.FilterAction(this, options);
		}
		if(action == "reset") {
			options = Ext.applyIf(options || {}, {
				layer: this.layer
			});
			action = new GeoExt.ux.form.ResetAction(this, options);
		}
		return GeoExt.form.BasicForm.superclass.doAction.call(
			this, action, options
		);
	},

	/** api: method[filter]
	 *  :param options: ``Object`` The options passed to the Action
	 *      constructor.
	 *  :return: :class:`GeoExt.ux.form.AttributeFilterBasicForm` This form.
	 *  
	 *  Shortcut to do a filter action.
	 */
	filter: function(options) {
		return this.doAction("filter", options);
	},
	
	/** api: method[reset]
	 *  :param options: ``Object`` The options passed to the Action
	 *      constructor.
	 *  :return: :class:`GeoExt.ux.form.AttributeFilterBasicForm` This form.
	 *  
	 *  Shortcut to do a reset action.
	 */
	reset: function(options) {
		return this.doAction("reset", options);
	}
});
