.. _widget-editfeature-update-label:

====================
 EditFeature_Update
====================

Widget that enables the modification of geometry and/or attributes of existing
features on vector layers on the map.

.. note:: This widget can't be drawn with the drawWidget(s) template(s).
          Instead, it must be added to the GeoExtToolbar widget using its
          **__featurepanel__** widget tag value.

.. seealso::

   :ref:`widget-editfeature-label`


XML Sample
------------
Sample configuration

.. code-block:: xml

   <editfeature_update>
     <name>W_MyEditFeature_Update</name>
     <options>
       <featurepanel>W_MyFeaturePanelForm</featurepanel>
     </options>
   </editfeature_update>


Mandatory Options
-------------------



Optional Options
------------------
:editgeom:              (Boolean).  Defaults to 'true'.  Whether the widget
                        should enable geometry editing or not.
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
:text:                  The text to display for the item menu of the toolbar.
                        You can also define a text node in the datastore
                        params instead.


Resource Options
------------------
:selectorMethod: (String) Only used if this widget has no 'featurepanel' option
                 set. After inserting a single feature, open a window containing
                 what this method returns.

                 .. note::  This widget can do 'insert' commits when an other
                            editfeature widget has the **toogleEdit** option
                            set, which delegates the commit to this widget.
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
update
