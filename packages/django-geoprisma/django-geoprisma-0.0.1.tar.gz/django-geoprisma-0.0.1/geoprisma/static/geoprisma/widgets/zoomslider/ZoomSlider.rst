.. _widget-zoomslider-label:

========================
 ZoomSlider
========================

Replaces the OpenLayers zoom slider control by the GeoExt ZoomSlider widget by
using a *Slider* from ExtJS and some *.css* replacement.

.. note:: Must be applied as an item of a GeoExt.MapPanel with layout:'anchor'.

.. note:: This widget must appear only once.

XML Sample
------------
Sample configuration

.. code-block:: xml

   <zoomslider>
     <name>W_MyZoomSlider</name>
     <options>
     </options>
   </zoomslider>

drawWidget Sample
-------------------
The widget can be drawn with the *drawWidget* function but directly in a
GeoExt.MapPanel object.  Here's an example of use :

.. code-block:: xslt

   oMyMapPanel = new GeoExt.MapPanel ({
     id: 'gpDefaultMap',
     title: 'Map',
     layout: 'anchor', // (Mandatory)
     region: 'center',
     border: false,
     height: 800,
     width: 800,
     <xsl:if test="count(/geoprisma/widgets/widget[./type = 'zoomslider']) > 0 ">
     items: [
       <xsl:for-each select="/geoprisma/widgets/widget[./type = 'zoomslider']">
         <xsl:call-template name="zoomslider:drawWidget">
           <xsl:with-param name="pWidgetName" select="./name" />
         </xsl:call-template>
       </xsl:for-each>
     ],
     </xsl:if>
     map: oMap
   });


Mandatory Options
-------------------
N/A


Optional Options
------------------
N/A


Service Type
--------------
N/A


Widget Action
--------------
read
