.. _widgets-layer-label:

==========
 Layer
==========

This is the widget that creates the OpenLayers.Layer objets.  It must be linked
the a resource in order to do so.  For each resource linked to a Layer widget,
the according OpenLayers.Layer objects are created and added to the map 
depending on its available DataStores and Services it's linked to.

.. note:: Must be used with the :ref:`widgets-mappanel-label` widget.

.. note:: It replaces and **deprecates** the :ref:`widgets-map-label` widget.



XML Sample
------------
Sample configuration.

.. code-block:: xml

    <layer>
      <name>W_MyLayerWMS</name>
      <options>
        <servicetype>wms</servicetype>
        <isBaseLayer>false</isBaseLayer>
        <projectionString>EPSG:42304</projectionString>
        <transparent>true</transparent>
        <buffer>0</buffer>
        <visibility>false</visibility>
        <group>GMap</group>
        <singleTile>true</singleTile>
      </options>
    </layer>


How to 'draw' the widget
---------------------------------
You don't need to draw this widget.  The layers it creates are automatically
added to the map.


Mandatory Options
-------------------
There are no mandatory options for this widget.


Optional Options
------------------
Any OpenLayers.Layer or OpenLayers.Layer.**[ANYCLASS]** properties and 
OpenLayers.Layer 'param' properties that have
**String**, **Numeric** or **Boolean**
values are valid options for this widget.  Those that would need to have other
values, for example Array, Objects, HashTables, etc. have conterpart options
using string values in order to set them :

:cluster: (Boolean) If set to true, add a OpenLayers.Strategy.Cluster object
          to the 'strategies' option.  Only useful for OpenLayers.Layer.Vector
          objects.
:projectionString: (String) The projection to use for the layer.  Used to set
                   the OpenLayers.Layer *projection* property.  Value example :
                   'EPSG:900913'
:tileSizeString: (String) The tile size separated by ','.  Used to set the
                 OpenLayers.Layer.Grid (WMS) *tileSize* property.

Most commonly used
~~~~~~~~~~~~~~~~~~~

:isBaseLayer: (Boolean)
:transparent: (Boolean)
:format: (String)
:buffer: (Integer)
:ratio: (Float)
:singleTile: (Boolean)
:visibility: (Boolean)
:type: (String) Used by 'TMS' layers. The format extension corresponding to the
       requested tile image type.  
:geometryName: (String) Used by the 'WFS' layers to set the 'geometryName'
               property of the OpenLayers.Protocol.WFS.

Widget-specific
~~~~~~~~~~~~~~~~

:servicetype: (String) Possible values are : "wms", "tilecache", "featureserver"
              and "gymo".  If set, only the layers of the according service
              type will be created by the widget.  If not set, all layers
              of all service types the resource has are created (default
              behavior).
:group: (String) The group the created layers are member of.  You can define
        sub groups by adding "/" characters between groups.  For example : 
        "group/subgroup".  This option is used by the 
        :ref:`widgets-geoextux-layertreebuilder-label` widget.


Resource Options
-----------------
:noLayer: (Boolean) If set to true, then no layer will be created for the
          resource regardless of the layer widgets linked to it.


Service Type
--------------
N/A


Widget Action
--------------
read
