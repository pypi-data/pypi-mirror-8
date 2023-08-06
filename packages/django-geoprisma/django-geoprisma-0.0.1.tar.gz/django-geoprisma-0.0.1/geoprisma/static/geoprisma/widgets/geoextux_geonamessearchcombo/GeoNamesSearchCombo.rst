==============================
 GeoExtux_GeoNamesSearchCombo
==============================

This widget is directly taken from the GeoExt.ux eXtensions.  Basically, it's
a textbox where the user can input anything, like City name, Countries, Street
names, etc.  While the text is entered, a request is sent to an external
(public) database and *GeoReferenced* results are displayed in a list.  
Clicking on any result recenters the map to its location.

.. seealso::

   http://trac.geoext.org/wiki/ux/GeonamesSearch


XML Sample
------------
Sample configuration with no options.

.. code-block:: xml

    <geoextux_geonamessearchcombo>
      <name>MyGeoExtuxGeoNamesSearchCombo</name>
      <options></options>
    </geoextux_geonamessearchcombo>


Sample configuration with one option

.. code-block:: xml

    <geoextux_geonamessearchcombo>
      <name>MyGeoExtuxGeoNamesSearchCombo</name>
      <options>
        <zoom>10</zoom> <!-- optional -->
      </options>
    </geoextux_geonamessearchcombo>


How to 'draw' the widget
---------------------------------
Currently, the widget can only be added to the *GeoExtToolbar* widget.  To be
able to do so, it must be added to the widget list, in the xml config :

.. code-block:: xml

    <geoexttoolbar>
      <name>GeoExtToolbar</name>
      <options>
        <widgets>
          <widget>MyGeoExtuxGeoNamesSearchCombo</widget>
        </widgets>
      </options>
    </geoexttoolbar>


Mandatory Options
-------------------
There are no mandatory options for this widget.


Optional Options
------------------
All the possibles options are defined in the *GeoNamesSearchCombo.js* file.
Here's the most important ones :

:width: The width of the textbox
:listWidth: The width of the list
:loadingText: The text to display while loading
:emptyText: The text shown when no in focus
:zoom: The zoom level to zoom to when recentering.
:minChars: The minimum number of characters requiered to send a query


Service Type
--------------
gymo


Widget Action
--------------
read
