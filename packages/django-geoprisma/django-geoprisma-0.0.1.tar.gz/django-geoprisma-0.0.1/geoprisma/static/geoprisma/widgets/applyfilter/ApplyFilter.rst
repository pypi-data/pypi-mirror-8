.. _widget-applyfilter-label:

=============
 ApplyFilter
=============

A widget listening to GeoPrisma API "applyfilters" event to apply filters from
third party libraries to one or more resources.  The filters are applied in two
ways :

* on the resource OpenLayers.Layer.WMS object using SLD
* in a grid using WFS

The grid features :

* paging
* vector features added to the map for the page currently visible
* on row select, the according vector feature on the map gets highlighted
* a column containing a "zoomTo" button to zoom the map on the feature

.. warning:: Only one instance of this widget is currently supported, so make
             sure you only define one in your config.

.. note:: The widget must be linked to the resources required to be filtered.

.. note:: A resource must have both **WMS and WFS DataStores** to be linked with
          this widget.


XML Sample
-----------
Sample configuration.

.. code-block:: xml

   <applyfilter>
     <name>W_ApplyFilter</name>
      <options>
        <pageSize>5</pageSize>
        <maxZoomScale>1000000</maxZoomScale>
      </options>
   </applyfilter>


How to draw the widget
-----------------------

The widget must be drawn with the *drawWidgets* function.  See
:ref:`widget-basics-drawWidgets-label`.

The content drawn is the TabPanel containg the grids for each resource that can
be filtered.


Mandatory Options
-------------------
N/A


Optional Options
------------------

:ignoredField: (String) Use this option instead of ignoredFields/ignoredField
               when you only want to define one. See below for more.
:ignoredFields/ignoredField: (String) You can set more than one of this option.
                             Each define a field to ignore, i.e. not to show in
                             the grids.  Defaults to "geometry", "geom" and
                             "the_geom" if not set.
                           
                             .. note:: The "ignoredField" and "ignoredFields"
                                       resource options have priority over
                                       these options, so for that resource
                                       grid, if any of these resource options
                                       is set, this widget option is not used.

:maxZoomScale: (Float) Defines the max scale denominator allow to zoom to.  Used
               when zooming on features.
:pageSize: (Integer) Defaults to 10. Sets the maximum number of rows to display
           per page inside the result grid. Only used by WFS, i.e. in WMS all
           features returned by the query are displayed in the map.


Resource options
-----------------

:ignoredField: (String) Use this option instead of ignoredFields/ignoredField
               when you only want to define one. See below for more.
:ignoredFields/ignoredField: (String) You can set more than one of this option.
                             Same purpose as the widget option of the same name,
                             but only applies for the resource. Has priority
                             over widget option.


Resource fields
----------------

This widget can use resource fields parameters and options to set the according
element options created, such as the grid and its columns.  

:title: (String) Sets the column header for the field in the grid. If not set,
        the name of the field is used instead.
:options/width: (Integer) Set the width of the column in the grid. If not set,
                the default value set by Ext is used.

Example of a resource with fields used by this widget :

.. code-block:: xml

    <resource>
      <name>R_Park</name>
      <title>Parks</title>
      <datastores>
        <datastore>DS_Park_WMS</datastore>
        <datastore>DS_Park_WFS</datastore>
      </datastores>
      <widgets>
        <widget>W_Layer_Park_WMS</widget>
        <widget>W_ApplyFilter</widget>
      </widgets>
      <fields> <!-- fields -->
        <field>
          <name>NAME_E</name>
          <title>Name (en)</title> <!-- title -->
          <options>
            <width>200</width> <!-- width -->
          </options>
        </field>
        <field>
          <name>NAME_F</name>
          <title>Name (fr)</title>
          <options>
            <width>200</width>
          </options>
        </field>
      </fields>
      <options />
    </resource>


Service Type
--------------

* WMS (for SLD filtering on the WMS layer)
* WFS (for WFS filtering in the grid)


Widget Action
--------------
read
