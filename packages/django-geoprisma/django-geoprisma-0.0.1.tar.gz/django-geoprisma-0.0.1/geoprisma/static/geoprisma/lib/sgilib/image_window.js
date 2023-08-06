var ImageWindow;
var previousImageWindow;

ImageWindow = (function() {

	function ImageWindow(config) {
		// url
		this.url = config.url;
		this.urlImage = config.urlImage;
		this.urlThumb = config.urlThumb;
		this.keyImage = config.keyImage;
		this.keyFormat = config.keyFormat;

		this.currentHeight = Ext.getBody().getViewSize().height-40;

		/*
		*--------------------------------------------------
		* WINDOWS SETTINGS
		*--------------------------------------------------
		*/
		var defaultWindowOptions = {
			layout: 'fit',
			closable : true,
			border : false,
			modal: true,
			plain    : true,
			resizable : false,
			autoScroll: true,
			constrain: true,
			region: 'center'
		};

		/*
		*--------------------------------------------------
		* STORES
		*--------------------------------------------------
		*/


		/*
		*--------------------------------------------------
		* STYLES
		*--------------------------------------------------
		*/
		var matriceLabelStyles = {
			textAlign: 'center',
			marginRight: '20px',
			display: 'block',
			fontSize: 11
		}


		/*
		*--------------------------------------------------
		* BUTTON HANDLER
		*--------------------------------------------------
		*/
		var handlerClose = function (result_id, b, c) {
			if (!this.scope) {
				this.scope = this;
			}
			this.scope.imageWindowKeymap.disable();
			this.scope.imageWindowKeymapLeft.disable();
			this.scope.imageWindowKeymapRight.disable();
			var currentWindow = this.scope.currentWin;
			currentWindow.id = 'garbage_window';
			currentWindow.hide();
			this.images.hide();
			//currentWindow.destroy();
		}
		var handlerNext = function (result_id, b, c) {
			if (this.scope) this.scope.images.next();
			else this.images.next();
		}
		var handlerPrevious = function (result_id, b, c) {
			if (this.scope) this.scope.images.previous();
			else this.images.previous();
		}


		/*
		*--------------------------------------------------
		* BUTTON
		*--------------------------------------------------
		*/
		this.buttonClose = new Ext.Container({
			xtype: 'container',
			frame:false,
			header:false,
			border: false,
			hideBorders: false,
			cls: 'close-btn',
			width: 26,
			scope: this,
			listeners:{
				render: function(container){
					container.el.addListener('click', handlerClose, container);
				},
				scope: this
			}
		});

		this.btnPrevious = new Ext.Container({
			xtype: 'container',
			frame:false,
			header:false,
			border: false,
			hideBorders: false,
			style: {'top':this.currentHeight*0.25},
			cls: 'previous-btn',
			width: 208,
			scope: this,
			listeners:{
				render: function(container){
					container.el.addListener('click', handlerPrevious, container);
				},
				scope: this
			}
		});

		this.btnNext = new Ext.Container({
			xtype: 'container',
			frame:false,
			header:false,
			border: false,
			hideBorders: false,
			style: {'top':this.currentHeight*0.25},
			cls: 'next-btn',
			width: 208,
			scope: this,
			listeners:{
				render: function(container){
					container.el.addListener('click', handlerNext, container);
				},
				scope: this
			}
		});

		/*
		*--------------------------------------------------
		* BUTTON FORM HANDLER
		*--------------------------------------------------
		*/

		/*
		*--------------------------------------------------
		* BUTTON FORM
		*--------------------------------------------------
		*/

		/*
		*--------------------------------------------------
		* DATA FIELD
		*--------------------------------------------------
		*/
		// Images
		this.images = new ImageViewer({
			url: this.url,
			urlImage: this.urlImage,
			urlThumb: this.urlThumb,
			keyImage: this.keyImage,
			keyFormat: this.keyFormat,
			name: 'image',
			height: this.currentHeight-40,
			toolsPosition: 'bottom',
			disabled: false,
			hidden: false,
			addable: false,
			deletable: false,
			printable: false,
			frame: false,
			toolsWidth: 110,
			toolsColumnWidth: 0.144,
			limitWidth: true,
			limitHeight: true,
			parent: this,
			index: 0,
			horizontalAutoScroll: true,
			listeners: {
				change: function(imageViewer, data, container) {
					var myImage = new Image();
					myImage.onload = function() {
						if (this.scope.container.dom && this.scope.container.dom.offsetHeight) {
							//var newWidth = parseInt((this.width / this.height * this.scope.container.dom.offsetHeight));
							var newWidth = parseInt((1024 / 768 * this.scope.container.dom.offsetHeight));
							var oldWIdth = this.scope.container.dom.offsetWidth;

							var newX = this.scope.parent.currentWin.x + ((oldWIdth - newWidth)/2)
							var oldX = this.scope.parent.currentWin.x

							newWidth += 50;

							this.scope.parent.currentWin.setWidth(newWidth);
							this.scope.parent.currentWin.center()
							//this.scope.parent.currentWin.setPosition(newX, this.scope.parent.currentWin.y);

							//this.scope.parent.currentWin.animate({
							//	duration: 100,
							//	to: {
							//		width: newWidth,
							//      x: newX
							//	}
							//});
						}
					};
					myImage.src = data.url;
					myImage.scope = {container: container, parent: this.scope};
				},
				load: function(store, records) {
					if (records.length > 1) {
						this.scope.btnPrevious.show();
						this.scope.btnNext.show();
					}
					else {
						this.scope.btnPrevious.hide();
						this.scope.btnNext.hide();
					}
				},
				scope: this
			}
		})


		/*
		*--------------------------------------------------
		* FRAME SET
		*--------------------------------------------------
		*/

		var panelContainer = new Ext.Container({
			xtype: 'container',
			layout: 'column',
			frame:false,
			header:false,
			border: false,
			hideBorders: false,
			id: 'images_viewer_window_container',
			items: [
				this.images.get()
			]
		});


		/*
		*--------------------------------------------------
		* LISTENERS
		*--------------------------------------------------
		*/
		formListener = {
			'afterrender': function (form) {
				// répliquer le type de formulaire sur la fenêtre
				if (form.ownerCt instanceof Ext.Window) {
					form.ownerCt.formType = this.formType;
				}
			},
			'actioncomplete': function (form, action) {
				if(action.type == 'load') {
					//var data = action.result.data
				}
			}
		}


		/*
		*--------------------------------------------------
		* FORM
		*--------------------------------------------------
		*/
		var oFormPanel = new Ext.form.FormPanel({
			formType: 'dataViewer',
			trackResetOnLoad : true,
			frame:false,
			header:false,
			border: false,
			hideBorders: false,
			bodyStyle:'padding:5px 5px 0',
			items: [
				panelContainer,
				this.btnPrevious,
				this.btnNext,
				this.buttonClose
			],
			listeners: formListener
		});


		/*
		*--------------------------------------------------
		* WINDOWS
		*--------------------------------------------------
		*/
		var windowOptions = {
			items: oFormPanel,
			width: ((this.currentHeight-120)*1.36),
			height: this.currentHeight,
			frame: false,
			plain: false,
			modal: true,
			closable: false,
			border: false,
			shadow: false,
			resizable: false,
			resizeHandles: false,
			monitorResize: false,
			padding: 20,
			id: 'images_viewer_window'
		};
		for (var attrname in config) { windowOptions[attrname] = config[attrname]; }

		this.oWindow = Ext.apply(windowOptions);

		this.imageWindowKeymap = new Ext.KeyMap(Ext.getBody(), [{
			key: Ext.EventObject.ESC,
			defaultEventAction: 'preventDefault',
			scope: this,
			fn: handlerClose
		 }]);

		this.imageWindowKeymapLeft = new Ext.KeyMap(Ext.getBody(), [{
			key: Ext.EventObject.LEFT,
			defaultEventAction: 'preventDefault',
			scope: this,
			fn: handlerPrevious
		 }]);

		this.imageWindowKeymapRight = new Ext.KeyMap(Ext.getBody(), [{
			key: Ext.EventObject.RIGHT,
			defaultEventAction: 'preventDefault',
			scope: this,
			fn: handlerNext
		 }]);


		Ext.EventManager.onWindowResize(function () {
			var window = Ext.get(Ext.query('#images_viewer_window'))
			window.center()
		});
	}

	ImageWindow.prototype.show = function() {
		if (previousImageWindow && previousImageWindow.currentWin && previousImageWindow.currentWin.destroy) {
			previousImageWindow.currentWin.destroy();
		}
		previousImageWindow = this;
		this.currentWin = new Ext.Window(this.oWindow).show();
	};

	return ImageWindow;

})();