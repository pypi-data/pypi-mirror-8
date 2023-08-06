.. _widget-queryonclick-label:

========================
 QueryOnClick
========================

Widget that send GetFeatureInfo requests when the map is clicked.  Only visible
layers are queried.

To display the query results, the widget must use one or more of theses
widgets :

  * :ref:`widget-resultextgrid-label`
  * :ref:`widget-featurepanel-selector-label`
  * :ref:`widget-resultvectorlayer-label`

.. note:: This widget can't be drawn with the drawWidget template.  Instead,
          it must be added to one of the toolbar widgets :

          * Toolbar
          * GeoExtToolbar

.. note:: When added to the GeoExtToolbar, a dropDown is created.  
          Its content gets populated by the following information (only one,
          in priority order) :

          * the <text> node of the DataStore (if set)
          * the resource name


XML Sample
------------
Sample configuration.

.. code-block:: xml

   <queryonclick>
     <name>W_MyQueryOnClick</name>
     <options>
       <results>
         <result>W_MyResultExtGrid</result>
       </results>
     </options>
   </queryonclick>


Having a single <result> tag if only one result is used by the widget is also
okay :

.. code-block:: xml

   <queryonclick>
     <name>W_MyQueryOnClick</name>
     <options>
       <result>W_MyResultExtGrid</result>
     </options>
   </queryonclick>


Configuration with "resetOnDeactivation" set to all

.. code-block:: xml

   <queryonclick>
     <name>W_MyQueryOnClick</name>
     <options>
       <resetOnDeactivation>all</resetOnDeactivation>
       <results>
         <result>W_MyResultExtGrid</result>
       </results>
     </options>
   </queryonclick>


Configuration using a specific marker

.. code-block:: xml

   <queryonclick>
     <name>W_MyQueryOnClick</name>
     <options>
       <markerStyle>
         <graphicWidth>42</graphicWidth>
         <graphicHeight>50</graphicHeight>
         <graphicYOffset>-50</graphicYOffset>
         <externalGraphic>/path/to/otherMarker.gif</externalGraphic>
       </markerStyle>
       <results>
         <result>W_MyResultExtGrid</result>
       </results>
     </options>
   </queryonclick>


XML Sample - widget to be added to a toolbar
---------------------------------------------
This widget must be added to a GeoExtToolbar widget

.. code-block:: xslt

  <geoexttoolbar>
    <name>W_GeoExtToolbar</name>
    <options>
      <widgets>
        <widget>W_MyQueryOnClick</widget>
      </widgets>
    </options>
  </geoexttoolbar>


Mandatory Options
-------------------
:results: Contains <result> tags if you wish to use more than one result.
          Either 'results' or 'result' is mandatory.
:result: Name of a result widget that will be used to contain the features
         returned by a query.  Can only be used if one result is used by the
         query.  Either 'results' or 'result' is mandatory.
:results/result:  If you want to have more than one result, you must define them
                  in <results> tag.


Optional Options
------------------
:resetOnDeactivation: Determine what to reset when the widget gets deactivated.
                      By default (when this option is ommited), it's
                      automatically set to "marker".  You can set this option
                      to (**case sensitive**): 

                      * marker : (removes only the query marker)
                      * nothing : (removes nothing)
                      * all : (removes the marker and reset the query results)

:markerStyle:         To change the style of the marker that appears on map
                      click.  Must contains Vector Features Symbolizer
                      properties nodes
                      (see OpenLayers/lib/OpenLayers/Feature/Vector.js).
                      See an example in the samples above.
:dropDownList:        Can be set to *true* or *false*.  Default value is *true*
                      if ommited.  Creates a SplitButton object if set to 
                      *true* instead of a regular button.
:noMarker:            Can be set to *true* or *false*.  Default value is *false*
                      if ommited.  Skip the creation of the *markerLayer* object
                      resulting in adding no marker when the map is clicked if
                      this option is set to *true*.
:iconCls:             (String) An alternative class name (CSS) to use for the
                      icon in the toolbar.
:multipleKey:         (String) Value can be 'altKey', 'shiftKey' or 'ctrlKey'.
                      Defaults to null.  If set to one of the key, holding it
                      while querying keep the old query results instead of
                      discarding them.
:altKey:              (String) Value can be 'altKey', 'shiftKey' or 'ctrlKey'.
                      Defaults to null.  If set to one of the key, holding it
                      while querying on an existing feature will unselect it.
:multiple:            (Boolean) Defaults to false.  Allow selection of multiple
                      features.
:toggle:              (Boolean) Defaults to false.  Unselect feature on click.
:displayClass:        (String) Defaults to 'olControlQueryOnClick'.  This
                      property is used for CSS related to the drawing of the
                      Control.


Resource Options
-----------------
:primaryField: (String) Defaults to null.  Defines the **name** of the primary
               key field of the resource to use by this widget when collecting
               features in 'multiple' mode.  Setting this avoids having the same
               feature selected if clicked again.

               .. note:: supported by all configuration drivers.


Service Type
--------------
wms


Widget Action
--------------
read
