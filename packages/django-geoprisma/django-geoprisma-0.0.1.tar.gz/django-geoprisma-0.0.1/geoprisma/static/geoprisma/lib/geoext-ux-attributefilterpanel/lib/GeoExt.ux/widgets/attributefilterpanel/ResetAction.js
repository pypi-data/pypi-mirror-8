/**
 * Copyright (c) 2008-2010 The Open Source Geospatial Foundation
 *
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */
 
Ext.namespace("GeoExt.ux.form");

GeoExt.ux.form.ResetAction = Ext.extend(Ext.form.Action, {
	/** private: property[type]
	 *  ``String`` The action type string.
	 */
	type: "reset",

	/** api: property[formPanel]
	 *  ``GeoExt.ux.form.AttributeFilterPanel`` form object
	 */
	formPanel: null,

	/** private
	 *  (used by ``GeoExt.ux.form.AttributeFilterBasicForm``)
	 */
	constructor: function(form, options) {
		Ext.apply(this, options);
		GeoExt.ux.form.ResetAction.superclass.constructor.call(this, form, options);
	},

	/** private: method[run]
	 *  Run the action.
	 */
	run: function() {
		var o = this.options;
		if (this.formPanel) {
			// clear the contents of the form fields
			var data = {};
			this.formPanel.items.each(function(item) {
				data[item.getName()] = null;
			});
			var emptyRecord = new Ext.data.Record(data);
			this.formPanel.getForm().loadRecord(emptyRecord);
		}
		
		if (o.layer) {
			// clear the layer's filter and refresh the layer
			o.layer.filter = null;
			// o.layer.refresh({force: true});
			// reexecute the filter action instead...
			var action = new GeoExt.ux.form.FilterAction(this.form, o);
			GeoExt.form.BasicForm.superclass.doAction.call(
				this.form, action, o
			);
		}

	}

});
