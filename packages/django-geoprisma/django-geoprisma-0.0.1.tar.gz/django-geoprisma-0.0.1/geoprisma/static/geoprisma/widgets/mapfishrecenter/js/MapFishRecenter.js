/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 
/*
 * @requires
**/
/**
 * Class: mapfish.widgets.recenter.DataField
 *
 * Extends the mapfish recenter tool
 *
 * Inherits From:
 * - <mapfish.widgets.recenter.Base>
**/


mapfish.widgets.recenter.DataField.prototype.i18n_filter_field_label = "Filter";
mapfish.widgets.recenter.DataField.prototype.i18n_filter_box_label_start = "Starts with";
mapfish.widgets.recenter.DataField.prototype.i18n_filter_box_label_anywhere = "Anywhere";
mapfish.widgets.recenter.DataField.prototype.i18n_filter_box_label_end = "Ends with";
mapfish.widgets.recenter.DataField.prototype.i18n_min_char_label = "Minimum nb of characters";
mapfish.widgets.recenter.DataField.prototype.i18n_show_center_label = "Show center";
mapfish.widgets.recenter.DataField.prototype.addItems = function() {
        this.removeAll();

		var combo = Array();
		var store = Array();
	//	this.fieldLabels = this.fieldLabel.split(";");
    //    this.fieldLabel.pop();        
        this.fieldLabels = this.fieldLabel;
		this.displayFields = this.displayField.split(";");
		this.queryParams = this.queryParam.split(";");
		this.filterTypes = this.filterType.split(";");
		
		// For each field
		for (i=0; i<this.fieldLabels.length-1; i++)
		{
			store.push(new Ext.data.Store({
				id : this.name+'_'+i,
				nbrStore: i,
				reader: new GeoExt.data.FeatureReader({}, [
					{name: this.displayFields[i]}
				]),
				proxy: new GeoExt.data.ProtocolProxy({
					protocol: this.protocol
				}),
				sortInfo: {field: this.displayFields[i], direction: "ASC"}
			}));

			combo.push(new Ext.form.ComboBox({
				fieldLabel: this.fieldLabels[i],
				name: this.displayFields[i],
				mode: 'remote',
                anchor:'-20',
				minChars: this.minChars,
				typeAhead: false,  // Will not type the first result in the input
				forceSelection: false,
				hideTrigger: false,
				filterType: (this.filterTypes[i] != '')?this.filterTypes[i]:'%#%',
				displayField: this.displayFields[i],
				emptyText: OpenLayers.i18n('mf.recenter.emptyText'),
				queryParam: this.queryParams[i] || this.displayFields[i],
				store: store[i],
				listeners: {
					select : function(combo, record, index) {
					        this.onComboSelect(record); 
					}/*,
					specialkey: function(combo, event) {
						if (event.getKey() == event.ENTER) {
							this.onComboSelect(record);
						}
                                                }*/,
					scope: this
				}
			}));
			this.add(combo[i]);
		}
		
		if (this.forceFilters != "true")
		{
			var radiogroup = new Ext.form.RadioGroup({
				fieldLabel: this.i18n_filter_field_label,
				columns: 1,
				defaults: {name: 'radioNameRecenter'},
				vertical: true,
				width: '300px',
				items: [
				{
					boxLabel: this.i18n_filter_box_label_start,
					inputValue: '#%', 
					width: '300px',
					checked: true,
					listeners: {
						'check':{
							fn: function(){
									if (radiogroup.items.items[0].getGroupValue())
									{
										for (i=0; i<combo.length; i++)
										{
											combo[i].doQuery('',true);
										}
									}
									(function(){})},
									scope: this
								}
						}
				},{
					boxLabel: this.i18n_filter_box_label_anywhere,
					inputValue: '%#%',
					width: '300px',
					listeners: {
						'check':{
							fn: function(){
									if (radiogroup.items.items[0].getGroupValue())
									{
										for (i=0; i<combo.length; i++)
										{
											combo[i].doQuery('',true);
										}
									}
									(function(){})
								},
								scope: this
							}
						}
				},{
					boxLabel: this.i18n_filter_box_label_end,
					inputValue: '%#',
					width: '300px',
					listeners: {
						'check':{
							fn: function(){
									if (radiogroup.items.items[0].getGroupValue())
									{
										for (i=0; i<combo.length; i++)
										{
											combo[i].doQuery('',true);
										}
									}
									(function(){})
								},
								scope: this
							}
						}
				}]
			});
			this.add(radiogroup);
		}

  /*      var showCenterchkbox = new Ext.form.Checkbox({
               boxLabel: this.i18n_show_center_label,
               checked:false,
               width:'auto',
               name:'chkCenter',
               listeners: {
						'check':{
							fn: function(obj, state){
                                this.showCenter = state;
								},
								scope: this
							}
						}
         });

        this.add(showCenterchkbox);
*/
        // variables to set minChars from the UI

		// var char_number = [ [0], [1], [2], [3], [4], [5], [6], [7], [8] ];

        var char_number = new Array();

        for (i=0;i<=this.maxChars - this.minChars;i++)
            char_number.push([this.minChars + i]);
/*
        var numberField = new Ext.form.ComboBox({
            fieldLabel: this.i18n_min_char_label,
            hiddenName: 'number',
            store: new Ext.data.SimpleStore({
                fields: ['number'],
                data : char_number 
            }),
            displayField: 'number',
            mode: 'local',
            triggerAction: 'all',
            emptyText:'Value ...',
            forceSelection:true,
            lazyRender: true,
            anchor:'-20',
            value: this.minChars,
            listeners:{

                 'select':{
                            fn: function(obj, rec, ind){
                                //this.minChars = ind;
                                for (i=0; i<combo.length; i++)
									    {
										    combo[i].minChars = rec.data.number;
									    }
					        },
                            scope: this
                          }
            }

        });

        this.add(numberField);
        */
		for (i=0; i<store.length; i++)
		{
			// add a filter to the options passed to proxy.load, proxy.load
			// itself passes these options to protocol.read
			store[i].on({
				beforeload: function(store, options) {					
					queryable = "";

					for (j=0; j<combo.length; j++)
					{
						if (combo[j].lastQuery)
						{
							if (queryable != "") { queryable += ","; }
							queryable += combo[j].queryParam;
							if (radiogroup)
							{
								store.proxy.protocol.params[combo[j].queryParam + "__ilike"] = radiogroup.items.items[0].getGroupValue().replace(/#/g,combo[j].lastQuery);
							}else{
								store.proxy.protocol.params[combo[j].queryParam + "__ilike"] = combo[j].filterType.replace(/#/g,combo[j].lastQuery);
							}
							delete combo[j].lastQuery;
						}
					}
					store.proxy.protocol.params.queryable = queryable;
					
					
					// remove the queryParam from the store's base
					// params not to pollute the query string
					delete store.baseParams[combo[store.nbrStore].queryParam];
				},
				scope: this
			});
		}
    };

mapfish.widgets.recenter.Base.prototype.expand = Ext.FormPanel.prototype.expand;
mapfish.widgets.recenter.Base.prototype.addItems = function() {
        this.addItems();
        mapfish.widgets.recenter.Base.superclass.render.apply(this, arguments);
	};
