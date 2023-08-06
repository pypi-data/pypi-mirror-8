var GeomField;

GeomField = (function() {

	// Constant usefull projections
	GeomField.DMS = {
		key: 'dms',
		name: 'DMS',
		shortName: 'DMS',
		epsg: 4326,
		labelX: 'Long. (DMS)',
		labelY: 'Lat. (DMS)',
		quadrantX: null,
		quadrantY: null
	};
	GeomField.DMS.NO = {
		key: GeomField.DMS.key,
		name: GeomField.DMS.name + ' (N O)',
		shortName: GeomField.DMS.shortName,
		epsg: GeomField.DMS.epsg,
		labelX: GeomField.DMS.labelX,
		labelY: GeomField.DMS.labelY,
		quadrantX: 'O',
		quadrantY: 'N'
	};
	GeomField.DMS.NW = GeomField.DMS.NO;
	GeomField.DMS.NE = {
		key: GeomField.DMS.key,
		name: GeomField.DMS.name + ' (N E)',
		shortName: GeomField.DMS.shortName,
		epsg: GeomField.DMS.epsg,
		labelX: GeomField.DMS.labelX,
		labelY: GeomField.DMS.labelY,
		quadrantX: 'E',
		quadrantY: 'N'
	};
	GeomField.DMS.SO = {
		key: GeomField.DMS.key,
		name: GeomField.DMS.name + ' (S O)',
		shortName: GeomField.DMS.shortName,
		epsg: GeomField.DMS.epsg,
		labelX: GeomField.DMS.labelX,
		labelY: GeomField.DMS.labelY,
		quadrantX: 'O',
		quadrantY: 'S'
	};
	GeomField.DMS.SW = GeomField.DMS.SO;
	GeomField.DMS.SE = {
		key: GeomField.DMS.key,
		name: GeomField.DMS.name + ' (S E)',
		shortName: GeomField.DMS.shortName,
		epsg: GeomField.DMS.epsg,
		labelX: GeomField.DMS.labelX,
		labelY: GeomField.DMS.labelY,
		quadrantX: 'E',
		quadrantY: 'S'
	};
	GeomField.DECIMAL = {
		key: 'decimal',
		name: 'Degrés déc.',
		shortName: 'Déc.',
		epsg: 4326,
		labelX: 'Long. (déc.)',
		labelY: 'Lat. (déc.)'
	};
	GeomField.MTM1 = {
		key: 'mtm1',
		name: 'MTM zone 1',
		shortName: 'MTM1',
		epsg: 32181,
		labelX: 'x (MTM 1)',
		labelY: 'y (MTM 1)'
	};
	GeomField.MTM2 = {
		key: 'mtm2',
		name: 'MTM zone 2',
		shortName: 'MTM2',
		epsg: 32182,
		labelX: 'x (MTM 2)',
		labelY: 'y (MTM 2)'
	};
	GeomField.MTM3 = {
		key: 'mtm3',
		name: 'MTM zone 3',
		shortName: 'MTM3',
		epsg: 32183,
		labelX: 'x (MTM 3)',
		labelY: 'y (MTM 3)'
	};
	GeomField.MTM4 = {
		key: 'mtm4',
		name: 'MTM zone 4',
		shortName: 'MTM4',
		epsg: 32184,
		labelX: 'x (MTM 4)',
		labelY: 'y (MTM 4)'
	};
	GeomField.MTM5 = {
		key: 'mtm5',
		name: 'MTM zone 5',
		shortName: 'MTM5',
		epsg: 32185,
		labelX: 'x (MTM 5)',
		labelY: 'y (MTM 5)'
	};
	GeomField.MTM6 = {
		key: 'mtm6',
		name: 'MTM zone 6',
		shortName: 'MTM6',
		epsg: 32186,
		labelX: 'x (MTM 6)',
		labelY: 'y (MTM 6)'
	};
	GeomField.MTM7 = {
		key: 'mtm7',
		name: 'MTM zone 7',
		shortName: 'MTM7',
		epsg: 32187,
		labelX: 'x (MTM 7)',
		labelY: 'y (MTM 7)'
	};
	GeomField.MTM8 = {
		key: 'mtm8',
		name: 'MTM zone 8',
		shortName: 'MTM8',
		epsg: 32188,
		labelX: 'x (MTM 8)',
		labelY: 'y (MTM 8)'
	};
	GeomField.MTM9 = {
		key: 'mtm9',
		name: 'MTM zone 9',
		shortName: 'MTM9',
		epsg: 32189,
		labelX: 'x (MTM 9)',
		labelY: 'y (MTM 9)'
	};
	GeomField.MTM10 = {
		key: 'mtm10',
		name: 'MTM zone 10',
		shortName: 'MTM10',
		epsg: 32191,
		labelX: 'x (MTM 10)',
		labelY: 'y (MTM 10)'
	};
	GeomField.MTM11 = {
		key: 'mtm11',
		name: 'MTM zone 11',
		shortName: 'MTM11',
		epsg: 32191,
		labelX: 'x (MTM 11)',
		labelY: 'y (MTM 11)'
	};
	GeomField.MTM12 = {
		key: 'mtm12',
		name: 'MTM zone 12',
		shortName: 'MTM12',
		epsg: 32192,
		labelX: 'x (MTM 12)',
		labelY: 'y (MTM 12)'
	};
	GeomField.MTM13 = {
		key: 'mtm13',
		name: 'MTM zone 13',
		shortName: 'MTM13',
		epsg: 32193,
		labelX: 'x (MTM 13)',
		labelY: 'y (MTM 13)'
	};
	GeomField.MTM14 = {
		key: 'mtm14',
		name: 'MTM zone 14',
		shortName: 'MTM14',
		epsg: 32194,
		labelX: 'x (MTM 14)',
		labelY: 'y (MTM 14)'
	};
	GeomField.MTM15 = {
		key: 'mtm15',
		name: 'MTM zone 15',
		shortName: 'MTM15',
		epsg: 32195,
		labelX: 'x (MTM 15)',
		labelY: 'y (MTM 15)'
	};
	GeomField.MTM16 = {
		key: 'mtm16',
		name: 'MTM zone 16',
		shortName: 'MTM16',
		epsg: 32196,
		labelX: 'x (MTM 16)',
		labelY: 'y (MTM 16)'
	};
	GeomField.GOOGLE = {
		key: 'google',
		name: 'Google',
		shortName: 'Google',
		epsg: 900913,
		labelX: 'x (google)',
		labelY: 'y (google)'
	}

    function GeomField(config) {

		// The name of the input
        this.name = config.name;

		// Define the width of the label
		this.labelWidth = 65;
		if (config.labelWidth)
			this.labelWidth = config.labelWidth;

		// Define if the value is mandatory or not
		this.allowBlank = true;
		if (config.allowBlank === true || config.allowBlank === false)
			this.allowBlank = config.allowBlank;

		// Define how many decimal to keep (null value disable the round operation)
		this.decimalNumber = null;
		if (config.decimalNumber)
			this.decimalNumber = config.decimalNumber;

		// Included projection in the control
		this.projections = {
			'dms': 		GeomField.DMS,
			'decimal': 	GeomField.DECIMAL,
			'mtm7': 	GeomField.MTM7,
			'mtm8': 	GeomField.MTM8
		};
		if (config.projections) {
			this.projections = config.projections;
		}

		// Default control projection
		this.defaultProjection = 'dms';
		if (config.defaultProjection) {
			if (config.defaultProjection.key) {
				this.defaultProjection = config.defaultProjection.key;
			}
			else {
				this.defaultProjection = config.defaultProjection;
			}
		}
		if (this.projections[this.defaultProjection]) {
			this.projections[this.defaultProjection].defaut = true;
		}
		else {
			alert('La projection par défaut du widget de position est incorrecte.');
		}

		this.currentProjection = this.defaultProjection;


		// Input / Output projection
		this.IOProjection = GeomField.MTM7.epsg;
		if (config.IOProjection) {
			if (this.projections[config.IOProjection]) {
				this.IOProjection = this.projections[config.IOProjection].epsg;
			}
			else if (config.IOProjection.epsg) {
				this.IOProjection = config.IOProjection.epsg;
			}
			else if (config.IOProjection > 0) {
				this.IOProjection = config.IOProjection;
			}
			else {
				alert('La projection d\'entrée/sortie du widget de position est incorrecte.');
			}
		}

		// Fields
		this.fieldX = new Ext.form.Hidden({
			xtype: 'hidden',
			name: 'x_'+this.name,
			allowBlank: this.allowBlank,
			scope: this,
			value: 0
		});

		this.fieldY = new Ext.form.Hidden({
			xtype: 'hidden',
			name: 'y_'+this.name,
			allowBlank: this.allowBlank,
			scope: this,
			value: 0
		});

		this.fields = {
			'x': this.fieldX,
			'y': this.fieldY
		}


		// initialised
		this.loadedInForm = false;


		// Register all projections
		this.registerProjections();

	}

	// Return current Value
	GeomField.prototype.getValue = function() {
		return {
			'x': this.fields.x.getValue(),
			'y': this.fields.y.getValue()
		}
	}

	// Set current Value
	GeomField.prototype.setValue = function(point, updateInput) {
		// convert WKT point
		if (typeof point === "string") {
			point = this.pointFromWKT(point);
		}

		// default value of update input param
		if (typeof updateInput === "undefined") {
			updateInput = true;
		}

		var fixOriginalValue = false;
		if (this.fields.x.getValue() == 0 && this.fields.y.getValue() == 0) {
			fixOriginalValue = true;
		}

		// set value
		this.fields.x.setValue(point.x);
		this.fields.y.setValue(point.y);

		// set not dirty
		if (fixOriginalValue) {
			this.fields.x.originalValue = point.x;
			this.fields.y.originalValue = point.y;
		}

		if (updateInput == true) {
			this.inputUpdate(this.getValue());
		}
	}


	// Switch to the specified projection
	GeomField.prototype.setCurrentProjection = function(projection) {
		// use the good way to define how the key is passed
		var currentKey;
		if (projection.key) {
			currentKey = projection.key;
		}
		else {
			currentKey = projection;
		}
		this.currentProjection = projection;

		for (key in this.projections) {
			if (key == currentKey) { // show good key
				this.projections[key].fields.x.show();
				this.projections[key].fields.y.show();
				if (this.projections[key].fields.x.xtype == 'panel' && this.loadedInForm) {
					this.projections[key].fields.x.syncSize();
				}
				if (this.projections[key].fields.y.xtype == 'panel' && this.loadedInForm) {
					this.projections[key].fields.y.syncSize();
				}
			}
			else { // hide all
				this.projections[key].fields.x.hide();
				this.projections[key].fields.y.hide();
			}
		}
	}


	// Hide
	GeomField.prototype.hide = function() {
		for (key in this.projections) {
			this.projections[key].fields.x.hide();
			this.projections[key].fields.y.hide();
		}
	}


	// Show
	GeomField.prototype.show = function() {
		this.setCurrentProjection(this.currentProjection);
	}


	// Convert a WKT to a coordinate
	GeomField.prototype.pointFromWKT = function(geomwkt) {
		// to remove the SRID
		geomwkt = geomwkt.split(';');
		return OpenLayers.Geometry.fromWKT(geomwkt[0]);
	}


	// Return all ExtJs content
	GeomField.prototype.getItems = function() {
		var items = new Array();

		// principal fields
		items.push(this.fields.x);
		items.push(this.fields.y);

		// projections fields
		for (key in this.projections) {
			items.push(this.projections[key].fields.x);
			items.push(this.projections[key].fields.y);
		}

		return items;
	}


	// get html data to render object
	GeomField.prototype.registerProjectionField = function(projection) {
		var currentProjectionForm = {}

		currentProjectionForm['x'] = new Ext.form.TextField({
			fieldLabel: projection.labelX,
			xtype: 'textfield',
			name: 'x_'+projection.key+'_'+this.name,
			width: '85%',
			hidden: (!projection.defaut),
			allowBlank: this.allowBlank,
			scope: this,
			maskRe: /^[0-9\.\-]*$/,
			listeners: {
				change: function(field, newValue, oldValue) {
					this.scope.inputChange(projection);
				}
			}
		});

		currentProjectionForm['y'] = new Ext.form.TextField({
			fieldLabel: projection.labelY,
			xtype: 'textfield',
			name: 'y_'+projection.key+'_'+this.name,
			width: '85%',
			hidden: (!projection.defaut),
			allowBlank: this.allowBlank,
			scope: this,
			maskRe: /^[0-9\.\-]*$/,
			listeners: {
				change: function(field, newValue, oldValue) {
					this.scope.inputChange(projection);
				}
			}
		});

		// Store form data in the projection data
		this.projections[projection.key].fields = currentProjectionForm;
	};


	// get html data to render object using special DMS format
	GeomField.prototype.registerProjectionDMSField = function(projection) {
		var currentProjectionForm = {}
		currentProjectionForm['deg'] = {}
		currentProjectionForm['min'] = {}
		currentProjectionForm['sec'] = {}
		currentProjectionForm['quadrant'] = {}

        currentProjectionForm['deg']['x'] = new Ext.form.TextField({
            xtype: 'textfield',
            name: 'x_'+projection.key+'_deg'+'_'+this.name,
            width: '95%',
            allowBlank: this.allowBlank,
            scope: this,
			maskRe: /^[0-9\-]*$/,
			style: {'text-align':'right', 'padding-left':'0px', 'padding-right':'1px'},
            listeners: {
				change: function(field, newValue, oldValue) {
					this.scope.inputChange(projection);
				}
            }
        });
        currentProjectionForm['min']['x'] = new Ext.form.TextField({
            xtype: 'textfield',
            name: 'x_'+projection.key+'_min'+'_'+this.name,
            width: '95%',
            allowBlank: this.allowBlank,
            scope: this,
			maskRe: /^[0-9]*$/,
			style: {'text-align':'right', 'padding-left':'0px', 'padding-right':'1px'},
            listeners: {
				change: function(field, newValue, oldValue) {
					this.scope.inputChange(projection);
				}
            }
        });
        currentProjectionForm['sec']['x'] = new Ext.form.TextField({
            xtype: 'textfield',
            name: 'x_'+projection.key+'_sec'+'_'+this.name,
            width: '95%',
            allowBlank: this.allowBlank,
            scope: this,
			maskRe: /^[0-9.]*$/,
			style: {'text-align':'right', 'padding-left':'0px', 'padding-right':'1px'},
            listeners: {
				change: function(field, newValue, oldValue) {
					this.scope.inputChange(projection);
				}
            }
        });
		// add quadrant
		var groupQuadrantX;
		if (projection.quadrantX) {
			currentProjectionForm['quadrant']['x'] = new Ext.form.Hidden({
				xtype: 'hidden',
				name: 'x_'+projection.key+'_quadrant'+'_'+this.name,
				allowBlank: this.allowBlank,
				scope: this,
				value: projection.quadrantX
			})
			groupQuadrantX = [
				currentProjectionForm['quadrant']['x'],
				new Ext.form.Label({
					cls: 'x-form-item',
					width: 10,
					html: (projection.quadrantX == 1)?'E':'O',
					style: {
						marginTop: 3
					}
				})
			];
		}
		else {
			currentProjectionForm['quadrant']['x'] = new Ext.form.ComboBox({
				name: 'x_'+projection.key+'_quadrant'+'_'+this.name,
				allowBlank: this.allowBlank,
				width: 17,
				forceSelection: true,
				hideTrigger: true,
				editable: false,
				selectOnFocus: false,
				scope: this,
				autoScroll: false,
				store: new Ext.data.SimpleStore({
					fields: ['text', 'value'],
					data :  [['E', 1], ['O', -1]]
				}),
				displayField: 'text',
				valueField: 'value',
				typeAhead: true,
				mode: 'local',
				triggerAction: 'all',
				listeners: {
					change: function(field, newValue, oldValue) {
						this.scope.inputChange(projection);
					}
				}
			});
			groupQuadrantX = [currentProjectionForm['quadrant']['x']];
		}


        currentProjectionForm['deg']['y'] = new Ext.form.TextField({
            xtype: 'textfield',
            name: 'y_'+projection.key+'_deg'+'_'+this.name,
            width: '95%',
            allowBlank: this.allowBlank,
            scope: this,
			maskRe: /^[0-9\-]*$/,
			style: {'text-align':'right', 'padding-left':'0px', 'padding-right':'1px'},
            listeners: {
				change: function(field, newValue, oldValue) {
					this.scope.inputChange(projection);
				}
            }
        });
        currentProjectionForm['min']['y'] = new Ext.form.TextField({
            xtype: 'textfield',
            name: 'y_'+projection.key+'_min'+'_'+this.name,
            width: '95%',
            allowBlank: this.allowBlank,
            scope: this,
			maskRe: /^[0-9]*$/,
			style: {'text-align':'right', 'padding-left':'0px', 'padding-right':'1px'},
            listeners: {
				change: function(field, newValue, oldValue) {
					this.scope.inputChange(projection);
				}
            }
        });
        currentProjectionForm['sec']['y'] = new Ext.form.TextField({
            xtype: 'textfield',
            name: 'y_'+projection.key+'_sec'+'_'+this.name,
            width: '95%',
            allowBlank: this.allowBlank,
            scope: this,
			maskRe: /^[0-9.]*$/,
			style: {'text-align':'right', 'padding-left':'0px', 'padding-right':'1px'},
            listeners: {
				change: function(field, newValue, oldValue) {
					this.scope.inputChange(projection);
				}
            }
        });
		// add quadrant
		var groupQuadrantY;
		if (projection.quadrantY) {
			currentProjectionForm['quadrant']['y'] = new Ext.form.Hidden({
				xtype: 'hidden',
				name: 'y_'+projection.key+'_quadrant'+'_'+this.name,
				allowBlank: this.allowBlank,
				scope: this,
				value: projection.quadrantY
			})
			groupQuadrantY = [
				currentProjectionForm['quadrant']['y'],
				new Ext.form.Label({
					cls: 'x-form-item',
					width: 10,
					html: (projection.quadrantY == 1)?'N':'S',
					style: {
						marginTop: 3
					}
				})
			];
		}
		else {
			currentProjectionForm['quadrant']['y'] = new Ext.form.ComboBox({
				name: 'y_'+projection.key+'_quadrant'+'_'+this.name,
				allowBlank: this.allowBlank,
				width: 17,
				forceSelection: true,
				hideTrigger: true,
				editable: false,
				selectOnFocus: false,
				scope: this,
				autoScroll: false,
				store: new Ext.data.SimpleStore({
					fields: ['text', 'value'],
					data :  [['N', 1], ['S', -1]]
				}),
				displayField: 'text',
				valueField: 'value',
				typeAhead: true,
				mode: 'local',
				triggerAction: 'all',
				listeners: {
					change: function(field, newValue, oldValue) {
						this.scope.inputChange(projection);
					}
				}
			});
			groupQuadrantY = [currentProjectionForm['quadrant']['y']];
		}

		// fix for IE fieldsize
		if (Ext.isIE) {
			currentProjectionForm['deg']['x'].width = '80%';
			currentProjectionForm['deg']['x'].style = {'text-align':'right', 'padding-left':0, 'padding-right':1};
			currentProjectionForm['deg']['y'].width = '80%';
			currentProjectionForm['deg']['y'].style = {'text-align':'right', 'padding-left':0, 'padding-right':1};
			currentProjectionForm['min']['x'].width = '80%';
			currentProjectionForm['min']['x'].style = {'text-align':'right', 'padding-left':0, 'padding-right':1};
			currentProjectionForm['min']['y'].width = '80%';
			currentProjectionForm['min']['y'].style = {'text-align':'right', 'padding-left':0, 'padding-right':1};
			currentProjectionForm['sec']['x'].width = '87%';
			currentProjectionForm['sec']['x'].style = {'text-align':'right', 'padding-left':0, 'padding-right':1};
			currentProjectionForm['sec']['y'].width = '87%';
			currentProjectionForm['sec']['y'].style = {'text-align':'right', 'padding-left':0, 'padding-right':1};
		}

        currentProjectionForm['x'] = new Ext.Panel({ // DMS inputs
			xtype: 'panel',
            layout:'column',
            fieldLabel: projection.labelX,
            name: 'x_'+projection.key+'_'+this.name,
			hidden: (!projection.defaut),
            columnWidth: .75,
			height: 22,
            items: [{
                columnWidth: .30,
                items: [
                    currentProjectionForm['deg']['x']
                ]
            },{
                width: 10,
                html: '°'
            },{
                columnWidth: .30,
                items: [
                    currentProjectionForm['min']['x']
                ]
            },{
                width: 10,
                html: "'"
            },{
                columnWidth: .40,
                items: [
                    currentProjectionForm['sec']['x']
                ]
            },{
                width: 10,
                html: '"'
            },
			groupQuadrantX
			]
        });

        currentProjectionForm['y'] = new Ext.Panel({ // DMS inputs
			xtype: 'panel',
            layout:'column',
            fieldLabel: projection.labelY,
            name: 'y_'+projection.key+'_'+this.name,
			hidden: (!projection.defaut),
            columnWidth: .75,
			height: 22,
            items: [{
                columnWidth: .30,
                items: [
                    currentProjectionForm['deg']['y']
                ]
            },{
                width: 10,
                html: '°'
            },{
                columnWidth: .30,
                items: [
                    currentProjectionForm['min']['y']
                ]
            },{
                width: 10,
                html: "'"
            },{
                columnWidth: .40,
                items: [
                    currentProjectionForm['sec']['y']
                ]
            },{
                width: 10,
                html: '"'
            },
			groupQuadrantY
			]
        });

		// Store form data in the projection data
		this.projections[projection.key].fields = currentProjectionForm;
    }


	// get html data to render object
	GeomField.prototype.registerProjections = function() {
		for (key in this.projections) {
			this.projections[key].key = key;
			if (key == 'dms') {
				// ajust Y quadrant (replace by 1, -1 or null)
				if (this.projections[key].quadrantY) {
					if (this.projections[key].quadrantY.toString().toUpperCase().indexOf('N', 'NORD', 'NORTH', '1', 1) != -1) {
						this.projections[key].quadrantY = 1;
					}
					else if (this.projections[key].quadrantY.toString().toUpperCase().indexOf('S', 'SUD', 'SOUTH', '-1', -1) != -1) {
						this.projections[key].quadrantY = -1;
					}
					else if (this.projections[key].quadrantY != 1 && this.projections[key].quadrantY != -1){
						this.projections[key].quadrantY = null;
					}
				}
				// ajust X quadrant (replace by 1, -1 or null)
				if (this.projections[key].quadrantX) {
					if (this.projections[key].quadrantX.toString().toUpperCase().indexOf('E', 'EST', 'EAST', '1', 1) != -1) {
						this.projections[key].quadrantX = 1;
					}
					else if (this.projections[key].quadrantX.toString().toUpperCase().indexOf('O', 'W', 'OUEST', 'WEST', '-1', -1) != -1) {
						this.projections[key].quadrantX = -1;
					}
					else if (this.projections[key].quadrantX != 1 && this.projections[key].quadrantX != -1) {
						this.projections[key].quadrantX = null;
					}
				}
				this.registerProjectionDMSField(this.projections[key]);
			}
			else {
				this.registerProjectionField(this.projections[key]);
			}
		}
	};


	// Fill all input fields with a coordinate from a projection (no projection use main widget projection)
	GeomField.prototype.inputUpdate = function(coordinate, projection) {
		if (!projection) {
			projection = {
				'epsg': this.IOProjection,
				'key': null
			}
		}

		// update data of all projection
		for (key in this.projections) {
			var targetProjection = this.projections[key]
			// avoid to convert to self projection because it's stupid and useless
			if (key != projection.key) {
				// Launch convertion
				var newCoordinate = this.convertCoordinateProjection(
					coordinate.x,			// x
					coordinate.y,			// y
					projection.epsg,		// input epsg
					targetProjection.epsg	// output epsg
				)
				// exception for DMS
				if (key == 'dms') {
					newCoordinate = this.convertCoordinateFromDecimalToDMS(newCoordinate['x'], newCoordinate['y']);
					targetProjection.fields.deg.x.setValue(newCoordinate['x'][0]);
					targetProjection.fields.deg.y.setValue(newCoordinate['y'][0]);
					targetProjection.fields.min.x.setValue(newCoordinate['x'][1]);
					targetProjection.fields.min.y.setValue(newCoordinate['y'][1]);
					targetProjection.fields.sec.x.setValue(newCoordinate['x'][2]);
					targetProjection.fields.sec.y.setValue(newCoordinate['y'][2]);

					// original value update
					targetProjection.fields.deg.x.originalValue = newCoordinate['x'][0];
					targetProjection.fields.deg.y.originalValue = newCoordinate['y'][0];
					targetProjection.fields.min.x.originalValue = newCoordinate['x'][1];
					targetProjection.fields.min.y.originalValue = newCoordinate['y'][1];
					targetProjection.fields.sec.x.originalValue = newCoordinate['x'][2];
					targetProjection.fields.sec.y.originalValue = newCoordinate['y'][2];

					// cadrant fixer
					if (this.projections[key].quadrantX) {
						targetProjection.fields.deg.x.setValue(targetProjection.fields.deg.x.value * newCoordinate['x'][3] * this.projections[key].quadrantX);
						targetProjection.fields.deg.x.originalValue = targetProjection.fields.deg.x.originalValue * newCoordinate['x'][3] * this.projections[key].quadrantX;
					}
					else {
						targetProjection.fields.quadrant.x.setValue(newCoordinate['x'][3]);
						targetProjection.fields.quadrant.x.originalValue = newCoordinate['x'][3];
					}
					if (this.projections[key].quadrantY) {
						targetProjection.fields.deg.y.setValue(targetProjection.fields.deg.y.value * newCoordinate['y'][3] * this.projections[key].quadrantY);
						targetProjection.fields.deg.y.originalValue = targetProjection.fields.deg.y.originalValue * newCoordinate['y'][3] * this.projections[key].quadrantY;
					}
					else {
						targetProjection.fields.quadrant.y.setValue(newCoordinate['y'][3]);
						targetProjection.fields.quadrant.y.originalValue = newCoordinate['y'][3];
					}
				}
				// for all normal projection
				else {
					targetProjection.fields.x.setValue(newCoordinate['x']);
					targetProjection.fields.y.setValue(newCoordinate['y']);

					// original value update
					targetProjection.fields.x.originalValue = newCoordinate['x'];
					targetProjection.fields.y.originalValue = newCoordinate['y'];
				}
			}
		}
	}


	// when one input is changed
	GeomField.prototype.inputChange = function(projection) {
		// source of the convertion
		var convertedCoordinate = {};
		// exception for DMS
		if (projection.key == 'dms') {
			convertedCoordinate = this.convertCoordinateFromDMStoDecimal(
				[projection.fields.deg.x.getValue(), projection.fields.min.x.getValue(), projection.fields.sec.x.getValue(), projection.fields.quadrant.x.getValue()],
				[projection.fields.deg.y.getValue(), projection.fields.min.y.getValue(), projection.fields.sec.y.getValue(), projection.fields.quadrant.y.getValue()]
			)
		}
		// for all normal projection
		else {
			convertedCoordinate = {
				'x': projection.fields.x.getValue(),
				'y': projection.fields.y.getValue()
			}
		}

		// main value convertion
		this.setValue(this.convertCoordinateProjection(
			convertedCoordinate.x,		// x
			convertedCoordinate.y,		// y
			projection.epsg,		// input epsg
			this.IOProjection		// output epsg
		), false)

		// update data of all projection
		this.inputUpdate(convertedCoordinate, projection);
	};


	// convert a coordinate between two projections
	GeomField.prototype.convertCoordinateProjection = function(x, y, fromProjection, toProjection) {
		var result = new Array();

		x = parseFloat(x);
		y = parseFloat(y);

		// la coordonnée long a convertir doit absolument être négative pour une conversion valide en MTM7
		if (x > 0) {x = x*1};

		// error handling
		if (!Proj4js.defs["EPSG:"+fromProjection]){
			alert('Conversion de projection : La projection "EPSG:'+fromProjection+'" n\'est pas préchargé, la conversion risque de ne pas fonctionner.');
		}
		if (!Proj4js.defs["EPSG:"+toProjection]){
			alert('Conversion de projection : La projection "EPSG:'+toProjection+'" n\'est pas préchargé, la conversion risque de ne pas fonctionner.');
		}

		// convert : Decimal --> MTM
		var projIn = new OpenLayers.Projection("EPSG:"+fromProjection);
		var projOut = new OpenLayers.Projection("EPSG:"+toProjection);
		var point = new OpenLayers.LonLat(x, y);
		point.transform(projIn, projOut);

		// arrondir
		if (this.decimalNumber) {
			result['x'] = roundOff(point.lon, this.decimalNumber);
			result['y'] = roundOff(point.lat, this.decimalNumber);
		}
		else {
			result['x'] = point.lon;
			result['y'] = point.lat;
		}

		// ne pas autoriser de NaN à sortir
		if (isNaN(result['x'])) result['x'] = '';
		if (isNaN(result['y'])) result['y'] = '';

		return result;
	};

	GeomField.prototype.convertCoordinateFromDecimalToDMS = function(x, y) {
		var result = new Array();
		var quadrantX = 1, quadrantY = 1;

		x = parseFloat(x);
		y = parseFloat(y);

		// reverse incorect values
		if (x < 0) {
			x = -x;
			quadrantX = -1;
		}
		if (y < 0) {
			y = -y;
			quadrantY = -1;
		}

		// convert : Decimal --> DMS
		var dmsX = OpenLayers.Util.getFormattedLonLat(x, 'lon', 'dms');

		dmsX = dmsX.replace('°', '-');
		dmsX = dmsX.replace('\'', '-');
		dmsX = dmsX.replace('"', '-');
		dmsX = dmsX.split('-');
		result['x'] = dmsX;

		if (result['x'][3] == 'O' || result['x'][3] == 'W') { // inverser si la lettre est O (ou W dans les cas ou sa serais en anglais)
			result['x'][0] = result['x'][0]*-1;
		}

		var dmsY = OpenLayers.Util.getFormattedLonLat(y, 'lat', 'dms');

		dmsY = dmsY.replace('°', '-');
		dmsY = dmsY.replace('\'', '-');
		dmsY = dmsY.replace('"', '-');
		dmsY = dmsY.split('-');

		result['y'] = dmsY;

		if (result['y'][3] == 'S') { // inverser si la lettre est S
			result['y'][0] = result['y'][0]*-1;
		}

		// arrondir
		if (this.decimalNumber) {
			result['x'][2] = roundOff(result['x'][2], this.decimalNumber);
			result['y'][2] = roundOff(result['y'][2], this.decimalNumber);
		}

		// add quadrant
		result['x'][3] = quadrantX;
        result['y'][3] = quadrantY;

		// ne pas autoriser de NaN à sortir
		if (isNaN(result['x'][0])) result['x'][0] = '';
		if (isNaN(result['y'][0])) result['y'][0] = '';
		if (isNaN(result['x'][1])) result['x'][1] = '';
		if (isNaN(result['y'][1])) result['y'][1] = '';
		if (isNaN(result['x'][2])) result['x'][2] = '';
		if (isNaN(result['y'][2])) result['y'][2] = '';

		return result;
	};

	GeomField.prototype.convertCoordinateFromDMStoDecimal = function(x, y) {
		function convert(D,M,S){
			 var DD;
			 D < 0 ? DD = roundOff(D + (M/-60) + (S/-3600),6) : DD = roundOff(D + (M/60) + (S/3600),6);
			 return DD;
		}

		var result = new Array();

		 x[0] = parseInt(x[0]);
		 x[1] = parseInt(x[1]);
		 x[2] = parseFloat(x[2]);
		 y[0] = parseInt(y[0]);
		 y[1] = parseInt(y[1]);
		 y[2] = parseFloat(y[2]);

		 var LonDecimalDegrees = convert(x[0],x[1],x[2])*x[3];
		 var LatDecimalDegrees = convert(y[0],y[1],y[2])*y[3];

		 !isNaN(LonDecimalDegrees) && !(LonDecimalDegrees > 180) && !(LonDecimalDegrees < -180)  ? result['x'] = LonDecimalDegrees : result['x'] = "";
		 !isNaN(LatDecimalDegrees) && !(LatDecimalDegrees > 90) && !(LatDecimalDegrees < -90) ? result['y'] = LatDecimalDegrees : result['y'] = "";

		return result;
	};


	// get html data to render object
	GeomField.prototype.get = function() {
		this.loadedInForm = true;
		return {
			xtype: 'panel',
			layout: 'form',
			name: 'positionFields'+'_'+this.name,
			columnWidth: .7,
			labelWidth: this.labelWidth,
			style: { marginRight: 0 },
			items: [{
				layout: 'form',
				columnWidth: .5,
				labelWidth: this.labelWidth,
				style: { marginRight: 0 },
				items: this.getItems()
			}]
		}
	};

	return GeomField;

})();