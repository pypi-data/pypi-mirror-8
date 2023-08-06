<?xml version="1.0" encoding="utf-8"?>
<!-- 
   Copyright (c) 2010-2011 Mapgears Inc., published under the BSD license.
   See http://geoprisma.org/license for the full text of the license.
 --> 
<xsl:stylesheet version="1.0" xmlns:php="http://php.net/xsl"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:dyn="http://exslt.org/dynamic"
    xmlns:layer="http://geoprisma.org/layer"
    extension-element-prefixes="dyn">

  <xsl:output method="html" indent="yes" encoding="utf-8" omit-xml-declaration="yes"/>
  <xsl:namespace-alias stylesheet-prefix="php" result-prefix="xsl" />

  <!-- printWidgetSource START  -->
  <xsl:template name="layer:printWidgetSource">
    <script>
        <xsl:attribute name="src" >
             <xsl:value-of select="$g_widgets_url"/>
             <xsl:text>/layer/Layer.js</xsl:text>
        </xsl:attribute>    
    </script>
   </xsl:template>
  <!-- printWidgetSource END  -->

  <!-- printWidgetExecution START  -->
  <xsl:template name="layer:printWidgetExecution">
    <xsl:param name="pWidgetName" />
    <xsl:param name="pMapName" />

    <xsl:variable name="WidgetType">
      <xsl:text>layer</xsl:text>
    </xsl:variable>

    <script type="text/javascript">
      var mapPanel = objGPWidgetMapPanel<xsl:value-of select="$pMapName" />;
      var map = mapPanel.map;

      var strURL = "<xsl:value-of select="$proxyurl" />";
      var strURLAliases = "<xsl:value-of select="$g_proxy_url_aliases" />";
      var boolURLAliasesEnabled = (strURLAliases != '');
      var objArrayURLAliases, strSeparator;

      if(boolURLAliasesEnabled) {
          strSeparator = '<xsl:value-of select="$g_url_separator" />';
          objArrayURLAliases = strURLAliases.split(strSeparator);
      } else {
          objArrayURLAliases = [strURL];
      }

      <xsl:variable name="layerName">
        <xsl:value-of select="./name" />
      </xsl:variable>

      <xsl:for-each select="./resources/resource">
        <!-- Resource Name -->
        <xsl:variable name="resourceName">
          <xsl:value-of select="." />
        </xsl:variable>

      <!-- if noLayer resource option is set, then don't create any layer -->
      <xsl:if test="not(/geoprisma/resources/resource[./name = $resourceName]/options/noLayer = 'true')">
        <!-- Resource Title -->
        <xsl:variable name="resourceTitle">
          <xsl:for-each select="/geoprisma/resources/resource[./name = $resourceName]/title">
            <xsl:call-template name="getText" />
          </xsl:for-each>
        </xsl:variable>

        <!-- LayerObjectName -->
        <xsl:variable name="layerObjectName">
          <xsl:choose>
            <xsl:when test="$resourceTitle != ''">
              <xsl:value-of select="$resourceTitle"/>
            </xsl:when>
            <xsl:otherwise>
              "<xsl:value-of select="$resourceName"/>"
            </xsl:otherwise>
          </xsl:choose>
        </xsl:variable>

      <!-- ========== WMS ========== -->
      <xsl:variable name="bAddWMS">
        <xsl:choose>
          <xsl:when test="../../options/servicetype">
            <xsl:choose>
              <xsl:when test="../../options/servicetype = 'wms'">1</xsl:when>
              <xsl:otherwise>0</xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:otherwise>1</xsl:otherwise>
        </xsl:choose>
      </xsl:variable>

      <xsl:if test="$bAddWMS = 1">
        <xsl:variable name="serviceType">
          <xsl:text>wms</xsl:text>
        </xsl:variable>

        <xsl:variable name="serviceName">
          <xsl:call-template name="getDataStoreInfoFromWidget">
            <xsl:with-param name="pWidgetName" select="$pWidgetName" />
            <xsl:with-param name="pServiceType" select="$serviceType" />
            <xsl:with-param name="pNodeName"><xsl:text>service</xsl:text></xsl:with-param>
            <xsl:with-param name="pResourceName" select="$resourceName"/>
          </xsl:call-template>
        </xsl:variable>

        <!-- if no servicename was found, then no need to do anything -->
        <xsl:if test="$serviceName != ''">

          <!-- 'layer' params -->
          <xsl:variable name="layerParams">
            <xsl:call-template name="getDataStoreInfoFromWidget">
              <xsl:with-param name="pWidgetName" select="$pWidgetName" />
              <xsl:with-param name="pServiceType" select="$serviceType" />
              <xsl:with-param name="pNodeName"><xsl:text>params/layers</xsl:text></xsl:with-param>
              <xsl:with-param name="pResourceName" select="$resourceName"/>
            </xsl:call-template>
          </xsl:variable>

          <!-- options -->
          <xsl:call-template name="getOpenLayersOptions" >
            <xsl:with-param name="pWidgetName">
              <xsl:value-of select="$layerName" />
            </xsl:with-param>
          </xsl:call-template>
          objOptions.resources = ['<xsl:value-of select="$resourceName" />'];

          <!-- url -->
          <xsl:call-template name="layer:printLayerURL" >
            <xsl:with-param name="pServiceName">
              <xsl:value-of select="$serviceName" />
            </xsl:with-param>
            <xsl:with-param name="pResourceName">
              <xsl:value-of select="." />
            </xsl:with-param>
          </xsl:call-template>

          <!-- params -->
          <xsl:call-template name="layer:getWMSParams" >
            <xsl:with-param name="pLayerName">
              <xsl:value-of select="$layerName" />
            </xsl:with-param>
            <xsl:with-param name="pServiceName">
              <xsl:value-of select="$serviceName" />
            </xsl:with-param>
            <xsl:with-param name="pLayerParams">
              <xsl:value-of select="$layerParams" />
            </xsl:with-param>
          </xsl:call-template>

          <!-- 'vendor' service option -->
          objOptions.vendor = "<xsl:value-of select="/geoprisma/services/service[./name = $serviceName]/options/vendor" />".toLowerCase();

          var objLayer = new OpenLayers.Layer.WMS(
              <xsl:value-of select="$layerObjectName" />,
              objArrayURLAliases,
              objParams,
              objOptions
          );
          map.addLayer(objLayer);
        </xsl:if>
      </xsl:if>

      <!-- ========== TileCache ========== -->
      <xsl:variable name="bAddTileCache">
        <xsl:choose>
          <xsl:when test="../../options/servicetype">
            <xsl:choose>
              <xsl:when test="../../options/servicetype = 'tilecache'">1</xsl:when>
              <xsl:otherwise>0</xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:otherwise>1</xsl:otherwise>
        </xsl:choose>
      </xsl:variable>

      <xsl:if test="$bAddTileCache = 1">
        <xsl:variable name="serviceType">
          <xsl:text>tilecache</xsl:text>
        </xsl:variable>

        <xsl:variable name="serviceName">
          <xsl:call-template name="getDataStoreInfoFromWidget">
            <xsl:with-param name="pWidgetName" select="$pWidgetName" />
            <xsl:with-param name="pServiceType" select="$serviceType" />
            <xsl:with-param name="pNodeName"><xsl:text>service</xsl:text></xsl:with-param>
            <xsl:with-param name="pResourceName" select="$resourceName"/>
          </xsl:call-template>
        </xsl:variable>

        <!-- if no servicename was found, then no need to do anything -->
        <xsl:if test="$serviceName != ''">

          <!-- Service staticCache (option) -->
          <xsl:variable name="serviceStaticCache">
            <xsl:value-of select="/geoprisma/services/service[./name = $serviceName]/options/staticCache" />
          </xsl:variable>

          <!-- 'layer' params -->
          <xsl:variable name="layerParams">
            <xsl:call-template name="getDataStoreInfoFromWidget">
              <xsl:with-param name="pWidgetName" select="$pWidgetName" />
              <xsl:with-param name="pServiceType" select="$serviceType" />
              <xsl:with-param name="pNodeName"><xsl:text>params/layers</xsl:text></xsl:with-param>
              <xsl:with-param name="pResourceName" select="$resourceName"/>
            </xsl:call-template>
          </xsl:variable>

          <!-- options -->
          <xsl:call-template name="getOpenLayersOptions" >
            <xsl:with-param name="pWidgetName">
              <xsl:value-of select="$layerName" />
            </xsl:with-param>
          </xsl:call-template>
          objOptions.resources = ['<xsl:value-of select="$resourceName" />'];

          <!-- url -->
          <xsl:call-template name="layer:printLayerURL" >
            <xsl:with-param name="pServiceName">
              <xsl:value-of select="$serviceName" />
            </xsl:with-param>
            <xsl:with-param name="pResourceName">
              <xsl:value-of select="." />
            </xsl:with-param>
          </xsl:call-template>

          <xsl:choose>
            <!-- If staticCache, create TileCache layer -->
            <xsl:when test="$serviceStaticCache='true'">
              if (objArrayURLAliases instanceof Array) {
                  for(var key in objArrayURLAliases) {
                      objArrayURLAliases[key] =  OpenLayers.Util.urlAppend(objArrayURLAliases[key], "staticCache=");
                  }
              } else {
                  objArrayURLAliases = OpenLayers.Util.urlAppend(objArrayURLAliases, "staticCache=");
              }
              objLayer = new OpenLayers.Layer.TileCache(
                  <xsl:value-of select="$layerObjectName" />,
                  objArrayURLAliases,
                  "<xsl:value-of select='$layerParams'/>",
                  objOptions
              );
            </xsl:when>
            <!-- If not staticCache, create WMS layer -->
            <xsl:otherwise>
              <!-- params -->
              <xsl:call-template name="layer:getWMSParams" >
                <xsl:with-param name="pLayerName">
                  <xsl:value-of select="$layerName" />
                </xsl:with-param>
                <xsl:with-param name="pServiceName">
                  <xsl:value-of select="$serviceName" />
                </xsl:with-param>
                <xsl:with-param name="pLayerParams">
                  <xsl:value-of select="$layerParams" />
                </xsl:with-param>
              </xsl:call-template>

              objLayer = new OpenLayers.Layer.WMS(
                  <xsl:value-of select="$layerObjectName" />,
                  objArrayURLAliases,
                  objParams,
                  objOptions
              );
            </xsl:otherwise>
          </xsl:choose>
          map.addLayer(objLayer);
        </xsl:if>
      </xsl:if>


      <!-- ========== FeatureServer ========== -->
      <xsl:variable name="bAddFeatureServer">
        <xsl:choose>
          <xsl:when test="../../options/servicetype">
            <xsl:choose>
              <xsl:when test="../../options/servicetype = 'featureserver'">1</xsl:when>
              <xsl:otherwise>0</xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:otherwise>1</xsl:otherwise>
            </xsl:choose>
      </xsl:variable>

      <xsl:if test="$bAddFeatureServer = 1">
        <xsl:variable name="serviceType">
          <xsl:text>featureserver</xsl:text>
        </xsl:variable>

        <xsl:variable name="serviceName">
          <xsl:call-template name="getDataStoreInfoFromWidget">
            <xsl:with-param name="pWidgetName" select="$pWidgetName" />
            <xsl:with-param name="pServiceType" select="$serviceType" />
            <xsl:with-param name="pNodeName"><xsl:text>service</xsl:text></xsl:with-param>
            <xsl:with-param name="pResourceName" select="$resourceName"/>
          </xsl:call-template>
        </xsl:variable>

        <!-- if no servicename was found, then no need to do anything -->
        <xsl:if test="$serviceName != ''">

          <!-- 'layer' params -->
          <xsl:variable name="layerParams">
            <xsl:call-template name="getDataStoreInfoFromWidget">
              <xsl:with-param name="pWidgetName" select="$pWidgetName" />
              <xsl:with-param name="pServiceType" select="$serviceType" />
              <xsl:with-param name="pNodeName"><xsl:text>params/layers</xsl:text></xsl:with-param>
              <xsl:with-param name="pResourceName" select="$resourceName"/>
            </xsl:call-template>
          </xsl:variable>

          <!-- url -->
          <xsl:call-template name="layer:printLayerURL" >
            <xsl:with-param name="pServiceName">
              <xsl:value-of select="$serviceName" />
            </xsl:with-param>
            <xsl:with-param name="pResourceName">
              <xsl:value-of select="." />
            </xsl:with-param>
          </xsl:call-template>
          <![CDATA[
          var aszURLArray = strURL.split("?");
          strURL = aszURLArray[0]+"/]]><xsl:value-of select='$layerParams'/><![CDATA[?"+aszURLArray[1];
          ]]>

          <!-- options -->
          <xsl:call-template name="getOpenLayersOptions" >
            <xsl:with-param name="pWidgetName">
              <xsl:value-of select="$layerName" />
            </xsl:with-param>
          </xsl:call-template>
          objOptions.resources = ['<xsl:value-of select="$resourceName" />'];
          objOptions.strategies.push (new OpenLayers.Strategy.BBOX());
          objOptions.protocol = new OpenLayers.Protocol.HTTP({
              url: strURL,
              params: {
                  format: "GeoJSON",
                  service: "WFS",
                  request: "GetFeatures",
                  srs: objOptions["projection"] ? objOptions["protocol"] : "",
                  maxfeatures: objOptions["maxfeatures"]
              },
              format: new OpenLayers.Format.GeoJSON()
          });

          <!-- STYLEMAP  -->
          <xsl:for-each select="../../options/stylemap">
            objOptions["styleMap"] = new OpenLayers.StyleMap({});

            <!-- STYLES  -->
            <xsl:for-each select="./renderers/renderer">
                objOptions["styleMap"].styles["<xsl:value-of select='./renderintent'/>"] = new OpenLayers.Style(OpenLayers.Util.applyDefaults(
                <xsl:call-template name="layer:getStyleObject">
                  <xsl:with-param name="pStyle" select="./style" />
                </xsl:call-template>, 
                OpenLayers.Feature.Vector.style["<xsl:value-of select='./renderintent'/>"]),
                <xsl:call-template name="layer:getStyleContext">
                  <xsl:with-param name="pStyle" select="./style" />
                </xsl:call-template>);
            </xsl:for-each>

            <!-- UNIQUE VALUE RULES  -->
            <xsl:for-each select='./uniquevaluerules/uniquevaluerule'>
              objSymbolizers = {};

              <xsl:for-each select='./symbolizers/symbolizer'>
                objSymbolizers['<xsl:value-of select='./value'/>'] =   
                <xsl:call-template name="layer:getStyleObject">
                  <xsl:with-param name="pStyle" select="./style" />
                </xsl:call-template>;
              </xsl:for-each>

              <!-- TODO, should support the 4th 'context' parameter some day... -->
              objOptions["styleMap"].addUniqueValueRules(
                '<xsl:value-of select='./renderintent'/>',
                '<xsl:value-of select='./property'/>',
                objSymbolizers);

              <!-- Add an other symbolizer for the features that don't
                   fall under one of the rules created above.  Useful to
                   keep the vertices when editing.  TODO: theses values
                   are currently HARDCODED.
                -->
              rules = [new OpenLayers.Rule({
                  symbolizer: {strokeColor:"red",strokeWidth: 2},
                  elseFilter: true
              })];
              objOptions["styleMap"].styles["<xsl:value-of select='./renderintent'/>"].addRules(rules);
            </xsl:for-each>
          </xsl:for-each>

          objLayer = new OpenLayers.Layer.Vector(
              <xsl:value-of select="$layerObjectName" />,
              objOptions
          );
          map.addLayer(objLayer);
        </xsl:if>
      </xsl:if>
      
      <!-- ========== WFS ========== -->
      <xsl:variable name="bAddWFS">
        <xsl:choose>
          <xsl:when test="../../options/servicetype">
            <xsl:choose>
              <xsl:when test="../../options/servicetype = 'wfs'">1</xsl:when>
              <xsl:otherwise>0</xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:otherwise>1</xsl:otherwise>
            </xsl:choose>
      </xsl:variable>

      <xsl:if test="$bAddWFS = 1">
        <xsl:variable name="serviceType">
          <xsl:text>wfs</xsl:text>
        </xsl:variable>

        <xsl:variable name="serviceName">
          <xsl:call-template name="getDataStoreInfoFromWidget">
            <xsl:with-param name="pWidgetName" select="$pWidgetName" />
            <xsl:with-param name="pServiceType" select="$serviceType" />
            <xsl:with-param name="pNodeName"><xsl:text>service</xsl:text></xsl:with-param>
            <xsl:with-param name="pResourceName" select="$resourceName"/>
          </xsl:call-template>
        </xsl:variable>

        <!-- if no servicename was found, then no need to do anything -->
        <xsl:if test="$serviceName != ''">

          var objProtocolOptions = {};
        
          <!-- 'layer' params -->
          <xsl:variable name="layerParams">
            <xsl:call-template name="getDataStoreInfoFromWidget">
              <xsl:with-param name="pWidgetName" select="$pWidgetName" />
              <xsl:with-param name="pServiceType" select="$serviceType" />
              <xsl:with-param name="pNodeName"><xsl:text>params/layers</xsl:text></xsl:with-param>
              <xsl:with-param name="pResourceName" select="$resourceName"/>
            </xsl:call-template>
          </xsl:variable>

          <!-- 'featureNS' param -->
          <xsl:variable name="featureNS">
            <xsl:call-template name="getDataStoreInfoFromWidget">
              <xsl:with-param name="pWidgetName" select="$pWidgetName" />
              <xsl:with-param name="pServiceType" select="$serviceType" />
              <xsl:with-param name="pNodeName"><xsl:text>params/featureNS</xsl:text></xsl:with-param>
              <xsl:with-param name="pResourceName" select="$resourceName"/>
            </xsl:call-template>
          </xsl:variable>
          
          <!-- 'geometryName' param -->
          <xsl:variable name="geometryName">
            <xsl:call-template name="getDataStoreInfoFromWidget">
              <xsl:with-param name="pWidgetName" select="$pWidgetName" />
              <xsl:with-param name="pServiceType" select="$serviceType" />
              <xsl:with-param name="pNodeName"><xsl:text>params/geometryName</xsl:text></xsl:with-param>
              <xsl:with-param name="pResourceName" select="$resourceName"/>
            </xsl:call-template>
          </xsl:variable>
  
          <!-- url -->
          <xsl:call-template name="layer:printLayerURL" >
            <xsl:with-param name="pServiceName">
              <xsl:value-of select="$serviceName" />
            </xsl:with-param>
            <xsl:with-param name="pResourceName">
              <xsl:value-of select="." />
            </xsl:with-param>
          </xsl:call-template>
          <![CDATA[
          var aszURLArray = strURL.split("?");
          strURL = aszURLArray[0]+"/]]><xsl:value-of select='$layerParams'/><![CDATA[?"+aszURLArray[1];
          ]]>

          <!-- options -->
          <xsl:call-template name="getOpenLayersOptions" >
            <xsl:with-param name="pWidgetName">
              <xsl:value-of select="$layerName" />
            </xsl:with-param>
          </xsl:call-template>
          objOptions.resources = ['<xsl:value-of select="$resourceName" />'];
          objOptions.strategies.push (new OpenLayers.Strategy.BBOX());
          objOptions.protocol = new OpenLayers.Protocol.WFS({
              url: strURL,
              version: objOptions["version"] ? objOptions["version"] : undefined,
              srsName: objOptions["projectionString"] ? objOptions["projectionString"] : undefined,
              featureType: "<xsl:value-of select="$layerParams" />",
              featureNS: objOptions["featureNS"] ? objOptions["featureNS"] : undefined,
              featurePrefix: objOptions["featurePrefix"] ? objOptions["featurePrefix"] : undefined,
              geometryName: objOptions["geometryName"] ? objOptions["geometryName"] : undefined
          });

          <!-- STYLEMAP  -->
          <xsl:for-each select="../../options/stylemap">
            objOptions["styleMap"] = new OpenLayers.StyleMap({});

            <!-- STYLES  -->
            <xsl:for-each select="./renderers/renderer">
                objOptions["styleMap"].styles["<xsl:value-of select='./renderintent'/>"] = new OpenLayers.Style(OpenLayers.Util.applyDefaults(
                <xsl:call-template name="layer:getStyleObject">
                  <xsl:with-param name="pStyle" select="./style" />
                </xsl:call-template>, 
                OpenLayers.Feature.Vector.style["<xsl:value-of select='./renderintent'/>"]),
                <xsl:call-template name="layer:getStyleContext">
                  <xsl:with-param name="pStyle" select="./style" />
                </xsl:call-template>);
            </xsl:for-each>

            <!-- UNIQUE VALUE RULES  -->
            <xsl:for-each select='./uniquevaluerules/uniquevaluerule'>
              objSymbolizers = {};

              <xsl:for-each select='./symbolizers/symbolizer'>
                objSymbolizers['<xsl:value-of select='./value'/>'] =   
                <xsl:call-template name="layer:getStyleObject">
                  <xsl:with-param name="pStyle" select="./style" />
                </xsl:call-template>;
              </xsl:for-each>

              <!-- TODO, should support the 4th 'context' parameter some day... -->
              objOptions["styleMap"].addUniqueValueRules(
                '<xsl:value-of select='./renderintent'/>',
                '<xsl:value-of select='./property'/>',
                objSymbolizers);

              <!-- Add an other symbolizer for the features that don't
                   fall under one of the rules created above.  Useful to
                   keep the vertices when editing.  TODO: theses values
                   are currently HARDCODED.
                -->
              rules = [new OpenLayers.Rule({
                  symbolizer: {strokeColor:"red",strokeWidth: 2},
                  elseFilter: true
              })];
              objOptions["styleMap"].styles["<xsl:value-of select='./renderintent'/>"].addRules(rules);
            </xsl:for-each>
          </xsl:for-each>

          objLayer = new OpenLayers.Layer.Vector(
              <xsl:value-of select="$layerObjectName" />,
              objOptions
          );
          map.addLayer(objLayer);
        </xsl:if>
      </xsl:if>
      

      <!-- ========== GYMO ========== -->
      <xsl:variable name="bAddGYMO">
        <xsl:choose>
          <xsl:when test="../../options/servicetype">
            <xsl:choose>
              <xsl:when test="../../options/servicetype = 'gymo'">1</xsl:when>
              <xsl:otherwise>0</xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:otherwise>1</xsl:otherwise>
        </xsl:choose>
      </xsl:variable>

      <xsl:if test="$bAddGYMO = 1">
        <xsl:variable name="serviceType">
          <xsl:text>gymo</xsl:text>
        </xsl:variable>

        <xsl:variable name="serviceName">
          <xsl:call-template name="getDataStoreInfoFromWidget">
            <xsl:with-param name="pWidgetName" select="$pWidgetName" />
            <xsl:with-param name="pServiceType" select="$serviceType" />
            <xsl:with-param name="pNodeName"><xsl:text>service</xsl:text></xsl:with-param>
            <xsl:with-param name="pResourceName" select="$resourceName"/>
          </xsl:call-template>
        </xsl:variable>

        <!-- if no servicename was found, then no need to do anything -->
        <xsl:if test="$serviceName != ''">
          <!-- provider and source -->
          <xsl:variable name="strGYMOProvider">
            <xsl:value-of select="//services/service[name=$serviceName]/provider" />
          </xsl:variable>
          <xsl:variable name="strGYMOSource">
            <xsl:value-of select="//services/service[name=$serviceName]/source" />
          </xsl:variable>

          <!-- 'layer' params -->
          <xsl:variable name="layerParams">
            <xsl:call-template name="getDataStoreInfoFromWidget">
              <xsl:with-param name="pWidgetName" select="$pWidgetName" />
              <xsl:with-param name="pServiceType" select="$serviceType" />
              <xsl:with-param name="pNodeName"><xsl:text>params/layers</xsl:text></xsl:with-param>
              <xsl:with-param name="pResourceName" select="$resourceName"/>
            </xsl:call-template>
          </xsl:variable>

          <!-- options -->
          <xsl:call-template name="getOpenLayersOptions" >
            <xsl:with-param name="pWidgetName">
              <xsl:value-of select="$layerName" />
            </xsl:with-param>
          </xsl:call-template>
          objOptions.resources = ['<xsl:value-of select="$resourceName" />'];

          <xsl:choose>
            <xsl:when test="$strGYMOProvider='google'">
              <xsl:choose>
                <xsl:when test="$layerParams='satellite'">
                  objOptions['type'] = google.maps.MapTypeId.SATELLITE;
                </xsl:when>
                <xsl:when test="$layerParams='hybrid'">
                  objOptions['type'] = google.maps.MapTypeId.HYBRID;
                </xsl:when>
                <xsl:when test="$layerParams='terrain'">
                  objOptions['type'] = google.maps.MapTypeId.TERRAIN;
                </xsl:when>
                <!-- 'physical' was v2 value for 'terrain' -->
                <xsl:when test="$layerParams='physical'">
                  objOptions['type'] = google.maps.MapTypeId.TERRAIN;
                </xsl:when>
              </xsl:choose>
              objLayer = new OpenLayers.Layer.Google(
                  <xsl:value-of select="$layerObjectName" />,
                  objOptions
              );
            </xsl:when>
            <xsl:when test="$strGYMOProvider='openstreetmap'">
              strURL = "<xsl:value-of select='$strGYMOSource'/>";
              objLayer = new OpenLayers.Layer.OSM(
                  <xsl:value-of select="$layerObjectName" />,
                  strURL,
                  objOptions
              );
            </xsl:when>
            <xsl:when test="$strGYMOProvider='bing'">
              <xsl:choose>
                <xsl:when test="$layerParams='shaded'">
                  objOptions['type'] = VEMapStyle.Shaded;
                </xsl:when>
                <xsl:when test="$layerParams='hybrid'">
                  objOptions['type'] = VEMapStyle.Hybrid;
                </xsl:when>
                <xsl:when test="$layerParams='aerial'">
                  objOptions['type'] = VEMapStyle.Aerial;
                </xsl:when>
              </xsl:choose>
              objLayer = new OpenLayers.Layer.VirtualEarth(
                  <xsl:value-of select="$layerObjectName" />,
                  objOptions
              );
            </xsl:when>
            <xsl:when test="$strGYMOProvider='yahoo'">
              <xsl:choose>
                <xsl:when test="$layerParams='street'">
                </xsl:when>
                <xsl:when test="$layerParams='hybrid'">
                  objOptions['type'] = YAHOO_MAP_HYB;
                </xsl:when>
                <xsl:when test="$layerParams='satellite'">
                  objOptions['type'] = YAHOO_MAP_SAT;
                </xsl:when>
              </xsl:choose>
              objLayer = new OpenLayers.Layer.Yahoo(
                  <xsl:value-of select="$layerObjectName" />,
                  objOptions
              );
            </xsl:when>
          </xsl:choose>
          map.addLayer(objLayer);
        </xsl:if>
      </xsl:if>

      <!-- ========== TMS ========== -->
      <xsl:variable name="bAddTMS">
        <xsl:choose>
          <xsl:when test="../../options/servicetype">
            <xsl:choose>
              <xsl:when test="../../options/servicetype = 'tms'">1</xsl:when>
              <xsl:otherwise>0</xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:otherwise>1</xsl:otherwise>
        </xsl:choose>
      </xsl:variable>

      <xsl:if test="$bAddTMS = 1">
        <xsl:variable name="serviceType">
          <xsl:text>tms</xsl:text>
        </xsl:variable>

        <xsl:variable name="serviceName">
          <xsl:call-template name="getDataStoreInfoFromWidget">
            <xsl:with-param name="pWidgetName" select="$pWidgetName" />
            <xsl:with-param name="pServiceType" select="$serviceType" />
            <xsl:with-param name="pNodeName"><xsl:text>service</xsl:text></xsl:with-param>
            <xsl:with-param name="pResourceName" select="$resourceName"/>
          </xsl:call-template>
        </xsl:variable>

        <!-- if no servicename was found, then no need to do anything -->
        <xsl:if test="$serviceName != ''">
          <!-- 'layer' params -->
          <xsl:variable name="layerParams">
            <xsl:call-template name="getDataStoreInfoFromWidget">
              <xsl:with-param name="pWidgetName" select="$pWidgetName" />
              <xsl:with-param name="pServiceType" select="$serviceType" />
              <xsl:with-param name="pNodeName"><xsl:text>params/layers</xsl:text></xsl:with-param>
              <xsl:with-param name="pResourceName" select="$resourceName"/>
            </xsl:call-template>
          </xsl:variable>

          <!-- options -->
          <xsl:call-template name="getOpenLayersOptions" >
            <xsl:with-param name="pWidgetName">
              <xsl:value-of select="$layerName" />
            </xsl:with-param>
          </xsl:call-template>

          Ext.applyIf(objOptions, {
              resources: ['<xsl:value-of select="$resourceName" />'],
              layername: "<xsl:value-of select='$layerParams'/>",
              type: "png" <!-- default value if not set -->
          });

          <!-- url -->
          <xsl:call-template name="layer:printLayerURL" >
            <xsl:with-param name="pServiceName">
              <xsl:value-of select="$serviceName" />
            </xsl:with-param>
            <xsl:with-param name="pResourceName">
              <xsl:value-of select="." />
            </xsl:with-param>
          </xsl:call-template>

          if (objArrayURLAliases instanceof Array) {
              for(var key in objArrayURLAliases) {
                  objArrayURLAliases[key] =  OpenLayers.Util.urlAppend(objArrayURLAliases[key], "TMSRequest=");
              }
          } else {
              objArrayURLAliases = OpenLayers.Util.urlAppend(objArrayURLAliases, "TMSRequest=");
          }
          objLayer = new OpenLayers.Layer.TMS(
              <xsl:value-of select="$layerObjectName" />,
              objArrayURLAliases,
              objOptions
          );
          map.addLayer(objLayer);
        </xsl:if>
      </xsl:if>

      </xsl:if>
      </xsl:for-each> <!-- end of for-each resource -->


      <!-- ========== Vector (not binded to resources) ========== -->
      <xsl:if test="./options/servicetype = 'vector'">
        // aaaaaa
      </xsl:if>

    </script>

  </xsl:template>
  <!-- printWidgetExecution END  -->


  <xsl:template name="layer:getWMSParams">
    <xsl:param name="pLayerName" />
    <xsl:param name="pServiceName" />
    <xsl:param name="pLayerParams" />

    var objParams = {
        'layers': ['<xsl:value-of select='$pLayerParams'/>']
    };

    <!-- Service version (option) -->
    <xsl:variable name="serviceVersion">
      <xsl:value-of select="/geoprisma/services/service[./name = $pServiceName]/options/version" />
    </xsl:variable>
    <xsl:if test="$serviceVersion != ''">
      objParams["version"] = '<xsl:value-of select="$serviceVersion" />';
      
      <!-- temp fix, related to http://trac.openlayers.org/ticket/2478 -->
      <xsl:if test="$serviceVersion = '1.3.0'">
        objParams["exceptions"] = "INIMAGE";
      </xsl:if>
    </xsl:if>
    
    <xsl:for-each select="/geoprisma/widgets/widget[./name = $pLayerName]/options">
      <xsl:if test='./format'>
        objParams["format"] = "<xsl:value-of select='./format'/>";
      </xsl:if>
      <xsl:if test='./maxfeatures'>
        objParams["maxfeatures"] = "<xsl:value-of select='./maxfeatures'/>";
      </xsl:if>
      <xsl:if test='./transparent'>
        objParams["transparent"] = "<xsl:value-of select='./transparent'/>";
      </xsl:if>
      <xsl:if test='./typename'>
        objParams["typename"] = "<xsl:value-of select='./typename'/>";
      </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="layer:printLayerURL">
    <xsl:param name="pServiceName" />
    <xsl:param name="pResourceName" />
      var objArrayURLParams = [];
      objArrayURLParams.push();

      var objURLParams = {
          'osmservice': '<xsl:value-of select="$pServiceName" />'
      };
      var strParams = OpenLayers.Util.getParameterString(objURLParams);
      <![CDATA[
      strParams += '&osmresource[]=]]><xsl:value-of select="$pResourceName" /><![CDATA[';
      if(strParams.length > 0) {
          var strSeparator = (strURL.indexOf('?') > -1) ? '&' : '?';
          strURL += strSeparator + strParams;
          for(var i=0; i<objArrayURLAliases.length; i++){
              var strSeparator = (objArrayURLAliases[i].indexOf('?') > -1) ? '&' : '?';
              objArrayURLAliases[i] += strSeparator + strParams;
          }
      }
      ]]>
  </xsl:template>

  <!--
    Function: getStyleObject
    Given a <style> node, build a javascript object with "property: 'value',"
    properties.  It can then be used to create OpenLayers.Style() objects or
    defining rules.

    Parameters:
    {node}   - pStyle    A <style> node

    Returns:
    A javascript object ready to create OpenLayers objects, like Style, Rules...
    Example of return :  { strokeOpacity: 1, strokeColor: #ffee22, last: '' }
    -->
  <xsl:template name="layer:getStyleObject">
    <xsl:param name="pStyle" />
    
        {
    <xsl:for-each select='$pStyle/*'>  <!-- Switch to style context - only one -->
           <xsl:if test="position()>1">,</xsl:if>
           <xsl:choose>
                <xsl:when test="name() = 'fillcolor'">fillColor: "#<xsl:value-of select='.'/>"</xsl:when>
                <xsl:when test="name() = 'fillopacity'">fillOpacity: "<xsl:value-of select='.'/>"</xsl:when>
                <!-- pointRadius == manual pointRadius -->
                <xsl:when test="name() = 'pointradius'">pointRadius: "<xsl:value-of select='.'/>"</xsl:when>
                <xsl:when test="name() = 'strokedashstyle'">strokeDashstyle: "<xsl:value-of select='.'/>"</xsl:when>
                <xsl:when test="name() = 'strokelinecap'">strokeLinecap: "<xsl:value-of select='.'/>"</xsl:when>
                <xsl:when test="name() = 'strokeopacity'">strokeOpacity: "<xsl:value-of select='.'/>"</xsl:when>
                <xsl:when test="name() = 'strokewidth'">strokeWidth: "<xsl:value-of select='.'/>"</xsl:when>
                <xsl:when test="name() = 'strokecolor'">strokeColor: "#<xsl:value-of select='.'/>"</xsl:when>
                <!-- radius == automatic pointRadius -->    
                <xsl:when test="name() = 'radius'"> pointRadius: "${radius}"</xsl:when>
                <xsl:otherwise>
                    'bidon' : null  <!-- fix for ie extra ',' -->    
                </xsl:otherwise>
	   </xsl:choose>
     </xsl:for-each>
         }
  </xsl:template>
  
  <xsl:template name="layer:getStyleContext">
    <xsl:param name="pStyle" />
        {   
            context: {
                first: function(feature){return ''}

                <xsl:for-each select='$pStyle'>  <!-- Switch to style context -->
                
                    <xsl:for-each select='context/functions/*'>
                      <xsl:choose>

                        <!-- either attributegualfunction or 
                             fidegualfunction -->
                        <xsl:when test="count(./egual)!=0">
                          <xsl:choose>

                            <!-- attributegualfunction -->
                            <xsl:when test="count(./attribute)!=0">
                                <xsl:variable name="egual">
                                    <xsl:choose>            
                                        <xsl:when test="egual/getValueFrom">
                                            <xsl:for-each select='egual/getValueFrom'><xsl:call-template name="getValueFrom" /></xsl:for-each>    
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select='egual'/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:variable>
                                , <xsl:value-of select='name'/> : function(feature) {
                                    if (feature.attributes['<xsl:value-of select='attribute'/>'] == '<xsl:value-of select='$egual'/>') return '<xsl:value-of select='result'/>'; else return '<xsl:value-of select='defaultresult'/>';  
                                }
                            </xsl:when>
 
                            <!-- fidegualfunction -->
                            <xsl:otherwise>
                                <xsl:variable name="egual">
                                    <xsl:choose>            
                                        <xsl:when test="egual/getValueFrom">
                                            <xsl:for-each select='egual/getValueFrom'><xsl:call-template name="getValueFrom" /></xsl:for-each>    
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select='egual'/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:variable>
                                , <xsl:value-of select='name'/> : function(feature) {
                                    if (feature.fid == '<xsl:value-of select='$egual'/>') return '<xsl:value-of select='result'/>'; else return '<xsl:value-of select='defaultresult'/>';  
                                }
                            </xsl:otherwise>
                          </xsl:choose>
                        </xsl:when>
                        <!-- standard function -->
                        <xsl:otherwise>
                        /* xxxxxxx standard function */

                            , <xsl:value-of select='name'/> : function(feature) {
                                <xsl:value-of select='code'/>     
                            }
                        </xsl:otherwise>
                      </xsl:choose>                       
                        
                    </xsl:for-each>  
                    
                    <xsl:if test="radius">
                        ,radius: function(feature) {
                            <xsl:if test="maxradius">
                                if ( typeof(feature.attributes) != 'undefined' &amp;&amp; typeof(feature.attributes.count) != 'undefined')
                                {
                                    return Math.min(feature.attributes.count, <xsl:value-of select='maxradius'/>) + <xsl:value-of select='radius'/>;
                                }
                                else
                                {
                                    return <xsl:value-of select='radius'/>;
                                }                            
                            </xsl:if>
                            <xsl:if test="not(maxradius)">
                                if ( typeof(feature.attributes) != 'undefined' &amp;&amp; typeof(feature.attributes.count) != 'undefined')
                                {
                                    return feature.attributes.count + <xsl:value-of select='radius'/>;
                                }
                                else
                                {
                                    return <xsl:value-of select='radius'/>;
                                }
                            </xsl:if>
                        }
                    </xsl:if>  
                </xsl:for-each>    
            }  
        }
  </xsl:template>


</xsl:stylesheet>
