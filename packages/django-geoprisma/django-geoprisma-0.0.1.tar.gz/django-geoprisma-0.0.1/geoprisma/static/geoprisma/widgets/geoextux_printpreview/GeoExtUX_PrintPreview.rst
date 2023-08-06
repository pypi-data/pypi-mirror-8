.. _widget-geoextux-printpreview-label:

==============================
 GeoExtux_PrintPreview
==============================

A print widget that use the GeoExt.ux.PrintPreview widget to print the map.

.. seealso:: http://trac.geoext.org/wiki/ux/PrintPreview

.. note:: Setting the Map 'projection' is mandatory.


XML Sample
------------
Sample configuration.

.. code-block:: xml

    <geoextux_printpreview>
      <name>W_GeoExtUXPrintPreview</name>
      <options>
        <servicename>S_MapFishPrint</servicename>
      </options>
    </geoextux_printpreview>


How to 'draw' the widget
---------------------------------
This widget must be added to a toolbar.


Mandatory Options
-------------------
:servicename: (String) The name of the MapFishService to use with this widget.
              The service **capabilities** will be used to populate the values
              of the fields of this widget (layout, resolution, scale, etc.)


Optional Options
------------------
This widget has no optional options.


Service Type
--------------
mapfishprint


Widget Action
--------------
read
