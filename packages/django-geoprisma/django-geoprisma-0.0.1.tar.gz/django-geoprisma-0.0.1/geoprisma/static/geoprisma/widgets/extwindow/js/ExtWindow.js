/*
   Copyright (c) 2010- Groupe Nippour, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license.
*/
Ext.namespace('OpenLayers.Control.ExtWindow');
OpenLayers.Control.ExtWindow = OpenLayers.Class(OpenLayers.Control, {
    type: OpenLayers.Control.TYPE_BUTTON,
    tooltip: null,
    formurl: null,
    formmethod: null,
    windowH: null,
    windowW: null,
    windowM: null,
    windowC: null,
    windowIconVisible: null,
    menuIcon: null,
    windowIcon: null,
    windowClosable: null,
    windowBorder: null,
    windowPlain: null,
    windowResizable: null,
    windowAutoScroll: null,
    windowConstrain: null,
    windowLayout: null,
    trigger: function(){
        // create the window from method
        if (Ext.isFunction(this.formmethod)) {
            this.oHTExtWindow = this.formmethod();
            this.oHTExtWindow.show();

            //var newWindowOptions = Ext4.apply({});
        }

        if(this.formurl != null)
        {
            this.oHTExtWindow.load({
                url: baseUrl + ''+this.formurl+'?nocache='+(new Date()).getTime()+'',
                scripts: true
            });
         }
    },
    CLASS_NAME: "OpenLayers.Control.ExtWindow"
});