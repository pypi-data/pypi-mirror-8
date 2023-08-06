.. _widget-geoextux-wmsbrowser-label:

==============================
 GeoExtux_WMSBrowser
==============================

This widget is directly taken from the GeoExt.ux eXtensions.  It's a button
added to the toolbar that shows a window containing a tool to add WMS layers.

.. note::

   This widget should be included only once.

.. note:: 

   (i18n) This widget uses the i18n files included in its source directory.  If
   you wish to add more lang, add them inside the GeoExt.ux widget directly and
   then add them inside the .xslt.


XML Sample
------------
Sample configuration.

.. code-block:: xml

    <geoextux_wmsbrowser>
      <name>W_MyWMSBrowser</name>
      <options>
        <servers>
          <server>http://example.com/wms?request=GetCapabilities</server>
        </servers>
      </options>
    </geoextux_wmsbrowser>


How to 'draw' the widget
---------------------------------
This widget must be drawn inside a GeoExtToolbar widget :

.. code-block:: xml

    <geoexttoolbar>
      <name>W_MyGeoExtToolbar</name>
      <options>
        <widgets>
          <widget>W_MyWMSBrowser</widget>
        </widgets>
      </options>
    </geoexttoolbar>


Mandatory Options
-------------------
There are no mandatory options for this widget.


Optional Options
------------------
:server:                 (String) List of predefined servers.
:blacklistedURLs:        Contains *blacklistedURL* nodes.
:blacklistedURLs/blacklistedURL:         (String) URL of the server that must not be connected to.
:whitelistedURLs:         Contains *whitelistedURL* nodes.
:whitelistedURLs/whitelistedURL:         (String) URL of the server that must be connected to.
                                         Every other URLs will return blank.
:useIcons:               (Boolean) Defaults to **true**.  Whether use an icon
                         for the button (true) or text (false).

Service Type
--------------
N/A


Widget Action
--------------
N/A
