.. _widgets-mappanel-label:

==========
 MapPanel
==========

This is the widget that creates the OpenLayers.Map and GeoExt.MapPanel widgets.

.. note:: It replaces and **deprecates** the :ref:`widgets-map-label` widget.

.. note::
   OpenLayers.Layer objects are not created by this widget, but rather by the
   :ref:`widgets-layer-label` widget.


Initial map center/extent
--------------------------

You can set the initial center or extent of the map using one of the following
combinaison of options :

* **centerString** and **zoom**
* **extentString**

See below for more details.

.. note:: If you don't set one of these combinaisons, then the initial extent
          of the map will be equal to its max extent.


XMLWorkspaceConfig
~~~~~~~~~~~~~~~~~~~

If you're using the XMLWorkspaceConfig driver, it's possible to override the
above options inside the workspace **mappaneloptions** tag.  This way, you can
have a unique initial map center/extent for each workspace.

Here's a example :

.. code-block:: xml

    <workspace>
      <name>WS_Default</name>
      <mappaneloptions>
        <centerString>1682372,220446</centerString> <!-- overrides mappanel "centerString" option -->
        <zoom>3</zoom> <!-- overrides mappanel "zoom" option -->
      </mappaneloptions>
      <resources>
        <resource>
          <name>R_Base</name>
          <widgets>
            <widget>W_Layer_Base_TileCache</widget>
          </widgets>
        </resource>
      </resources>
    </workspace>

.. note:: You can override **any** mappanel option defined below that way when
          using the XMLWorkpaceConfig driver.


XML Sample
------------
Sample configuration.

.. code-block:: xml

    <mappanel>
      <name>W_MyMapPanel</name>
      <options>
        <maxExtentString>-2751549.750,-935783.250,3582850.250,4674119.750</maxExtentString>
        <projectionString>EPSG:42304</projectionString>
        <units>m</units>
        <maxResolution>156543.0339</maxResolution>
        <scalesString>20000000,10000000,4000000,1000000,500000</scalesString>
        <numZoomLevels>5</numZoomLevels>
        <allOverlays>false</allOverlays>
        <centerString>1142372,888446</centerString>
        <zoom>0</zoom>
      </options>
    </mappanel>


How to 'draw' the widget
---------------------------------
This widget must be drawn using the **drawWidgets** method :
:ref:`widget-basics-drawWidgets-label`


Mandatory Options
-------------------
There are no mandatory options for this widget.


Optional Options
------------------

Any GeoExt.MapPanel and OpenLayers.Map properties that have
**String**, **Numeric** or **Boolean**
values are valid options for this widget.  Those that would need to
have other values, for example Array, Objects, HashTables, etc. have 
conterpart options using string values in order to set them :

:centerString: (String) Center string separated by ','.  Used to set the
               GeoExt.MapPanel *center* property. Can be use in combinaison
               with the *zoom* option for initial map centering purpose.
:displayProjectionString: (String) The display projection to use for the map.
                          Used to set the OpenLayers.Map *displayProjection*
                          property.  Value example : 'EPSG:4326'
:extentString: (String) Extent string separated by ','. Used to set the
               GeoExt.MapPanel *extent* property.  Used for initial map
               centering purpose.
:projectionString: (String) The projection to use for the map.  Used to set the
                   OpenLayers.Map *projection* property.  Value example :
                   'EPSG:900913'
:maxExtentString:  (String) Extent string separated by ','.  Used to set the
                   OpenLayers.Map *maxExtent* property.
:resolutionsString: (String) The resolution list seperated by ','.  Used to set
                    the OpenLayers.Map *resolutions* property. 
:scalesString:     (String) The scale list separated by ','.  Used to set the
                   OpenLayers.Map *scales* property.

Among those that use official OpenLayers.Map or GeoExt.MapPanel properties, here
are the most commonly used ones :

:title: (String) Sets the title for the MapPanel.  Supports :ref:`i18n-label`.
:allOverlays: (Boolean)
:units: (String)
:maxResolution: (Float)
:zoom: (Integer) Sets the *zoom* property of the MapPanel. Requires the
       *centerString* option set.

Here's the widget-specific options :

:pageTitle: (String) Defaults to "GeoPrisma".  Can be used to set the page
            ``<title>`` tag value. Requires the replacement of the ``<title>``
            tag by a ``<xsl:call-template>`` tag as demonstrated below. This
            option supports :ref:`i18n-label` value.

            .. code-block:: xml

               <html>
                 <head>
                   <xsl:call-template name="mappanel:printPageTitle" />
                 </head>
                 <body>
                   <!-- body content -->
                 </body>
               </html>


:zoomBoxNavigation: (Boolean) Defaults to false.  Whether the default Navigation
                    control, which is always active, should use the 'box'
                    handler or not.  Enabling this can sometime results in
                    handler incompatibility since it uses the "shift" key.


Service Type
--------------
N/A


Widget Action
--------------
N/A
