.. _widget-geoextux-zoomto-label:

==============================
 GeoExtux_ZoomTo
==============================

This widget is directly taken from the GeoExt.ux eXtensions.  It's a button
added to the toolbar that, on click, pops a window that contains a combobox of
projection, X and Y textfields to input coordinates and a "zoom" button that, 
when clicked, recenters the map to the inputed location using the selected
projection.

When choosing an other projection from the list, if the X and Y textfields
contain coordinates, they will be reprojected in the newly selected projection.

.. note::

   For each 'projection' option set, this widget will automatically load the
   according file of the same name from the proj4js library located in the
   **$GP_ROOT/lib/client/proj4js/lib/defs/** directory.

   A projection file must be named as its original name minus the semi-colons,
   for example : **EPSG:32198** must be named **EPSG32198.js**.

.. note::

   This widget should be included only once.


XML Sample
------------
Sample configuration.

.. code-block:: xml

    <geoextux_zoomto>
      <name>W_MyZoomTo</name>
      <options>
        <projections>
          <projection>EPSG:42304</projection>
        </projections>
        <defaultZoomLevel>10</defaultZoomLevel>
      </options>
    </geoextux_zoomto>


How to 'draw' the widget
---------------------------------
This widget must be drawn inside a GeoExtToolbar widget :

.. code-block:: xml

    <geoexttoolbar>
      <name>W_MyGeoExtToolbar</name>
      <options>
        <widgets>
          <widget>W_MyZoomTo</widget>
        </widgets>
      </options>
    </geoexttoolbar>


Mandatory Options
-------------------
There are no mandatory options for this widget.

.. note:: In order for this widget to work properly, all layer widgets must
          have a **projectionString** option set.


Optional Options
------------------
:projections:            Contains *projection* nodes.
:projections/projection: The projection code to add.  Requires proj4js and its
                         unique projection file (see in description above) 

                         .. note:: If none is set, then EPSG:4326 and
                                   EPSG:900913 are used by default. They don't
                                   required proj4js since they are already 
                                   included in the OpenLayers library.

:defaultZoomLevel:       (Integer) The level to zoom to when zooming.  If not
                         defined, the map gets recentered only (not zoomed).
:autoHideWindowOnZoom:   (Boolean) Defaults to **true**.  Hides the popup after
                         zooming or not.
:showCenter:             (Boolean) Defaults to **true**.  Shows a **+** marker
                         on center of the map after zooming or not.
:useIcons:               (Boolean) Defaults to **true**.  Whether use an icon
                         for the button (true) or text (false).
:autoLoad:               (Boolean) Defaults to **true**.  Whether automaticaly
                         load the Proj4js library or include them manually
                         (false). You need to define the
                         **projections/projection** parameter if it set to
                         false.
:enableDrag:             (Boolean) Defaults to **false**. Requires *showCenter*
                         option set.  If set, the center marker can be dragged
                         around, which updates the coordinates displayed in
                         the popup.


Service Type
--------------
N/A


Widget Action
--------------
N/A
