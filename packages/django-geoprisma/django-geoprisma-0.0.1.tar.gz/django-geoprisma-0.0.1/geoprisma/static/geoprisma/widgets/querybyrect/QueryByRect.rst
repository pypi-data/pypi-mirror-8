.. _widget-querybyrect-label:

========================
 QueryByRect
========================

Widget that send GetFeature requests when a box is drawn on the map.  Only
visible layers are queried.

To display the query results, the widget must use one or more of theses
widgets :

  * :ref:`widget-resultextgrid-label`.


.. note:: This widget can't be drawn with the drawWidget template.  Instead,
          it must be added to one of the toolbar widgets :

          * GeoExtToolbar

.. note:: When added to the GeoExtToolbar, a dropDown is created.  
          Its content gets populated by the following information (only one,
          in priority order) :

          * the <title> of the resource
          * the <text> node of the DataStore (if set)
          * the resource name


XML Sample
------------
Sample configuration

.. code-block:: xml

   <querybyrect>
     <name>W_MyQuerybyrect</name>
     <options>
       <results>
         <result>W_MyResultExtGrid</result>
       </results>
     </options>
   </querybyrect>


Having a single <result> tag if only one result is used by the widget is also
okay :

.. code-block:: xml

   <querybyrect>
     <name>W_MyQuerybyrect</name>
     <options>
       <result>W_MyResultExtGrid</result>
     </options>
   </querybyrect>


Configuration with "resetOnDeactivation" set to all

.. code-block:: xml

   <querybyrect>
     <name>W_MyQuerybyrect</name>
     <options>
       <resetOnDeactivation>all</resetOnDeactivation>
       <results>
         <result>W_MyResultExtGrid</result>
       </results>
     </options>
   </querybyrect>


XML Sample - widget to be added to a toolbar
---------------------------------------------
This widget must be added to a GeoExtToolbar widget

.. code-block:: xslt

  <geoexttoolbar>
    <name>W_GeoExtToolbar</name>
    <options>
      <widgets>
        <widget>W_MyQuerybyrect</widget>
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
                      automatically set to "nothing".  You can set this option
                      to (**case sensitive**): 

                      * nothing : (removes nothing)
                      * all : (reset the query results)

:dropDownList:        Can be set to *true* or *false*.  Default value is *true*
                      if ommited.  Creates a SplitButton object if set to 
                      *true* instead of a regular button.


Service Type
--------------
* featureserver
* wfs


Widget Action
--------------
read
