.. _widget-editfeature-create-label:

====================
 EditFeature_Create
====================

Widget that enables the possibility to draw new features on vector layers on
the map.  Since the new features drawn are directly linked to a Resource, you
must specify the kind of geometry available to draw.

.. note:: This widget can't be drawn with the drawWidget(s) template(s).
          Instead, it must be added to the GeoExtToolbar widget using its
          **__featurepanel__** widget tag value.

.. seealso::

   :ref:`widget-editfeature-label`


XML Sample
------------
Sample configuration

.. code-block:: xml

   <editfeature_create>
     <name>W_MyEditFeature_Create_LineString</name>
     <options>
       <geometrytype>LineString</geometrytype>
       <featurepanel>W_MyFeaturePanelForm</featurepanel>
     </options>
   </editfeature_create>


Mandatory Options
-------------------
:geometrytype: The geometry type the widget can draw.  The possible values are
               (**case sensitive**) :

               * Point
               * LineString
               * Polygon


Optional Options
------------------
:featurepanel:          The name of the *featurepanel* widget (of any kind)
                        to display to edit the attributes (fields) of features. 
                        If none was provided, then the attributes can't be
                        edited.
:featurecontroloptions: The options for the OpenLayers control to be created.
                        Can have any
                        <OpenLayers property>value</OpenLayers property>
                        tag of the corresponding Control created, i.e.
                        SelectFeature (editgeom: false) or ModifyFeature
                        (editgeom: true).
:drawfeatureoptions:    The options for the OpenLayers DrawFeature controls to
                        be created.  Can have any
                        <OpenLayers property>value</OpenLayers property>
                        tag of the DrawFeature control.
:text:                  The text to display for the item menu of the toolbar.
                        You can also define a text node in the datastore
                        params instead.


Resource Options
------------------
:selectorMethod: (String) Only used if this widget has no 'featurepanel' option
                 set. After inserting a single feature, open a window
                 containing what this method returns.
:selectorTemplateHeight: (Integer) If set, defines the height of the window
                         opened after a single insert.  Only used when
                         "selectorMethod" resource option is set.
:selectorTemplateWidth: (Integer) If set, defines the width of the window
                         opened after a single insert.  Only used when
                         "selectorMethod" resource option is set.


Service Type
--------------
featureserver


Widget Action
--------------
create
