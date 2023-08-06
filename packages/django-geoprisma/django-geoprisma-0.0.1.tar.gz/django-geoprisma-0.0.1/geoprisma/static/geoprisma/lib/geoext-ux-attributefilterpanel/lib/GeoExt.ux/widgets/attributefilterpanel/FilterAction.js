/**
 * Copyright (c) 2008-2010 The Open Source Geospatial Foundation
 *
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

Ext.namespace("GeoExt.ux.form");


GeoExt.ux.form.FilterAction = Ext.extend(Ext.form.Action, {
	/** private: property[type]
	 *  ``String`` The action type string.
	 */
	type: "filter",
		
	/** api: property[formToFilter]
	 *  ``GeoExt.ux.form.FormToFilter`` object that defines the mapping
	 *  from the Form contents to the Filter object (by calling its toFilter()
	 *  method).
	 *  Defaults to an instance of GeoExt.ux.form.FormToFilter with
	 *  the default options.
	 */
	 formToFilter: new GeoExt.ux.form.FormToFilter(),

	/** private
	 *  (used by ``GeoExt.ux.form.AttributeFilterBasicForm``)
	 */
	constructor: function(form, options) {
		Ext.apply(this, options);
		GeoExt.ux.form.FilterAction.superclass.constructor.call(this, form, options);
	},

	/** private: method[run]
	 *  Run the action.
	 */
	run: function() {
		var o = this.options;
		var f = this.formToFilter.toFilter(this.form, o.logicalOp, o.wildcard);
		
		if (o.clientValidation === false || this.form.isValid()) {

			if (o.layer) {
				if (f != null) {
					o.layer.filter = f;
					o.layer.refresh({force: true});
					/*
					if (this.strategy && this.strategy instanceof OpenLayers.Strategy.Fixed) {
						this.strategy.load();
					}
					*/
				} else if (this.noFeaturesOnEmptyForm) {
					o.layer.removeAllFeatures();
					o.layer.redraw();
				}
			}

		} else if (o.clientValidation !== false){
			// client validation failed
			this.failureType = Ext.form.Action.CLIENT_INVALID;
			this.form.afterAction(this, false);
		}
	}

});

