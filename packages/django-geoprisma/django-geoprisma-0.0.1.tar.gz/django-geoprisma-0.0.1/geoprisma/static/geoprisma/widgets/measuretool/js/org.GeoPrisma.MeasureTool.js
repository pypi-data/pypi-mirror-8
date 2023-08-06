/**
 * Copyright (c) 2009-2011 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 * 
 * The code of this widget was borrowed from the GXP library at the following
 * version, which was published under the BSD license at that time :
 * 
 * Commit : a56125b1ff578110bc39f4ac76312eab0fc46073
 * Author : Bart Van den Eijnden
 * Date : Wed Mar 23 17:11:55 2011 +0100
 */

/** api: (define)
 *  module = org.GeoPrisma
 *  class = MeasureTool
 */

/** api: (extends)
 *  SplitButton.js
 */
Ext.namespace("org.GeoPrisma");

/** api: constructor
 *  .. class:: MeasureTool(config)
 *
 *    Provides two actions for measuring length and area in metric and english
 *    units.
 */

PathElevation = OpenLayers.Class(OpenLayers.Handler.Path, {
    immediate: false,
    
    /**
     * Method: dblclick 
     * Handle double-clicks.
     * 
     * Parameters:
     * evt - {Event} The browser event
     *
     * Returns: 
     * {Boolean} Allow event propagation
     */
    dblclick: function(evt) {
        this.doubleClick = true;
        return false;
    },

    CLASS_NAME: "PathElevation"
});


org.GeoPrisma.MeasureTool = Ext.extend(Ext.SplitButton, {

    /* i18n */

    /** api: config[tooltip]
     *  ``String``
     *  Text for button tooltip (i18n).
     */
    tooltip: "Measure Tools",

    /** api: config[lengthMenuText]
     *  ``String``
     *  Text for measure length menu item (i18n).
     */
    lengthMenuText: "Length",

    /** api: config[areaMenuText]
     *  ``String``
     *  Text for measure area menu item (i18n).
     */
    areaMenuText: "Area and Perimeter",
    
    /** api: config[areaMenuText]
     *  ``String``
     *  Text for measure area menu item (i18n).
     */
    elevationMenuText: "Calcul de la pente",

    /** api: config[lengthTooltip]
     *  ``String``
     *  Text for measure length action tooltip (i18n).
     */
    lengthTooltip: "Measure length",

    /** api: config[areaTooltip]
     *  ``String``
     *  Text for measure area action tooltip (i18n).
     */
    areaTooltip: "Measure area",
    
    /** api: config[areaTooltip]
     *  ``String``
     *  Text for measure area action tooltip (i18n).
     */
    elevationTooltip: "Mesure de pente",

    /** api: config[perimeterTooltip]
     *  ``String``
     *  Text for measure perimeter action tooltip (i18n).
     */
    perimeterTooltip: "Measure perimeter",
    
    /** api: config[lastSegmentTooltip]
     *  ``String``
     *  Text for measure the last segement action tooltip (i18n).
     */
    lastSegmentTooltip: "Last segment Measure",

    /** api: config[measureTooltip]
     *  ``String``
     *  Text for measure action tooltip (i18n).
     */
    measureTooltip: "Measure",
    
    /**
     * api: config[unitsText]
     * ``Object``
     * texts for units
     */
    unitsText: {
            '50kilometers': '50kilometers',
            '150kilometers': '150kilometers',
            'BenoitChain': 'BenoitChain',
            'BenoitLink': 'BenoitLink',
            'Brealey': 'Brealey',
            'CaGrid': 'CaGrid',
            'CapeFoot': 'CapeFoot',
            'Centimeter': 'Centimètre',
            'ClarkeChain': 'ClarkeChain',
            'ClarkeFoot': 'ClarkeFoot',
            'ClarkeLink': 'ClarkeLink',
            'Decameter': 'decameter',
            'Decimeter': 'dm',
            'Dekameter': 'dekameter',
            'Fathom': 'Fathom',
            'Foot': 'ft',
            'Furlong': 'furlong',
            'GermanMeter': 'GermanMeter',
            'GoldCoastFoot': 'GoldCoastFoot',
            'GunterChain': 'GunterChain',
            'GunterLink': 'GunterLink',
            'Hectometer': 'hectometer',
            'IFoot': 'IFoot',
            'IInch': 'IInch',
            'IMile': 'IMile',
            'IYard': 'IYard',
            'Inch': 'in',
            'IndianFoot': 'IndianFoot',
            'IndianFt37': 'IndianFt37',
            'IndianFt62': 'IndianFt62',
            'IndianFt75': 'IndianFt75',
            'IndianYard': 'IndianYard',
            'IndianYd37': 'IndianYd37',
            'IndianYd62': 'IndianYd62',
            'IndianYd75': 'IndianYd75',
            'IntnlChain': 'IntnlChain',
            'IntnlLink': 'IntnlLink',
            'Kilometer': 'km',
            'Lat-66': 'Lat-66',
            'Lat-83': 'Lat-83',
            'Meter': 'm',
            'MicroInch': 'MicroInch',
            'Mil': 'Mil',
            'Mile': 'mi',
            'Millimeter': 'mm',
            'ModAmFt': 'ModAmFt',
            'NautM': 'NautM',
            'NautM-UK': 'NautM-UK',
            'Perch': 'Perch',
            'Pole': 'Pole',
            'Rod': 'perche',
            'Rood': 'Rood',
            'SearsChain': 'SearsChain',
            'SearsFoot': 'SearsFoot',
            'SearsLink': 'SearsLink',
            'SearsYard': 'SearsYard',
            'Yard': 'verge',
            'ch': 'ch',
            'cm': 'cm',
            'dd': 'dd',
            'degrees': 'degrees',
            'dm': 'dm',
            'fath': 'fath',
            'ft': 'ft',
            'in': 'in',
            'inches': 'in',
            'ind-ch': 'ind-ch',
            'ind-ft': 'ind-ft',
            'ind-yd': 'ind-yd',
            'km': 'km',
            'kmi': 'kmi',
            'link': 'link',
            'm': 'm',
            'mi': 'mi',
            'mm': 'mm',
            'nmi': 'nmi',
            'us-ch': 'us-ch',
            'us-ft': 'us-ft',
            'us-in': 'us-in',
            'us-mi': 'us-mi',
            'us-yd': 'us-yd',
            'yd': 'yd'
        },
    
    /**
     * api: config[areaUnits]
     * ``Object``
     * define units as area only units
     */
    areaUnits: ['Hectometer'],
    
    /**
     * api: config[units]
     * ``Object``
     * select the units or units group to display
     */
    units: [
        'metric',
        'english',
        'Hectometer'
    ],

    /** api: property[hectare]
     *  ``Boolean``
     *  (Deprecated) Add Hectometer to units...
     */
    hectare: false,
    
    /**
     * api: config[units]
     * ``Object``
     * contain units group that you can add as an "unit" to use one of them
     * unit group will use calibration value to show the most suitable unit
     */
    unitsGroup: {
        'metric': ['Kilometer', 'm', 'cm'],
        'english': ['Mile', 'Foot']
    },
    
    /**
     * api: config[calibrationValue]
     * ``Float``
     * used for transition of the units in groups units
     * the system will auto-select the closest superior value to the calibration value
     */
    calibrationValue: 1.00,

    /* API Properties (Mandatory) */ 

    /** api: config[mapPanel]
     *  :class:`GeoExt.MapPanel`
     *  Used to access the :class:`OpenLayers.Map` and calculate the tooltip
     *  position.
     */
    mapPanel: null,

    /** api: config[measureWindow]
     *  :class:`Ext.Window`
     *  Used contain the informative window.
     */
    measureWindow: null,
    
    /** api: config[measureControl]
     *  The measureControl.
     */
    measureControl: null,

    /* API Properties (Optional, with default value) */

    /** api: property[geodesic]
     *  ``Boolean``
     *  Sets the Measure control 'geodesic' property.
     */
    geodesic: false,

    /** api: property[persist]
     *  ``Boolean``
     *  Sets the Measure control 'persist' property.
     */
    persist: true,

    /** api: property[immediate]
     *  ``Boolean``
     *  Sets the Measure control 'immediate' property.
     */
    immediate: true,

    /** api: property[iconCls]
     *  ``String``
     *  Default value of the 'iconCls' property.
     */
    iconCls: "gp-measuretool-icon-measure-length",

    /** api: property[enableToggle]
     *  ``Boolean``
     *  Default value of the 'enableToggle' property.
     */
    enableToggle: true,

    /** api: property[allowDepress]
     *  ``Boolean``
     *  Default value of the 'allowDepress' property.
     */
    allowDepress: false,
    
    /** api: property[showLastSegmentMeasure]
     *  ``Boolean``
     *  Default value of the 'showLastSegmentMeasure' property.
     */
    showLastSegmentMeasure: false,

    /** api: property[tooltipAtCursor]
     *  ``Boolean``
     *  Sets if the tooltip box follow the cursor.
     */
    tooltipAtCursor: true,

    /* Private Properties */

    /** api: property[activeIndex]
     *  ``Integer``
     *  Is set to the current active control index.
     */
    activeIndex: null,
    
    /** api: property[elevation]
     *  ``Boolean``
     *  Sets if the widget display the elevation option in menu
     */
     elevationInMenu: false,
    
    /** api: property[elevation]
     *  ``Boolean``
     *  Sets if the widget is currently used for elevation measure
     */
    elevationMode: false,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        this.addActions();
        
        if (!this.elevationInMenu) {
                this.menu.items.removeAt(this.menu.items.length-1);
        }
        
        
        org.GeoPrisma.MeasureTool.superclass.constructor.apply(this, arguments);
        this.activeIndex = 0;
        this.mapPanel = this.mapPanel || GeoExt.MapPanel.guess();
        this.loadUnitsGroup();
        
        // for hectare DEPRECATED option
        if (this.hectare) {
            this.units.push('Hectometer');
        }
    },
    
    loadUnitsGroup: function() {
        for (unitGroupName in this.unitsGroup) {
            if (this.units.indexOf(unitGroupName) > -1) {
                this.units[this.units.indexOf(unitGroupName)] = this.unitsGroup[unitGroupName];
            }
        }
    },

    /** private: method[initMyContent]
     *  Create and add the items of this widget : a Ext.ux.form.FileUploadField.
     */
    addActions: function() {
        Ext.apply(this, {
            listeners: {
                toggle: function(button, pressed) {
                    // toggleGroup should handle this
                    if(!pressed) {
                        button.menu.items.each(function(i) {
                            i.setChecked(false);
                        });
                    } else {
                        button.menu.get(this.activeIndex).setChecked(true);
                    }
                },
                render: function(button) {
                    // toggleGroup should handle this
                    Ext.ButtonToggleMgr.register(button);
                }
            },
            menu: new Ext.menu.Menu({
                items: [
                    new Ext.menu.CheckItem(
                        new GeoExt.Action({
                            text: this.lengthMenuText,
                            iconCls: "gp-measuretool-icon-measure-length",
                            toggleGroup: this.toggleGroup,
                            group: this.toggleGroup,
                            listeners: {
                                checkchange: function(item, checked) {
                                    this.activeIndex = 0;
                                    this.toggle(checked);
                                    this.measureWindow.init(this);
                                    this.measureWindow.setTitle(this.lengthTooltip);
                                    if (checked) {
                                        this.setIconClass(item.iconCls);
                                        this.elevationMode = false;
                                    }
                                },
                                scope: this
                            },
                            map: this.mapPanel.map,
                            control: this.createMeasureControl(
                                OpenLayers.Handler.Path, this.lengthTooltip, true
                            )
                        })
                    ),
                    new Ext.menu.CheckItem(
                        new GeoExt.Action({
                            text: this.areaMenuText,
                            iconCls: "gp-measuretool-icon-measure-area",
                            toggleGroup: this.toggleGroup,
                            group: this.toggleGroup,
                            allowDepress: false,
                            listeners: {
                                checkchange: function(item, checked) {
                                    this.activeIndex = 1;
                                    this.toggle(checked);
                                    this.measureWindow.init(this);
                                    this.measureWindow.setTitle(this.areaTooltip);
                                    if (checked) {
                                        this.setIconClass(item.iconCls);
                                        this.elevationMode = false;
                                    }
                                },
                                scope: this
                            },
                            map: this.mapPanel.map,
                            control: this.createMeasureControl(
                                OpenLayers.Handler.Polygon, this.areaTooltip, true
                            )
                        })
                    ),
                    new Ext.menu.CheckItem(
                        new GeoExt.Action({
                            text: this.elevationMenuText,
                            iconCls: "pente",
                            toggleGroup: this.toggleGroup,
                            group: this.toggleGroup,
                            listeners: {
                                checkchange: function(item, checked) {
                                    this.activeIndex = 2;
                                    this.first_elev = null;
                                    this.toggle(checked);
                                    this.measureWindow.init(this);
                                    this.measureWindow.setTitle(this.elevationTooltip);
                                    if (checked) {
                                        this.setIconClass(item.iconCls);
                                        this.elevationMode = true;
                                        
                                        var resource = map.getLayersByResource('346');
                        
                                        if (resource.length) {
                                            for (var i=0; i < resource.length; i++) {
                                                var oResource = resource[i];
                                                oResource.setVisibility(true);
                                                }
                                        }
                                    }
                                },
                                scope: this
                            },
                            map: this.mapPanel.map,
                            control: this.createMeasureControl(
                                PathElevation, this.elevationTooltip, false
                            )
                        })
                    )
                   
                ]
            })
        });
    },
    
    
    

    /** private: method[createMeasureControl]
     * :param: handlerType: the :class:`OpenLayers.Handler` for the measurement
     *     operation
     * :param: title: the string label to display alongside results
     *
     * Convenience method for creating a :class:`OpenLayers.Control.Measure`
     * control
     */
    createMeasureControl: function(handlerType, title, immediate) {

        var styleMap = this.getNewStyleMapObject();
        var cleanup = function() {
            if (this.measureWindow) {
                this.measureWindow.hide();
            }  
        };
        
        // convert and format all measure from metric informations
        var compileMeasureString = function (metric, metricUnit, metricOrder, This) {
            var displayMsg = new Array();
            if (This.units) { // add custom units
                for (var i=0 ; i < This.units.length ; i++) {
                    currentUnit = This.units[i];
                    
                    // for simple units
                    if (typeof currentUnit === 'string') {
                        // avoid areaUnits for non-area measure
                        if (This.areaUnits.indexOf(currentUnit) == -1 || metricOrder > 1) {
                            var toUnitRatio = OpenLayers.INCHES_PER_UNIT[metricUnit] /
                                OpenLayers.INCHES_PER_UNIT[currentUnit];
                            if (metricOrder > 1) { 
                                toUnitRatio = Math.pow(toUnitRatio, metricOrder);
                            }
                            var unitValue = metric * toUnitRatio;
                            var dim = (metricOrder > 1 && This.areaUnits.indexOf(currentUnit) == -1) ?
                            '<sup>'+metricOrder+'</sup>' :
                            '';
                            displayMsg.push(unitValue.toFixed(2) + " " + This.unitsText[currentUnit]+dim);
                        }
                    }
                    
                    // for units GROUPS
                    else {
                        // we need to loop to find the best unit (more near and superior than 1)
                        var superiorUnit = null, inferiorUnit = null, superiorValue = null, inferiorValue = null;
                        for (var familyIndex=0 ; familyIndex < currentUnit.length ; familyIndex++) {
                            currentUnitMember = currentUnit[familyIndex];
                            // avoid areaUnits for non-area measure
                            if (This.areaUnits.indexOf(currentUnitMember) == -1 || metricOrder > 1) {
                                // calcul the ratio and value
                                var toUnitRatio = OpenLayers.INCHES_PER_UNIT[metricUnit] /
                                    OpenLayers.INCHES_PER_UNIT[currentUnitMember];
                                if (metricOrder > 1) { 
                                    toUnitRatio = Math.pow(toUnitRatio, metricOrder);
                                }
                                var unitValue = metric * toUnitRatio;
                                // do comparaison
                                if (unitValue >= This.calibrationValue && (!superiorValue || unitValue < superiorValue)) {
                                    superiorValue = unitValue;
                                    superiorUnit = currentUnitMember;
                                }
                                if (unitValue < This.calibrationValue && (!inferiorValue || unitValue > inferiorValue)) {
                                    inferiorValue = unitValue;
                                    inferiorUnit = currentUnitMember;
                                }
                            }
                        }
                        if (!superiorValue) {
                            superiorValue = inferiorValue;
                            superiorUnit = inferiorUnit;
                        }
                        if (superiorValue) {
                            var dim = (metricOrder > 1 && This.areaUnits.indexOf(superiorUnit) == -1) ?
                            '<sup>2</sup>' :
                            '';
                            displayMsg.push(superiorValue.toFixed(2) + " " + This.unitsText[superiorUnit]+dim);
                        }
                    }
                }
            }
            
            return displayMsg;
        };
        
        // Make the text for the measureWindow
        var makeStringElevation = function(first_elev, elevation, longueur_totale) {
            var content = [];
            
            if (longueur_totale > 0) {
                
                deniv = Math.abs(first_elev - elevation);
                pourcent = (deniv / longueur_totale) * 100;
        
                //Presentation
                content.push("Pourcentage de la pente : " + pourcent.toFixed(4) + "%</b><br />");
                content.push("Distance : " + longueur_totale.toFixed(4) + "m</b><br />");
                content.push("Élévation initiale : " + first_elev + "m</b><br />");
                content.push("Élévation finale : " + elevation + "m</b><br />");
            }
            return content.join("");
        };
        
        var click = function(measureData, measureControl, last_point, This) {
                longueur = measureData.measure;
                
                if (This.measureWindow.isVisible()) {
                        This.measureWindow.hide();
                }
                
                var hover = new OpenLayers.Control.WMSGetFeatureInfo({
                     url: layer_url,
                     title: '',
                     map: map,
                     hover: false,
                     layers: [query_layer],
                     vendorParams: {radius: 5},
                     maxFeatures: 1,
                     handlerOptions: {
                         hover: {delay: 100}
                     },
        
                     infoFormat: 'application/vnd.ogc.gml',
                     queryVisible: false,
                     eventListeners: {
                         beforegetfeatureinfo: function(event){
                             OpenLayers.Element.addClass(map.viewPortDiv, "olCursorWait");
                         },
                         getfeatureinfo: function(event) {
                                var response = event.request;
                                var oFormat = new OpenLayers.Format.WMSGetFeatureInfo();
                                var oFeatures = oFormat.read(response.responseXML || response.responseText);
                                if (oFeatures.length > 0) {
                                    oFeature = oFeatures[oFeatures.length-1];
                                    elevation = oFeature.attributes['z_m']
                                    
                                    //S'il n'y a pas de premier point d'enregistré
                                    if (!This.first_elev)
                                    {
                                        This.first_elev = elevation
                                    }
                                    
                                    //Si c'est le dernier point, on affiche la fenêtre
                                    if (last_point) {
                                        if (measureData.units == 'km') {
                                                longueur = longueur * 1000;
                                        }
                                        if (measureData.units == 'cm') {
                                                longueur = longueur / 1000;
                                        }
                                        This.measureWindow.show();
                                        This.measureWindow.update(makeStringElevation(This.first_elev, elevation, longueur));
                                        This.measureWindow.syncShadow();
                                        
                                        geometry = measureControl.handler.getGeometry();
                                        indexLastPoint = geometry.components.length-1;
                                        measureControl.handler.line.geometry.removeComponent(geometry.components[indexLastPoint]);
                                        measureControl.handler.drawFeature();
                                        measureControl.handler.finishGeometry();
                                        This.first_elev = null;
                                    }
                                } else {
                                   //Si c'est le premier point 
                                   if (measureData.geometry.components.length == 2) {
                                       measureControl.handler.cancel();
                                   }
                                   else {
                                       measureControl.handler.undo();
                                   }
                                }
                            measureControl.handler.doubleClick = false
                         }
                     }
                 });
                
                var px = measureControl.handler.lastUp;
                
                //Si c'est le dernier point 
                if (last_point) {
                        indexLastPoint = measureControl.handler.getGeometry().components.length-2;
                        lastPoint = measureControl.handler.getGeometry().components[indexLastPoint];
                        px = map.getPixelFromLonLat(new OpenLayers.LonLat(lastPoint.x, lastPoint.y))
                }
                
                if (px) {
                        //On récupère l'élévation que si c'est le premier ou le dernier point
                        if (measureData.geometry.components.length == 2 || last_point) {
                                hover.request(px);
                        }
                        else {
                                //S'il n'y a pas de premier point d'enregistré
                                if (!This.first_elev) {
                                        measureControl.handler.cancel();
                                }
                        }
               } else {
                        measureControl.handler.cancel();
               }
            };
    
        // Make the text for the measureWindow
        var makeString = function(metricData, This) {
            var content = [];

                // manage first measure, whether it's a 'length' or 'area'
                var metric = metricData.measure;
                var metricUnit = metricData.units;
                
                // print and generate measures informations
                content.push(compileMeasureString(metric, metricUnit, metricData.order, This).join('<br />'));
                
                 //Show if last segment mesure is asked and if there is a segment and if it's a line measure
                if (This.showLastSegmentMeasure && metricData.geometry.components.length > 1 && metricData.geometry.CLASS_NAME.indexOf("LineString") > -1) {
                    
                    //Keep only the last segment in a clone
                    lastSegment = metricData.geometry.clone();
                    while(lastSegment.components.length > 2){
                        lastSegment.removeComponent(lastSegment.components[0])
                    }
                    
                    //Calculate measures with the clone
                    metric = measureControl.getBestLength(lastSegment);
                    metricUnit = metric[1];
                    metric = metric[0];
    
                    //Presentation
                    content.push("<br /><br />");
                    content.push("<b>" + This.lastSegmentTooltip + "</b><br />");
                    // print and generate measures informations
                    content.push(compileMeasureString(metric, metricUnit, 1, This).join('<br />'));
                }
                
                // manage a second custom measure if 'area' : perimeter
                if (metricData.geometry.CLASS_NAME.indexOf("LineString") == -1) {
                    metric = measureControl.getBestLength(metricData.geometry);
                    metricUnit = metric[1];
                    metric = metric[0];
    
                    //Presentation
                    content.push("<br /><br />");
                    content.push("<b>" + This.perimeterTooltip + "</b><br />");
                    // print and generate measures informations
                    content.push(compileMeasureString(metric, metricUnit, 1, This).join('<br />'));
                }
                
            return content.join("");
        };

        // declaration of the popup that will display informations about measure
        this.measureWindow = new Ext.Window({
            target: Ext.getBody(),
            html: '',
            title: title,
            autoHide: false,
            closable: true, 
            closeAction: 'hide',
            draggable: true,
            border: false,
            resizable: false,
            constrain: true,
            width: 200, 
            showDelay: 1,
            monitorResize: true,
            listeners: {
                hide: function() {
                    //this line cause error and it don't seem to have any utility
                    //measureControl.cancel();
                    cleanup();
                }
            },
            init: function(measureTool) {
                // Display tooltip at right top corner
                if(measureTool.tooltipAtCursor == false) {
                    var p0 = measureTool.mapPanel.getPosition();
                    var s0 = measureTool.mapPanel.getSize();
                    
                    this.setPosition([p0[0]+s0.width-this.width-5, p0[1]+36]);
                }
                
                if (measureTool.elevationInMenu) {
                        query_layer = map.getLayersByResource('346')[0];
                        layer_url = query_layer.url;
                        layer_url = ((layer_url instanceof Array )?layer_url[0]:layer_url);
                }
            },
            renderTo: this.mapPanel.getEl()
        });
        
        // The measure draw tools
        var measureControl = new OpenLayers.Control.Measure(handlerType, {
            geodesic: this.geodesic,
            persist: this.persist,
            immediate: immediate,
            handlerOptions: {layerOptions: {styleMap: styleMap}},
            eventListeners: {
                measurepartial: function(event) {
                        if (this.elevationMode) {
                                click(event, measureControl, measureControl.handler.doubleClick, this); 
                        }
                        else {
                                if(event.measure > 0) {
                                    this.measureWindow.show();
                                    
                                    // Update window text
                                    this.measureWindow.update(makeString(event, this));
                                    
                                    // Display tooltip at cursor
                                    if(this.tooltipAtCursor == true) {
                                        var px = measureControl.handler.lastUp;
                                        var p0 = this.mapPanel.getPosition();
                                        if (px) {
                                            this.measureWindow.setPosition([p0[0]+px.x-50, p0[1]+px.y+40]);
                                        }
                                    }
                                }
                                else {
                                    this.measureWindow.hide();
                                }
                        }
                },
                measure: function(event) {
                        if (!this.elevationMode) {
                                // Update window text
                                this.measureWindow.update(makeString(event, this));
                                
                                // Display tooltip at cursor
                                if (this.tooltipAtCursor == true) {
                                    Ext.getBody().on("mousemove", function(e) {
                                        var px = e.getXY()
                                        var p0 = this.mapPanel.getPosition();
                                        this.measureWindow.setPosition([px[0], px[1]]);
                                    }, this, {single: true});
                                }
                        }
                },
                deactivate: cleanup,
                scope: this
            }
        });

        return measureControl;
    },

    /** private: method[getNewStyleMapObject]
     * :return: :class:`OpenLayers.StyleMap` Used by the measure control layer.
     */
    getNewStyleMapObject: function() {
        return new OpenLayers.StyleMap({
            "default": new OpenLayers.Style(null, {
                rules: [new OpenLayers.Rule({
                    symbolizer: {
                        "Point": {
                            pointRadius: 4,
                            graphicName: "square",
                            fillColor: "white",
                            fillOpacity: 1,
                            strokeWidth: 1,
                            strokeOpacity: 1,
                            strokeColor: "#333333"
                        },
                        "Line": {
                            strokeWidth: 3,
                            strokeOpacity: 1,
                            strokeColor: "#666666",
                            strokeDashstyle: "dash"
                        },
                        "Polygon": {
                            strokeWidth: 2,
                            strokeOpacity: 1,
                            strokeColor: "#666666",
                            fillColor: "white",
                            fillOpacity: 0.3
                        }
                    }
                })]
            })
        });
    }
});