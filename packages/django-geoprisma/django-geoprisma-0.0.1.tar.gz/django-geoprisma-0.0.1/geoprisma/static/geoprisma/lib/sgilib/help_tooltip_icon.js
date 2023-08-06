var HelpTooltipIcon;

HelpTooltipIcon = (function() {

    function HelpTooltipIcon(config) {

		// The name of the input
        this.id = config.id;

		// Hint text
        this.text = config.text;

		// class
		this.cls = 'hintIcon';
		if (config.cls)
			this.cls = config.cls;

		// style
		this.style = {};
		if (config.style)
			this.style = config.style;

		// columnWidth
		this.columnWidth;
		if (config.columnWidth)
			this.columnWidth = config.columnWidth;

		// create
		this.content = null;
		this.create();

		return this.content;
	}

	// Create
	HelpTooltipIcon.prototype.create = function() {
		this.listeners = {
			afterrender: function() {
				new Ext.ToolTip({
					showDelay: 1,
					hideDelay: 1,
					target: this.id,
					anchor: 'top',
					defaultAlign: 'tl',
					bodyStyle: {padding: '2px'},
					anchorOffset: -5, // center the anchor on the tooltip
					html: this.tooltipText
				});

				Ext.QuickTips.init();
			}
		};

		this.content = new Ext.form.Label({
			cls: this.cls,
			style: this.style,
			columnWidth: this.columnWidth,
			text: ' ',
			scope: this,
			tooltipText: this.text,
			listeners: this.listeners
		});
		if (this.id) {
			this.content.id = this.id;
		}
	}

	// get
	HelpTooltipIcon.prototype.get = function() {
		return this.content;
	}

	return HelpTooltipIcon;
})();