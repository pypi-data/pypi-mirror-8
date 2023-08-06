/*
   Copyright (c) 2010- Groupe Nippour, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license.
*/
Ext.namespace('OpenLayers.Control.HTWindow');
OpenLayers.Control.HTWindow = OpenLayers.Class(OpenLayers.Control, {
    type: OpenLayers.Control.TYPE_BUTTON,
    tooltip: '',
    formurl: null,
    formmethod: null,
    windowH: 500,
    windowW: 500,
    windowM: true,
    windowC: false,
    windowIconVisible: false,
    menuIcon: '',
    windowIcon: '',
    windowClosable: true,
    windowBorder: false,
    windowPlain: true,
    windowResizable: false,
    windowAutoScroll: true,
    windowConstrain: true,
    windowLayout: 'fit',
    trigger: function(){
        if (!this.oHTExtWindow || this.oHTExtWindow.isDestroyed){
            this.oHTExtWindow = new Ext.Window({
                id: this.id,
                title: this.text,
                layout: this.windowLayout,
                closable : this.windowClosable,
                width    : this.windowW,
                height   : this.windowH,
                border : this.windowBorder,
                modal: this.windowM,
                iconCls: ((this.windowIconVisible || this.windowIcon)?((this.windowIcon)?this.windowIcon:this.menuIcon):''),
                plain    : this.windowPlain,
                resizable : this.windowResizable,
                autoScroll: this.windowAutoScroll,
                constrain: this.windowConstrain,
                myformurl: this.formurl,
                collapsible: this.windowC,
                items: Ext.isFunction(this.formmethod) ? this.formmethod() : [],
                region: 'center'
            });
        }

        this.oHTExtWindow.show();

        if(this.formurl != null)
        {
            this.oHTExtWindow.load({
                url: ''+this.formurl+'?nocache='+(new Date()).getTime()+'',
                scripts: true
            });
         }
    },
    CLASS_NAME: "OpenLayers.Control.HTWindow"
});
