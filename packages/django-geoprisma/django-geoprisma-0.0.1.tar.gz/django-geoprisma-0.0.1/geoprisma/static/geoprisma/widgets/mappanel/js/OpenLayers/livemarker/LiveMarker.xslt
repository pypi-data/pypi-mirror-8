<?xml version="1.0" encoding="utf-8"?>
<!-- 
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license.
 --> 
<xsl:stylesheet version="1.0" xmlns:php="http://php.net/xsl"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:dyn="http://exslt.org/dynamic"
    xmlns:livemarker="http://geoprisma.org/livemarker"
    extension-element-prefixes="dyn">

  <xsl:output method="html" indent="yes" encoding="utf-8" omit-xml-declaration="yes"/>
  <xsl:namespace-alias stylesheet-prefix="php" result-prefix="xsl" />

  <!-- printWidgetSource START  -->
  <xsl:template name="livemarker:printWidgetSource">
    <script>
        <xsl:attribute name="src" >
             <xsl:value-of select="$g_widgets_url"/>
             <xsl:text>/livemarker/LiveMarker.js</xsl:text>
        </xsl:attribute>    
    </script>

    <link rel="stylesheet" type="text/css" >
        <xsl:attribute name="href" >
             <xsl:value-of select="$g_widgets_url"/>
             <xsl:text>/livemarker/LiveMarker.css</xsl:text>
        </xsl:attribute>
    </link>
   </xsl:template>
  <!-- printWidgetSource END  -->

  <!-- printWidgetExecution START  -->
  <xsl:template name="livemarker:printWidgetExecution">
    <xsl:param name="pWidgetName" />
    <xsl:param name="pMapName" />

    <!-- get draw mode  -->
    <xsl:variable name="pDrawMode">
      <xsl:value-of select="$drawmode" />
    </xsl:variable>

    <script type="text/javascript">
	// Find the widget service and resource
	var service, resource;
	<xsl:for-each select="//datastores/datastore/params[./widgettype='livemarker']">
		service = "<xsl:value-of select="../service" />";
		<xsl:variable name="datastore"><xsl:value-of select="../name" /></xsl:variable> 
		<xsl:for-each select="//resources/resource/datastores[./datastore=$datastore]">
			resource = "<xsl:value-of select="../name" />";
		</xsl:for-each>
	</xsl:for-each>
	
     var objGPWidget<xsl:value-of select="$pWidgetName" /> = new OpenLayers.Control.LiveMarker(
		{
			map: oMap,
			icon: "<xsl:value-of select='./options/icon'/>",
			selectedicon: "<xsl:value-of select='./options/selectedicon'/>",
			rate: <xsl:value-of select='./options/rate'/>,
			service: service,
			resource: resource,
			template: "<xsl:value-of select='./options/template'/>"
		});
	objGPWidget<xsl:value-of select="$pWidgetName" />.init();
    </script>
  </xsl:template>
  <!-- printWidgetExecution END  -->

  <!-- drawWidget START  -->
  <xsl:template name="livemarker:drawWidget">
    <xsl:param name="pWidgetName" />
      objGPWidget<xsl:value-of select="$pWidgetName" />
  </xsl:template>
  <!-- drawWidget END  -->

  <!-- 
       Method: drawWidgets
         Add the objGPWidget<WidgetType>Container object to an other given
         container

       Properties:
         pContainer - objGPWidget<WidgetType>Container is added to this object
         WidgetType - The widget type
    -->
<!--
    Function: getWidgetDepedencies

    Return the list of dependencies for this widget
-->
  <!-- Call for each widget type-->
  <xsl:template name="livemarker:getWidgetDepedencies">

  </xsl:template>

</xsl:stylesheet>
