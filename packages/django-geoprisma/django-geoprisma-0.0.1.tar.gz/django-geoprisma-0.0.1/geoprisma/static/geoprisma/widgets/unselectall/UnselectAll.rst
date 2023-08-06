.. _widget-unselectall-label:

==============================
 UnselectAll
==============================


XML Sample
------------
Sample configuration.

.. code-block:: xml

    <unselectall>
      <name>W_MyUnselectAll</name>
      <options/>
    </unselectall>


How to 'draw' the widget
---------------------------------
This widget must be drawn inside a GeoExtToolbar widget :

.. code-block:: xml

    <geoexttoolbar>
      <name>W_MyGeoExtToolbar</name>
      <options>
        <widgets>
          <widget>W_MyUnselectAll</widget>
        </widgets>
      </options>
    </geoexttoolbar>


Mandatory Options
-------------------
There are no mandatory options for this widget.


Optional Options
------------------
There are no optional options for this widget.


Service Type
--------------
N/A


Widget Action
--------------
N/A
