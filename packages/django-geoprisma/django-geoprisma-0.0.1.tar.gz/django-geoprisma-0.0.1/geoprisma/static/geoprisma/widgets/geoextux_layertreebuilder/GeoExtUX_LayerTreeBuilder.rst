.. _widgets-geoextux-layertreebuilder-label:

==============================
 GeoExtux_LayerTreeBuilder
==============================

This widget is directly taken from the GeoExt.ux eXtensions.  It's a LayerTree
widget that automatically creates its nodes every time a new
OpenLayers.Layer object is added to the map.

Features
---------

* The widget checks the 'group' property of the and put a new LayerNode
  object in the tree.  If any nodes don't exist, it creates them first.
* WMS layer nodes send 'GetLegendGraphic' requests when toggled visible.
* Base layers without 'group' property are added to a "Base layers" node
* Other layers without 'group' property are added to a "Other layers" node.
* If 'group' is set to "", the layer is added to the root of the tree. 


XML Sample
------------
Sample configuration.

.. code-block:: xml

    <geoextux_layertreebuilder>
      <name>W_MyLayerTreeBuilder</name>
      <options>
        <wmsLegendNodes>false</wmsLegendNodes>
      </options>
    </geoextux_layertreebuilder>


How to 'draw' the widget
---------------------------------
This widget must be drawn using the **drawWidgets** method :
:ref:`widget-basics-drawWidgets-label`


Mandatory Options
-------------------
There are no mandatory options for this widget.


Optional Options
------------------
Any Ext.tree.TreePanel property is a valid option for this widget.

:wmsLegendNodes: (Boolean) Defaults to 'true'.  Whether wms layer nodes should
                 display a legend or not.
:vectorLegendNodes: (Boolean) Defaults to 'true'.  Whether vectro layer nodes
                    should display a legend or not.


Notes and warnings
-------------------

.. warning::

   Don't use hashtable objects when creating your Ext objects in your
   template.xslt file.  This widget doesn't work with them.  Directly
   instanciate the objects instead.

Don't :

.. code-block:: xml

   var oCenterPanel = { xtype: 'panel', ... };

Do :

.. code-block:: xml

   var oCenterPanel = new Ext.Panel({ ... });

.. warning::

   When using this widget with the :ref:`widgets-map-label` widget, you must
   set 'addLayers' map option to 'false' and manually add them after the
   creation of the GeoExt.MapPanel widget and after the printWidgetExecution
   template call.

Here's an example on how to do so :

.. code-block:: xml

     <xsl:variable name="pstrMapName">
       <xsl:value-of select="/geoprisma/widgets/widget[./type = 'map']/name"></xsl:value-of>
     </xsl:variable>
     <xsl:call-template name="map:addLayers" >
       <xsl:with-param name="pMapName">
         <xsl:value-of select="$pstrMapName"></xsl:value-of>
       </xsl:with-param>
     </xsl:call-template>

.. note::

   Avoid using tilecache services without the 'staticCache' option set to true.
   Layers without this option are created as 'WMS', which make them send
   'GetLegendGraphic' requests that never return anything when they become
   visible.


Service Type
--------------
N/A


Widget Action
--------------
N/A
