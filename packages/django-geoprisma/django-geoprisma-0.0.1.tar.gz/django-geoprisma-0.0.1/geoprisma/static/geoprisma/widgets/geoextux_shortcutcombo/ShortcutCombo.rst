==============================
 GeoExtux_ShortcutCombo
==============================

This widget is directly taken from the GeoExt.ux eXtensions.  Basically, it's
a combobox populated from a specific Ext.data.Store object manually defined.

.. seealso::

   http://trac.geoext.org/wiki/ux/ShortcutCombo

.. warning::

   This widget is experimental.  Its source file comes from a sandbox (not
   official).


XML Sample
------------
Sample configuration.

.. code-block:: xml

    <geoextux_shortcutcombo>
      <name>W_GeoExtux_ShortcutCombo</name>
      <options>
        <title>Countries</title>
        <store>GeoExt.ux.ShortcutCombo.countryStore</store>
        <bboxField>bbox</bboxField>
        <bboxSrs>EPSG:900913</bboxSrs>
      </options>
    </geoextux_shortcutcombo>


How to 'draw' the widget
---------------------------------
Can be added inside a geoexttoolbar or inside a panel using the drawWidgets
method.

Inside a toolbar :

.. code-block:: xml

    <geoexttoolbar>
      <name>GeoExtToolbar</name>
      <options>
        <widgets>
          <widget>W_GeoExtux_ShortcutCombo</widget>
        </widgets>
      </options>
    </geoexttoolbar>

Using drawWidgets (**only**, *drawWidget* is not supported by this widget),
see :
:ref:`widget-basics-drawWidgets-label`


Mandatory Options
-------------------
:title:     The title to display when no element is selected in the list and
            also as the title of the list.
:store:     The variable name of the Ext.ux.Store object.  The javascript file 
            containing the defined object must be included in the template.
:bboxField: The field name inside the store containing the geometry.
:bboxSrs:   The EPSG:XXXX value of the geometry inside the store.


Optional Options
------------------
There are no optional options for this widget.


Service Type
--------------
none


Widget Action
--------------
read
