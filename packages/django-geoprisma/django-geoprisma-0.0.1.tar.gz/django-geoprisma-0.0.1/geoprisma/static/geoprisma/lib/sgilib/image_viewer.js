var ImageViewer;

ImageViewer = (function() {

	function ImageViewer(config) {
		this.name = config.name;


		// bouton d'impression
		this.printable = true;
		if (config.printable === true || config.printable === false)
			this.printable = config.printable;

		// bouton de suppression
		this.deletable = false;
		if (config.deletable === true || config.deletable === false)
			this.deletable = config.deletable;

		// bouton d'ajout
		this.addable = false;
		if (config.addable === true || config.addable === false)
			this.addable = config.addable;


		// adresse du store
		this.url = null;
		this.urlGet = null;
		if (config.url) {
			this.url = config.url;
			this.urlGet = config.url+'&REQUEST=get';
		}


		// hauteur
		this.height = 314;
		if (config.height)
			this.height = config.height-60;

		// hauteur
		this.heightFix = 0;
		if (config.heightFix)
			this.heightFix = config.heightFix;

		// limit image height
		this.limitWidth = true
		if (config.limitWidth === true || config.limitWidth === false)
			this.limitWidth = config.limitWidth;

		// limit image height
		this.limitHeight = true
		if (config.limitHeight === true || config.limitHeight === false)
			this.limitHeight = config.limitHeight;

		// Titre preview panel
		this.previewTitle = 'Vue de l\'image';
		if (config.previewTitle)
			this.previewTitle = config.previewTitle;

		// Titre Browser panel
		this.browserTitle = 'Images disponibles';
		if (config.browserTitle)
			this.browserTitle = config.browserTitle;

		// cachée
		this.browserHidden = false;
		if (config.browserHidden === true || config.browserHidden === false)
			this.browserHidden = config.browserHidden;

		// Empty message
		this.emptyText = 'Aucun document à afficher.';
		if (config.emptyText)
			this.emptyText = config.emptyText;

		// Empty message
		this.emptyHtml = '<div class="empty-error">'+this.emptyText+'</div>';
		if (config.emptyHtml)
			this.browserTitle = config.emptyHtml;

		// Remove frame
		this.frame = true;
		if (config.frame === true || config.frame === false)
			this.frame = config.frame;

		if (!this.frame) {
			this.previewTitle = null;
			this.browserTitle = null;
			this.height += 40
		}

		// animation
		// choice animation type in 'fade', 'slide', 'animate'
		// you can disable animation using false or none instead of animation name
		this.animation = 'fade'
		if (config.animation)
			this.animation = config.animation;

		// customize animations parameters
		this.animationOptionsIn = {duration: 1}
		this.animationOptionsOut = {duration: 1}
		if (config.animationOptions)
			this.animationOptionsIn = config.animationOptions;
			this.animationOptionsOut = config.animationOptions;
		if (config.animationOptionsIn)
			this.animationOptionsIn = config.animationOptionsIn;
		if (config.animationOptionsOut)
			this.animationOptionsOut = config.animationOptionsOut;

		// it's the direction for animation 'slide'
		this.animationAnchorIn = 'b'
		this.animationAnchorOut = 't'
		if (config.animationAnchor)
			this.animationAnchorIn = config.animationAnchor;
			this.animationAnchorOut = config.animationAnchor;
		if (config.animationAnchorIn)
			this.animationAnchorIn = config.animationAnchorIn;
		if (config.animationAnchorOut)
			this.animationAnchorOut = config.animationAnchorOut;

		// setup an horizontal auto scroll slideshow view
		this.horizontalAutoScroll = false;
		if (config.horizontalAutoScroll === true || config.horizontalAutoScroll === false)
			this.horizontalAutoScroll = config.horizontalAutoScroll;

		// to change animation duration when thumbnail bar autoscroll
		this.horizontalAutoScrollDuration = 0.5;
		if (config.horizontalAutoScrollDuration)
			this.horizontalAutoScrollDuration = config.horizontalAutoScrollDuration;

		// incremented to the max autoscroll offset to ajust the value
		this.horizontalAutoScrollOffset = 35;
		if (config.horizontalAutoScrollOffset)
			this.horizontalAutoScrollOffset = config.horizontalAutoScrollOffset;

		// same that previous param but mutltiplied by the number of thumbs
		this.horizontalAutoScrollThumbOffset = 3;
		if (config.horizontalAutoScrollThumbOffset)
			this.horizontalAutoScrollThumbOffset = config.horizontalAutoScrollThumbOffset;

		// non disponible
		this.disabled = false;
		if (config.disabled === true || config.disabled === false)
			this.disabled = config.disabled;

		// cachée
		this.hidden = false;
		if (config.hidden === true || config.hidden === false)
			this.hidden = config.hidden;

		// toolsPosition
		this.toolsPosition = 'bottom';
		if (config.toolsPosition)
			this.toolsPosition = config.toolsPosition;

		this.toolsVertical = false;
		if (this.toolsPosition == 'right' || this.toolsPosition == 'left')
			this.toolsVertical = true;
		else if (!this.browserHidden) {
			this.height -= 88;
		}

		// toolsButtonWidth
		this.toolsWidth = 100;
		if (config.toolsWidth)
			this.toolsWidth = config.toolsWidth;

		// toolsButtonWidth
		this.toolsColumnWidth = 0.22;
		if (config.toolsColumnWidth)
			this.toolsColumnWidth = config.toolsColumnWidth;

		// Zoom control
		this.zoomControl = true
		if (config.zoomControl === true || config.zoomControl === false)
			this.zoomControl = config.zoomControl;

		// Zoom control
		this.zoomControlIconSize = 32
		if (config.zoomControlIconSize)
			this.zoomControlIconSize = config.zoomControlIconSize;

		// Zoom control
		this.zoomControlIconVerticalPosition = 'top'
		if (config.zoomControlIconVerticalPosition)
			this.zoomControlIconVerticalPosition = config.zoomControlIconVerticalPosition;

		// Zoom control
		this.zoomControlIconHorizontalPosition = 'left'
		if (config.zoomControlIconHorizontalPosition)
			this.zoomControlIconHorizontalPosition = config.zoomControlIconHorizontalPosition;

		// Zoom control
		this.zoomAmount = 1.5;
		if (config.zoomAmount)
			this.zoomAmount = config.zoomAmount;

		// Zoom control
		this.zoomAnimationDuration = 0.25;
		if (config.zoomAnimationDuration)
			this.zoomAnimationDuration = config.zoomAnimationDuration;

		// Draggable
		this.draggable = true
		if (config.draggable === true || config.draggable === false)
			this.draggable = config.draggable;

		// input
		this.radioInput = false;
		if (config.radioInput)
			this.radioInput = config.radioInput;

		// define parent (usefull for to make some interaction with event listeners)
		this.parent = null
		if (config.parent)
			this.parent = config.parent;

		// event listeners
		// change = when selection change
		// load = when store is loaded
		// uploadSuccess - fired after upload success
		// uploadFailure - fired after upload failure
		this.listeners = {}
		if (config.listeners)
			this.listeners = config.listeners;


		// URL of the folder that contain images
		// can also be used to define a url that will receive a parameter
		this.urlImage = null;
		this.urlThumb = null;
		if (config.urlImage) {
			this.urlImage = config.urlImage;
			this.urlThumb = config.urlImage;
			this.urlPrint = config.urlImage;
		}
		if (config.urlThumb)
			this.urlThumb = config.urlThumb;
		if (config.urlPrint)
			this.urlPrint = config.urlPrint;


		// field to use for the image filename
		// IMPORTANT NOTE : can also be used to define an ID field to pass it as parameter
		// if you see 'id' AS 'keyImage' or 'keyThumb' it's because the widget use
		// a dynamic image
		//
		// this is the available sintax container exemples
		// urlImage                   +     keyImage
		// http://www.site.com/   	  +     fileName (exemple : image.jpg)
		// http://www.site.com/?id=   +     id (exemple : 5)
		//
		// urlImage and urlThumb are a constant path
		// keyImage and keyThumb are the end part of the link and will search the entry in the store
		this.keyImage = null;
		this.keyThumb = null;
		this.keyFormat = null;
		if (config.keyImage) {
			this.keyImage = config.keyImage;
			this.keyThumb = config.keyImage;
			this.keyFormat = config.keyFormat;
		}
		if (config.keyThumb)
			this.keyThumb = config.keyThumb;


		// Key format allow to include a specific key that will be used for pdf detection
		// When the column is equal or if the column contain the word "pdf" this current element
		// will be loaded in an iframe tag and not an img tag
		if (config.keyFormat)
			this.keyFormat = config.keyFormat;


		// value
		this.value = null;
		if (config.value || config.value === 0)
			this.value = config.value;

		// index
		this.index = null;
		if (config.index || config.index === 0)
			this.index = config.index;


		this.lastUrl;


		// show error messages
		this.showErrors = true;
		if (config.showErrors === true || config.showErrors === false)
			this.showErrors = config.showErrors;

		/*
		*--------------------------------------------------
		* STORES
		*--------------------------------------------------
		*/

		this.documentStore = new Ext.data.JsonStore({
			autoLoad: false,
			root: 'data',
			idProperty: 'id',
			totalProperty: 'totalCount',
			remoteSort:false,
			scope: this,
			fields: ['type',
				{ name: 'name', mapping: 'id' },
				{ name: 'file_name', mapping: this.keyImage },
				{ name: 'file_name_thumb', mapping: this.keyThumb },
				{ name: 'url', mapping: 'url' },
				{ name: 'thumb_url', mapping: 'thumb_url' },
				{ name: 'print_url', mapping: 'print_url' },
				{ name: 'path', mapping: 'path_document' },
				{ name: 'params', mapping: 'params' },
				{ name: 'type'}
			]
		});
		if (config.data) {
			this.documentStore.loadData(config.data);
		}



		this.tempStore = new Ext.data.JsonStore({
			autoLoad: false,
			root: 'data',
			idProperty: 'id',
			totalProperty: 'totalCount',
			remoteSort:true,
			baseParams: {
				sort: 'id',
				dir: 'ASC'
			},
			scope: this,
			url: this.urlGet,
			fields: ['id',
				{ name: 'file_name', mapping: this.keyImage },
				{ name: 'file_name_thumb', mapping: this.keyThumb },
				{ name: 'type', mapping: this.keyFormat }
			]
		});
		this.tempStore.on("load", function(store, records) {
			var scope = this;
			if (this.keyImage) {
				this.documentStore.removeAll();
				store.each( function(record) {

					// find file type
					if (record.get('type').indexOf('pdf') > -1 || record.get('type').indexOf('swf') > -1 || record.get('type').indexOf('.htm') > -1) {
						record.set('url', scope.urlImage + record.get('file_name'));
						record.set('thumb_url', 'images/thumb_pdf.png');
						record.set('print_url', scope.urlImage + record.get('file_name'));
						record.set('type', 'iframe');
					}
					else {
						record.set('url', scope.urlImage + record.get('file_name'));
						record.set('thumb_url', scope.urlThumb + record.get('file_name_thumb'));
						record.set('print_url', scope.urlPrint + record.get('file_name'));
						record.set('type', 'img');
					}

				});
				this.documentStore.add(records);
			}

			// ajust value
			if (this.index || this.index === 0) {
				this.setIndex(this.index, this.index)
			}
			if (this.value || this.value === 0) {
				this.setValue(this.value)
			}

			// uploadSuccess event listener
			if (this.listeners.load) {
				this.listeners.load(store, records);
			}
		}, this);
		this.load();


		/*
		*--------------------------------------------------
		* WINDOW - UPLOAD IMG
		*--------------------------------------------------
		*/
		this.uploadHandlerSave = function (button, event) {
			button.setDisabled(true);

			this.uploadForm.getForm().submit({
				url: this.url,
				params:{
					REQUEST: 'put',
					type: '',
					session_id: getCookie('PHPSESSID')
				},
				success: function(form, action) {
					button.setDisabled(false);
					this.uploadWindow.hide();
					this.load();
					// uploadSuccess event listener
					if (this.listeners.uploadSuccess) {
						this.listeners.uploadSuccess(form, action);
					}
					return true;
				},
				failure: function(form, action) {
					button.setDisabled(false);
					// uploadFailure event listener
					if (this.listeners.uploadFailure) {
						this.listeners.uploadFailure(form, action);
					}
					if (this.showErrors) {
						httprequestError(action);
					}
					return false;
				},
				scope : this,
				clientValidation: false
			});

		}

		this.uploadHandlerCancel = function (button ,event) {
			button.findParentByType(Ext.Window).hide();
		}

		this.uploadButtonSave = new Ext.Button({
			text: 'Sauvegarder',
			iconCls: 'ValidateFT',
			handler: this.uploadHandlerSave,
			scope: this
		});

		this.uploadButtonCancel = new Ext.Button({
			text: 'Annuler',
			iconCls: 'CancelFT',
			handler: this.uploadHandlerCancel,
			scope: this
		});

		var uploadField = new Ext.form.Field({
			name: 'image',
			inputType: "file",
			width: '99%',
			fieldLabel: 'Image'
		});

		this.uploadForm = new Ext.form.FormPanel({
			formType: 'dataForm',
			url: this.url,
			requestAction: 'put',
			trackResetOnLoad : true,
			frame:true,
			bodyStyle:'padding:5px 5px 0',
			fileUpload: true,
			labelWidth: 50,
			items: [
				uploadField
			],
			buttons: [
				this.uploadButtonCancel,
				this.uploadButtonSave
			]
		});

		this.uploadWindow = new Ext.Window({
			title: 'Envoyer une nouvelle image',
			layout: 'fit',
			closable : true,
			border : false,
			modal: true,
			plain    : true,
			resizable : false,
			autoScroll: true,
			constrain: true,
			region: 'center',
			closeAction: 'hide',
			width: 300,
			height: 135,
			items: [
				this.uploadForm
			]
		});


		/*
		*--------------------------------------------------
		* HANDLER
		*--------------------------------------------------
		*/
		this.handlerPrint = function(){
			var imageToDelete = this.imageBrowser.getSelectedRecords();
			imagePrintUrl = imageToDelete[0].data.print_url;
			if(imagePrintUrl){
				popup = window.open(imagePrintUrl);
			}
		}

		this.handlerDelete = function (button ,event) {
			if (confirm('Voulez-vous vraiment supprimer l\'image ?')) {
				var imageToDelete = this.imageBrowser.getSelectedRecords();
				imageToDelete = imageToDelete[0].id;

				Ext.Ajax.request({ // faire la requête de suppression en ajax
					url: this.url,
					params:{
						id: imageToDelete,
						REQUEST: 'delete',
						type: '',
						session_id: getCookie('PHPSESSID')
					},
					success: function(record) {
						this.load();
						return true;
					},
					failure: function(record) {
						return false;
					},
					scope: this
				})
			}
		}

		this.handlerAdd = function(){
			this.uploadWindow.show();
		}


		/*
		*--------------------------------------------------
		* BUTTON
		*--------------------------------------------------
		*/
		this.buttonPrint = new Ext.Button({
			width: this.toolsWidth,
			text: 'Imprimer',
			iconCls: 'PrintFT',
			disabled: true,
			style: 'margin-bottom:10px;',
			handler: this.handlerPrint,
			hidden: (!this.printable),
			scope: this
		});

		this.buttonDelete = new Ext.Button({
			width: this.toolsWidth,
			text: 'Supprimer',
			iconCls: 'EraseFT',
			disabled: true,
			handler: this.handlerDelete,
			hidden: (!this.deletable),
			scope: this
		});

		this.buttonAdd = new Ext.Button({
			width: this.toolsWidth,
			text: 'Ajouter',
			iconCls: 'AddFT',
			disabled: this.disabled,
			style: 'margin-bottom:10px;',
			handler: this.handlerAdd,
			hidden: (!this.addable),
			scope: this
		});

		/*
		*--------------------------------------------------
		* TEMPLATE
		*--------------------------------------------------
		*/
		this.tpl = new Ext.XTemplate(
			//'<div style="margin:0px auto; width:300px;">',
			'<tpl for=".">',
				'<div style="position:relative;">',
				'<div class="thumb-wrap zoom-cursor" id="{name}">',
				'<div class="thumb" style="position:relative;">',
				'<img src="{thumb_url}" title="{name}"></div>',
				'<span class="x-editable">{shortName}</span></div>',
				((this.radioInput)?'<div style="position:relative; width:1px; height:1px; padding:0px; margin:0px; float:left;"><input type="radio" name="'+this.radioInput+'" id="'+this.radioInput+'_{id}" value="{id}" style="position:absolute; top:15px; left:-84px; z-index:5;" /></div>':''),
				'</div>',
			'</tpl>'
			//,'</div>'
		);


		this.tplDetailBroken = new Ext.XTemplate(
		'<div class="details" style="width:100%;">',
				'<tpl for=".">',
		'	<div class="group">',
		'		<div style="width:100%;">',
		'			<div id=imgactions><div onClick="zoomIn()"class="imgzoomin"></div><div onClick="zoomOut()" class="imgzoomout"></div><div onClick="reset_img()" class="imgreset"></div></div>',
		'				<img id="mover_img" src="{url}" />',
		'		</div>',
		'	</div>',
		'	</div>',
				'</tpl>',
		'</div>'
		);

		this.tplDetail = new Ext.XTemplate(
			'<div class="details slideshow-front" style="position:absolute; top:0px; left:0px; width:100%; height:100%; '+((this.limitWidth && this.limitHeight)?'overflow:hidden;':'')+'">',
				'<tpl for=".">',
					'<div style="text-align:center;"><img id="big_image" src="{url}" style="'+((this.limitWidth)?'max-width:100%;':'')+' '+((this.limitHeight)?'max-height:100%;':'')+'" /></div>',
				'</tpl>',
			'</div>',
			'<div class="zoomControl">',
			'<a class="x-action-col-icon" onclick="imageViewerZoom('+this.zoomAmount+', '+this.zoomAnimationDuration+');" '+((this.zoomControl)?'':'style="display:none;"')+'><img src="'+baseUrl+'images/ico/'+this.zoomControlIconSize+'/magnifier_zoom_in.png" width="'+this.zoomControlIconSize+'" height="'+this.zoomControlIconSize+'" alt="Zoom avant" style="position:absolute; '+((this.zoomControlIconVerticalPosition == 'bottom')?'bottom':'top')+':5px; '+((this.zoomControlIconHorizontalPosition == 'right')?'right':'left')+':5px;" />',
			'<a class="x-action-col-icon" onclick="imageViewerZoom(-'+this.zoomAmount+', '+this.zoomAnimationDuration+');" '+((this.zoomControl)?'':'style="display:none;"')+'><img src="'+baseUrl+'images/ico/'+this.zoomControlIconSize+'/magnifier_zoom_out.png" width="'+this.zoomControlIconSize+'" height="'+this.zoomControlIconSize+'" alt="Zoom arrière" style="position:absolute; '+((this.zoomControlIconVerticalPosition == 'bottom')?'bottom':'top')+':5px; '+((this.zoomControlIconHorizontalPosition == 'right')?'right':'left')+':'+(this.zoomControlIconSize+12)+'px;" />',
			'</div>'
		);


		this.tplDetailPDF = new Ext.XTemplate(
			'<div class="details slideshow-front" style="position:absolute; top:0px; left:0px; width:100%; height:100%; overflow:hidden;">',
				'<tpl for=".">',
					'<div style="text-align:center;"><iframe id="big_image" src="{url}" style="width:100%; height:100%; padding:0px; margin:0px; border:0px;" /></div>',
				'</tpl>',
			'</div>'
		);


		/*
		*--------------------------------------------------
		* FRAME SET
		*--------------------------------------------------
		*/
		var panelThumbHeight;
		if (this.toolsVertical) {
			panelThumbHeight = this.height - 36;

			if (this.printable)
				panelThumbHeight -= 32;
			if (this.deletable)
				panelThumbHeight -= 32;
			if (this.addable)
				panelThumbHeight -= 22;
			if (this.printable || this.deletable || this.addable)
				panelThumbHeight -= 14;
		}
		else {
			panelThumbHeight = 88;
		}

		this.imageBrowser = new Ext.DataView({
			hidden: this.browserHidden,
			autoScroll: true,
			store: this.documentStore,
			tpl: this.tpl,
			autoHeight: false,
			height: panelThumbHeight,
			multiSelect: false,
			singleSelect: true,
			disabled: this.disabled,
			overClass: 'x-view-over',
			itemSelector: 'div.thumb-wrap',
			emptyText: this.emptyHtml,
			cls: 'image-browser',
			style: (this.horizontalAutoScroll)?{'white-space': 'nowrap', width: '9999px', position: 'relative', top: '0px', left: '0px'}:{},
			scope: this,

			// plugins: [
			// new Ext.DataView.DragSelector(),
			// ],
			/*
			prepareData: function(data){
				data.shortName = Ext.util.Format.ellipsis(data.name, 15);
				data.sizeString = Ext.util.Format.fileSize(data.size);
				data.dateString = data.lastmod.format("m/d/Y g:i a");
				return data;
			},
			*/
			listeners: {
				/*
				selectionchange: {
					fn: function(dv,nodes){
						var l = nodes.length;
						var s = l != 1 ? 's' : '';
						panelThumb.setTitle('Simple DataView Gallery ('+l+' image'+s+' selected)');
					}
				},
				*/
				selectionchange: {
					fn: function() {
						var selNode = this.scope.imageBrowser.getSelectedRecords();
						var lastDD = null;
						if (selNode[0]) {
							this.scope.buttonPrint.setDisabled(false);
							this.scope.buttonDelete.setDisabled(false);
							selNode[0].data.lasturl = this.lastUrl;
							var veryOldImg = Ext.get(Ext.query('#panelDetail .slideshow-back'));
							veryOldImg.remove();
							var oldImg = Ext.get(Ext.query('#panelDetail .slideshow-front'));
							oldImg.addClass('slideshow-back');
							oldImg.removeClass('slideshow-front');
							Ext.get(Ext.query('#panelDetail .zoomControl')).remove();
							// iframe template
							if(selNode[0].data.type && selNode[0].data.type == 'iframe') {
								this.scope.tplDetailPDF.append(this.scope.panelView.body, selNode[0].data);
							}
							// image template
							else {
								this.scope.tplDetail.append(this.scope.panelView.body, selNode[0].data);

								// draggable behavior
								if (this.scope.draggable) {
									if (lastDD) {
										lastDD.removeFromGroup('group');
										lastDD.unreg();
									}

									var items = Ext.get(Ext.query('#panelDetail .slideshow-front img'))
									items.elements[0].id = items.elements[0].id+'+'+parseInt(Math.random()*999999999);
									if (items.elements[0]) {
										items.elements[0].style.cursor = 'move';
										lastDD = items.elements[0].dd = new Ext.dd.DD(items.elements[0].id, 'group');
									}
								}
							}
							// animation
							if (this.scope.animation == 'fade') {
								Ext.get(Ext.query('#panelDetail .slideshow-back')).fadeOut(this.scope.animationOptionsOut);
								Ext.get(Ext.query('#panelDetail .slideshow-front')).fadeIn(this.scope.animationOptionsIn);
							}
							else if (this.scope.animation == 'slide') {
								Ext.get(Ext.query('#panelDetail .slideshow-back')).slideOut(this.scope.animationAnchorOut, this.scope.animationOptionsOut);
								Ext.get(Ext.query('#panelDetail .slideshow-front')).slideIn(this.scope.animationAnchorIn, this.scope.animationOptionsIn);
							}
							else if (this.scope.animation == 'animate') {
								Ext.get(Ext.query('#panelDetail .slideshow-back')).animate(this.scope.animationOptionsOut);
								Ext.get(Ext.query('#panelDetail .slideshow-front')).animate(this.scope.animationOptionsIn);
							}
							else {
								Ext.get(Ext.query('#panelDetail .slideshow-back')).remove();
							}
							this.lastUrl = selNode[0].data.url;

							// change event listener
							if (this.scope.listeners.change) {
								this.scope.listeners.change(this.scope, selNode[0].data, this.scope.panelView.body);
							}
							this.scope.scroll(selNode[0].store.indexOf(selNode[0]));
						}
						else {
							this.scope.buttonPrint.setDisabled(true);
							this.scope.buttonDelete.setDisabled(true);
						}
					}
				}
			}
		})

		var panelButtonPadding, panelThumbColumnWidth, panelButtonColumnWidth, hideButtonArea, panelThumbHeight, panelColumnWidth;

		if (this.printable || this.deletable || this.addable) {
			panelThumbColumnWidth = 1-this.toolsColumnWidth;
			hideButtonArea = false;
		}
		else {
			panelThumbColumnWidth = 1;
			hideButtonArea = true;
		}

		if (this.toolsVertical) {
			panelButtonPadding = '10px 0 4px 4px';
			panelThumbColumnWidth = 1;
			panelButtonColumnWidth = 1;
			panelThumbHeight = this.height;
			panelColumnWidth = this.toolsColumnWidth;
		}
		else {
			panelButtonPadding = '4px 0 4px 14px';
			panelThumbHeight = 60;
			panelColumnWidth = 1;
			panelButtonColumnWidth = this.toolsColumnWidth;
		}

		this.panelButtons = [
			this.buttonAdd,
			this.buttonPrint,
			this.buttonDelete
		];

		if (!this.browserHidden) {
			this.panelThumb = new Ext.Panel({
				columnWidth: panelColumnWidth,
				frame: this.frame,
				width: '100%',
				height: panelThumbHeight,
				id: 'panelThumb',
				autoHeight: true,
				title: this.browserTitle,
				items: [{
					layout: 'column',
					items: [{
						columnWidth: panelThumbColumnWidth,
						id: 'images-view',
						frame: false,
						width: '100%',
						height: panelThumbHeight,
						autoHeight: true,
						disabled: this.disabled,
						layout: 'auto',
						items: [this.imageBrowser]
					},{
						hidden: hideButtonArea,
						columnWidth: panelButtonColumnWidth,
						style: { padding:panelButtonPadding, 'text-align':'right'},
						items: this.panelButtons
					}]
				}]
			});
		}
		else {
			this.panelThumb = new Ext.Panel({
				hidden: hideButtonArea,
				columnWidth: panelColumnWidth,
				width: '100%',
				height: '22px',
				id: 'panelThumb',
				autoHeight: true,
				items: [{
						layout: 'column',
						items: this.panelButtons
					},
					this.imageBrowser
				]
			});
		}

		if (this.toolsVertical) {
			panelColumnWidth = 1-this.toolsColumnWidth;
		}
		else {
			panelColumnWidth = 1;
		}

		this.panelView = new Ext.Panel({
			columnWidth: panelColumnWidth,
			title: this.previewTitle,
			frame: this.frame,
			width: '100%',
			height: this.height + this.heightFix,
			id: 'panelDetail',
			tpl: this.tplDetail,
			autoScroll: true
		});

		// determine the order of the frame item according the parameter
		if (this.toolsPosition == 'top' || this.toolsPosition == 'left') {
			this.frameFilesItems = [
				this.panelThumb,
				this.panelView
			];
		}
		else {
			this.frameFilesItems = [
				this.panelView,
				this.panelThumb
			];
		}

		// global frame
		this.frameFiles = new Ext.Container({
			layout:'column',
			documentStore: this.documentStore,
			columnWidth: 1,
			frame: false,
			style: { padding:'0px'},
			hidden: this.hidden,
			items: this.frameFilesItems
		});
	}

	// return the selected value
	ImageViewer.prototype.getValue = function() {
		var selNode = this.imageBrowser.getSelectedRecords();
		if (selNode[0]) {
			return selNode[0].data;
		}
		else {
			return {'id':null};
		}
	}

	// select an image by value
	ImageViewer.prototype.setValue = function(newValue) {
		this.imageBrowser.select(this.imageBrowser.store.getById(newValue));
		if (document.getElementById(this.radioInput+'_'+newValue)) {
			document.getElementById(this.radioInput+'_'+newValue).checked = true;
		}
	}

	// select image using an index incrementation
	ImageViewer.prototype.setIndex = function(increment, defaultIndex) {
		var newIndex = defaultIndex;
		if (this.imageBrowser.getSelectedIndexes() && this.imageBrowser.getSelectedIndexes()[0] > -1) {
			newIndex = this.imageBrowser.getSelectedIndexes()[0]+increment
		}
		if (newIndex == -1 || (this.imageBrowser.getStore() && !this.imageBrowser.getStore().data.items[newIndex])) {
			newIndex = defaultIndex;
		}
		this.imageBrowser.select(newIndex);
	}

	// select next image
	ImageViewer.prototype.next = function() {
		this.setIndex(1, 0);
	}

	// select previous image
	ImageViewer.prototype.previous = function() {
		this.setIndex(-1, this.imageBrowser.getStore().data.items.length-1);
	}

	// autoscroll to a specific image index
	ImageViewer.prototype.scroll = function(offset) {
		if (this.horizontalAutoScroll) {
			var maxOffset = this.imageBrowser.getNode(this.imageBrowser.getNodes().length-1).offsetLeft + this.imageBrowser.getNode(this.imageBrowser.getNodes().length-1).offsetWidth + this.horizontalAutoScrollOffset - this.panelThumb.getEl().getWidth() + (this.imageBrowser.getNodes().length * this.horizontalAutoScrollThumbOffset);
			offset = (maxOffset / this.imageBrowser.getNodes().length) * offset;
			if (offset > maxOffset) {
				offset = maxOffset;
			}
			if (offset < 0) {
				offset = 0;
			}
			this.imageBrowser.getEl().animate({left:{to: - offset, unit: 'px'}}, this.horizontalAutoScrollDuration);
		}
	}

	// change action possible
	ImageViewer.prototype.setDeletable = function(state) {
		if (this.deletable && !state) {
			this.buttonDelete.hide();
			if (this.toolsVertical) {
				var heightIncrementation = 32;
				if (!this.printable && !this.addable) {
					heightIncrementation += 14;
				}
				this.imageBrowser.setHeight(this.imageBrowser.height + heightIncrementation);
			}
		}
		else if (!this.deletable && state) {
			this.buttonDelete.show();
			if (this.toolsVertical) {
				var heightIncrementation = 32;
				if (!this.printable && !this.addable) {
					heightIncrementation += 14;
				}
				this.imageBrowser.setHeight(this.imageBrowser.height - heightIncrementation);
			}
		}
		this.deletable = state;
	}
	ImageViewer.prototype.setPrintable = function(state) {
		if (this.printable && !state) {
			this.buttonPrint.hide();
			if (this.toolsVertical) {
				var heightIncrementation = 32;
				if (!this.deletable && !this.addable) {
					heightIncrementation += 14;
				}
				this.imageBrowser.setHeight(this.imageBrowser.height + heightIncrementation);
			}
		}
		else if (!this.printable && state) {
			this.buttonPrint.show();
			if (this.toolsVertical) {
				var heightIncrementation = 32;
				if (!this.printable && !this.addable) {
					heightIncrementation += 14;
				}
				this.imageBrowser.setHeight(this.imageBrowser.height - heightIncrementation);
			}
		}
		this.printable = state;
	}
	ImageViewer.prototype.setAddable = function(state) {
		if (this.addable && !state) {
			this.buttonAdd.hide();
			if (this.toolsVertical) {
				var heightIncrementation = 32;
				if (!this.printable && !this.deletable) {
					heightIncrementation += 14;
				}
				this.imageBrowser.setHeight(this.imageBrowser.height + heightIncrementation);
			}
		}
		else if (!this.addable && state) {
			this.buttonAdd.show();
			if (this.toolsVertical) {
				var heightIncrementation = 32;
				if (!this.printable && !this.deletable) {
					heightIncrementation += 14;
				}
				this.imageBrowser.setHeight(this.imageBrowser.height - heightIncrementation);
			}
		}
		this.addable = state;
	}

	// reload the store
	ImageViewer.prototype.hide = function() {
		this.frameFiles.hide();
	}

	// reload the store
	ImageViewer.prototype.show = function() {
		this.frameFiles.show();
	}

	// reload the store
	ImageViewer.prototype.disable = function() {
		this.frameFiles.disable();
	}

	// reload the store
	ImageViewer.prototype.enable = function() {
		this.frameFiles.enable();
	}

	// reload the store
	ImageViewer.prototype.load = function() {
		if (this.url) {
			this.tempStore.reload();
		}
	}

	// load specifics data
	ImageViewer.prototype.loadData = function(data) {
		this.documentStore.loadData(data);
	}

	// return the image viewer object
	ImageViewer.prototype.get = function(meters) {
		return this.frameFiles;
	};

	return ImageViewer;

})();



function imageViewerZoom(factor, animationDuration) {
	if (factor < 0) {
		factor = 0-factor;
		factor = parseFloat(1 / factor);
	}

	var eimg=Ext.query('#panelDetail .slideshow-front img')[0];

	if(isSet(eimg.style.height) &&  !notEmpty(eimg.style.height)){
		//eimg.style.width=100+'%';
		eimg.style.height=100+'%';
	}
	var h = eimg.style.height;
	var w = eimg.style.width;
	//eimg.style.width=factor+parseInt(w)+"%";
	//eimg.style.height =factor+parseInt(h)+"%";
	var oldPercent = parseInt(eimg.style.height);
	var newPercent = parseInt(factor*parseInt(h));

	if (newPercent < 100) {
		newPercent = 100;
	}

	var oldHeight = eimg.height;
	var oldWidth = eimg.width;
	if (newPercent > 150) {
		var newTop = {by: (oldHeight-(oldHeight*newPercent/oldPercent))/2 , unit:'px'};
		var newLeft = {by: (oldWidth-(oldWidth*newPercent/oldPercent))/2 , unit:'px'}
	}
	else {
		var newTop = {to: 0, unit:'px'};
		var newLeft = {to: 0, unit:'px'};
	}

	Ext.get(Ext.query('#panelDetail .slideshow-front img')).animate(
		// animation control object
		{
			height: {to: newPercent, from: oldPercent, unit: '%'},
			top: newTop,
			left: newLeft
		},
		animationDuration,      // animation duration
		null,      // callback
		'easeOut', // easing method
		'run'      // animation type ('run','color','motion','scroll')
	);
	eimg.style.maxHeight ="none";
	eimg.style.maxWidth ="none";
	//deplace le mover selon le zoom
	//modifier le ratio !!
	//var img=document.getElementById('big_image');
	//img.style.top=(img.offsetTop+Math.floor(-parseInt(factor)*2))+'px';
	//img.style.left=(img.offsetLeft+Math.floor(-parseInt(factor)*1.5))+'px';
}
