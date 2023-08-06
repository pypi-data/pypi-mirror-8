var GeomFieldSwitcher;

GeomFieldSwitcher = (function() {

    function GeomFieldSwitcher(config) {

		// The name of the input
        this.name = config.name;

		// CSS
		this.style = { marginLeft: 6 };
		if (config.style)
			this.style = config.style;

		// Define if the value is mandatory or not
		this.tinyName = false;
		if (config.tinyName === true || config.tinyName === false)
			this.tinyName = config.tinyName;

		// Column
		this.column = 1;
		if (config.column)
			this.column = config.column;

		// Width
		this.width = '80%';
		if (config.width)
			this.width = config.width;

		// an array of geom_field Objects to control
		this.targets = [];
		if (config.targets) {
			this.targets = config.targets;
		}
		else {
			alert('L\'objet de choix de projection n\'a pas d\'assignation. Celui-ci risque de ne pas fonctionner.');
		}

		// Default control projection
		this.value = null;

		// Included projection in the control
		this.projections = {};
		if (config.projections) {
			this.projections = config.projections;
		}
		else {
			this.loadProjections()
		}

		// Default control projection
		if (config.value) {
			if (config.value.key) {
				this.value = config.value.key;
			}
			else {
				this.value = config.value;
			}
		}
		if (this.projections[this.value]) {
			this.projections[this.value].defaut = true;
		}
		else {
			alert('La projection par défaut du widget de position est incorrecte.');
		}

		this.currentProjection = this.value;


		// Container
		this.container = new Ext.form.RadioGroup({
			xtype: 'radiogroup',
			layout: 'form',
			name: 'positionRadios',
			style: this.style,
			hideLabel : true,
            columns: this.column,
			width: this.width,
			items: []
		});


		// Register all projections
		this.registerProjections();

		// set value to good value
		if (this.value) {
			this.setValue(this.value);
		}
	}

	// Return current Value
	GeomFieldSwitcher.prototype.getValue = function() {
		return this.value;
	}


	// Switch to the specified projection
	GeomFieldSwitcher.prototype.setValue = function(projection) {
		// target the projection
		if (!projection.key) {
			projection = this.projections[projection];
		}

		if (projection) {
			// set correct value
			this.value = projection.key;

			//projection.fields.set;
			this.projections[projection.key].radio.checked = true;


			// loop in targets and match projection with the selector value
			for (var targetKey = 0; targetKey < this.targets.length; targetKey++) {
				this.targets[targetKey].setCurrentProjection(projection);
			}
		}
		else {
			alert('Le format de projection demandé est invalide.');
		}
	}


	// Hide
	GeomFieldSwitcher.prototype.hide = function() {
		this.container.hide();
	}


	// Show
	GeomFieldSwitcher.prototype.show = function() {
		this.container.show();
	}


	// Return all ExtJs content
	GeomFieldSwitcher.prototype.getItems = function() {
		var items = new Array();

		// projections fields
		for (key in this.projections) {
			items.push(this.projections[key].radio);
		}

		return items;
	}


	// get html data to render object
	GeomFieldSwitcher.prototype.registerProjectionField = function(projection) {
		if (projection) {
			this.projections[projection.key].radio = new Ext.form.Radio({
				xtype: 'radio',
				fieldLabel: '',
				boxLabel: ((this.tinyName == true)?projection.shortName:projection.name),
				name: this.name,
				inputValue: projection.key,
				checked: (this.getValue() == projection.key),
				hidden: projection.hidden,
				listeners: {
					check: function(radio, checked) {
						if (checked) {
							this.inputChange(projection);
						}
					},
					scope: this
				},
				scope: this
			});
		}
	};


	// load projection from all targets
	GeomFieldSwitcher.prototype.loadProjections = function() {
		// merge projections from all targets
		this.projections = {};
		// loop in targets
		for (var targetKey = 0; targetKey < this.targets.length; targetKey++) {
			// loop in projections
			var currentTargetProjections = this.targets[targetKey].projections;
			for (key in currentTargetProjections) {
				this.projections[currentTargetProjections[key].key] = currentTargetProjections[key];
				// search for default as value if no value is define
				if (!this.value && currentTargetProjections[key].defaut == true) {
					this.value = currentTargetProjections[key].key;
				}
			}
		}
	};


	// get html data to render object
	GeomFieldSwitcher.prototype.registerProjections = function() {
		// register fields
		for (key in this.projections) {
			this.projections[key].key = key;

			this.registerProjectionField(this.projections[key]);
		}
	};


	// when one input is changed
	GeomFieldSwitcher.prototype.inputChange = function(projection) {
		// set correct value
		this.setValue(projection);

		// loop in targets
		for (var targetKey = 0; targetKey < this.targets.length; targetKey++) {
			this.targets[targetKey].setCurrentProjection(projection);
		}
	};


	// get html data to render object
	GeomFieldSwitcher.prototype.get = function() {
		this.container.items = this.getItems();
		return this.container;
	};


	return GeomFieldSwitcher;

})();