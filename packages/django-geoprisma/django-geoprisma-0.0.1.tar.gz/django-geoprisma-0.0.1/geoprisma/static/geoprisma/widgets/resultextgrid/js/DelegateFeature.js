/* 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 

Ext.namespace('org.GeoPrisma', 'org.GeoPrisma.Delegate');

org.GeoPrisma.Delegate.Feature = OpenLayers.Class(Ext.util.Observable, {  
    
    initialize: function(options) {
        this.addEvents({
                            "onFeatureClick" : true,
                            "onFeaturesClick" : true
                        });        
    }
});

oGPDelegateFeature = new org.GeoPrisma.Delegate.Feature();  

if (window.opener != null && window.opener.onFeatureClick != null)
{
    testCallBack = function(object){
        window.opener.onFeatureClick(object);
    };    
    oGPDelegateFeature.on('onFeatureClick', testCallBack);
}

if (typeof(window.parent) != 'undefined' && typeof(window.parent.onFeatureClick) != 'undefined') 
{
    testCallBack2 = function(object){
        window.parent.onFeatureClick(object);
    };    
    oGPDelegateFeature.on('onFeatureClick', testCallBack2);
}

/*
oGPDelegateFeature.on('onFeatureClick', testCallBack);

function testCallBack(object)
{
    alert('CallBack\n\r\n\rresourcename: '+object.ressourceName+'\n\r\n\rdata: '+ object.data);    
}
*/

/*

Ext.namespace('GeoPrisma', 'GeoPrisma.Delegate');
Employee = function(name){
    this.name = name;
    this.addEvents({
        "test" : true
    });
 }

GeoPrisma.Delegate.Context = Ext.extend(Employee, Ext.util.Observable, {
	m_sJSON : null,
	m_oApplicationObjectCallBack : null,
	m_sEventCallBack : null,
	
	setJSON: function(psJSON) {
		this.m_sJSON = psJSON;
		this.fireEvent("test", "tomate")
	},
	
	getJSON: function() {
		return this.m_sJSON;
    }
});
oGPDelegateContext = new GeoPrisma.Delegate.Context();
    */

// Also works
/*
var Delegate = Ext.extend(Ext.Panel, {
    m_sJSON : null,
	
	setJSON: function(psJSON) {
		this.m_sJSON = psJSON;
    },
	
	getJSON: function() {
		return this.m_sJSON;
    }
});
*/
