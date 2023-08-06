/* 
   Copyright (c) 2009-2012 Boreal - Information Strategies
   Published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/

Ext.namespace("org.GeoPrisma");

/** api: (define)
 *  module = org.GeoPrisma
 *  class = GeoExtToolbar
 */

/** api: constructor
 *  .. class:: GeoExtToolbar
 *  Constructor used to define default controls and actions for the MapPanel
 *  inside a Ext.Toolbar object.
 */
org.GeoPrisma.GeoExtToolbar = Ext.extend(Ext.Toolbar, {
    
    /*
        const: i18n_zoomfull_tooltip
        {String} Tooltip of the zoomfull button        
    */
    i18n_zoomfull_tooltip : "Zoom to maximum extent",         

    /*
        const: i18n_zoomin_tooltip
        {String} Tooltip of the zoomin button        
    */
    i18n_zoomin_tooltip : "Zoom in",
    
    /*
        const: i18n_zoomout_tooltip
        {String} Tooltip of the zoomout button        
    */
    i18n_zoomout_tooltip : "Zoom out",
    
    /*
        const: i18n_pan_tooltip
        {String} Tooltip of the pan button        
    */
    i18n_pan_tooltip : "navigate",
    
    
    /*
        const: i18n_back_tooltip
        {String} Tooltip of the back button        
    */
    i18n_back_tooltip : "previous in history",
    
    /*
        const: i18n_next_tooltip
        {String} Tooltip of the next button        
    */
    i18n_next_tooltip : "next in history",

    /**
     * APIProperty: scrollDelay
     * {Integer} When scrollDelay is set, only one zoom event will be performed
     *           after the delay while the navigation control is active.
     */
    scrollDelay: 100,

    /**
     * APIProperty: controls
     * {Array(String)} List of controls and separators to build the toolbar
     *                 with.
     */
    controls: null,

    /**
     * Property: DEFAULT_CONTROLS
     * {Array(String)} List of default controls and separators to build the
     *                 toolbar with if no controls were defined.
     */
    DEFAULT_CONTROLS: ["ZoomMax", "Separator", "ZoomIn", "ZoomOut", "Pan",
                       "Separator", "History", "Separator"],

    /**
     * Method: initComponent
     * Call by Ext on initialize of the Component
     *  
     * Use to register function on event afterrender
     */
    initComponent: function(){
        org.GeoPrisma.GeoExtToolbar.superclass.initComponent.call(this);
        this.on("afterrender", this.onAfterRender, this);
    },
    
    /**
     * Method: initContent
     * Create default controls for the map and associate each one of them to a
     * GeoExtAction.  
     *
     * The initialisation of QuickTips MUST be made in a Ext.onReady function in
     * order to have tooltips working :
     *     Ext.QuickTips.init();
     *
     * Parameters:
     * map - {OpenLayers.Map} The map object
     */
    initContent : function(map, options) {
        var ctrl, toolbarItems = [], action, actions = {};

        // first, apply the options
        options = options || {};
        OpenLayers.Util.extend(this, options);

        if(this.control) 
        {
            this.controls = [this.control];
        }

        if(!this.controls)
        {
            this.controls = this.DEFAULT_CONTROLS;
        } else if (OpenLayers.Util.indexOf(this.controls, "Pan") == -1) {
            this.controls.push("Pan");
        }

        if(this.controls[this.controls.length-1] != "Separator") {
            this.controls.push("Separator");
        }

        for(var i=0, nLen=this.controls.length; i<nLen; i++)
        {
            action = null;

            switch (this.controls[i].toLowerCase())
            {
              case "separator":
                if(toolbarItems.length > 0 && 
                   toolbarItems[toolbarItems.length-1] != "-") {
                    toolbarItems.push("-");
                }
                break;

              case "zoommax":
                if(actions["max_extent"])
                {
                    break;
                }

                action = new GeoExt.Action({
                    control: new OpenLayers.Control.ZoomToMaxExtent(),
                    map: map,
                    iconCls: 'zoomfull',
                    tooltip: this.i18n_zoomfull_tooltip
                });
                actions["max_extent"] = action;
                toolbarItems.push(action);
                break;

              case "zoomin":
                if(actions["zoomin"])
                {
                    break;
                }

                action = new GeoExt.Action({
                    iconCls: 'zoomin',
                    control: new OpenLayers.Control.ZoomBox(),
                    map: map,
                    // button options
                    toggleGroup: map.id,
                    allowDepress: false,
                    tooltip: this.i18n_zoomin_tooltip,
                    // check item options
                    group: map.id
                });
                actions["zoomin"] = action;
                toolbarItems.push(action);
                break;

              case "zoomout":
                if(actions["zoomout"])
                {
                    break;
                }

                action = new GeoExt.Action({
                    iconCls: 'zoomout',
                    control: new OpenLayers.Control.ZoomBox({"out": true}),
                    map: map,
                    // button options
                    toggleGroup: map.id,
                    allowDepress: false,
                    tooltip: this.i18n_zoomout_tooltip,
                    // check item options
                    group: map.id
                });
                actions["zoomout"] = action;
                toolbarItems.push(action);
                break;

              case "pan":
                if(actions["nav"])
                {
                    break;
                }

                var navOptions = {};
                if(this.scrollDelay) {
                    navOptions = {'mouseWheelOptions': {
                        'interval': this.scrollDelay,
                        'cumulative': false
                    }};
                }
		navOptions['zoomWheelEnabled'] = false;
                action = new GeoExt.Action({
                    iconCls: 'pan',
                    control: new OpenLayers.Control.Navigation(navOptions),
                    map: map,
                    // button options
                    toggleGroup: map.id,
                    allowDepress: false,
                    pressed: true,
                    tooltip: this.i18n_pan_tooltip,
                    // check item options
                    group: map.id,
                    checked: true
                });
                actions["nav"] = action;
                toolbarItems.push(action);
                break;

              case "history":
                if(actions["previous"])
                {
                    break;
                }

                ctrl = new OpenLayers.Control.NavigationHistory();
                map.addControl(ctrl);

                action = new GeoExt.Action({
                    iconCls: 'back',
                    control: ctrl.previous,
                    disabled: true,
                    tooltip: this.i18n_back_tooltip
                });
                actions["previous"] = action;
                toolbarItems.push(action);

                action = new GeoExt.Action({
                    iconCls: 'next',
                    control: ctrl.next,
                    disabled: true,
                    tooltip: this.i18n_next_tooltip
                });
                actions["next"] = action;
                toolbarItems.push(action);
                break;             
            }
        }

        this.add(toolbarItems);
    },
    
    /**
     * Method: onCheckItemClicked
     * Called when a checkItem item of a menu item in the toolbar has been clicked.
     *
     * Unpress all buttons from the toolbar if it has a group and disable its
     * according OpenLayers control.
     */
    onCheckItemClicked : function() {
        var aoItems = this.items.items;

        for(var i=0, len=aoItems.length; i<len; i++){
            oItem = aoItems[i];

            // skip separators, menu and items that don't have a group
            if(!oItem.type || !oItem.baseAction || !oItem.initialConfig.group){
                continue;
            }

            if(oItem.pressed) {
                oItem.toggle();
                oItem.baseAction.control.deactivate();
            }
        }
    },
    
    /**
     * Method: onActionClicked
     * Called when a Action (button) item in the toolbar has been clicked.
     *
     * Uncheck all items from menu items in the toolbar and disable its according
     * OpenLayers control.
     */
    onActionClicked : function() {
        var aoItems = this.items.items;

        for(var i=0, len=aoItems.length; i<len; i++){
            oItem = aoItems[i];

            if(!oItem.menu){
                continue;
            }

            checkItems = oItem.menu.items.items;
            for(var j=0, jlen=checkItems.length; j<jlen; j++){
                checkItem = checkItems[j];

                if(checkItem.checked) {               
                    checkItem.setChecked(false);
                    checkItem.baseAction.control.deactivate();
                }
            }
        }
    },
    
    /**
     * Method: onAfterRender
     * Called after the toolbar has been rendered.
     *
     * Used register events on Buttons and Menu items that share the same group to
     * fix the following bug :
     * 
     * on button clicked : uncheck all menu items and deactivate all according 
     *                     controls.
     * on menu item cliked : unpress all buttons and deactivate all according
     *                       controls.
     *
     * N.B. This function doesn't check if the items actually share the same group,
     * only if it has the property.
     */
    onAfterRender : function() {
        var aoItems = this.items.items;

        menuFound = false;

        for(var i=0, len=aoItems.length; i<len; i++){
            oItem = aoItems[i];
            if(oItem.menu){
                menuFound = true;
                break;
            }
        }

        if(menuFound){
            for(var i=0, len=aoItems.length; i<len; i++){
                oItem = aoItems[i];

                // if item is a separator OR has no group nor menu, skip it
                if(!oItem.type || !(oItem.initialConfig.group || oItem.menu)){
                    continue;
                }

                if(!oItem.baseAction){
                    checkItems = oItem.menu.items.items;
                    for(var j=0, jlen=checkItems.length; j<jlen; j++){
                        checkItem = checkItems[j];
                        checkItem.on(
                            "click",
                            this.onCheckItemClicked,
                            this
                        );
                    }
                } else {
                    oItem.on(
                        "click",
                        this.onActionClicked,
                        this
                    );
                }
            }
        }
    }

});









