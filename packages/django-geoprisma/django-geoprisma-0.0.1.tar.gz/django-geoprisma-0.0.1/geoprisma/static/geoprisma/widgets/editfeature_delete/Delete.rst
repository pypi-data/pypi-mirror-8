.. _widget-editfeature-delete-label:

====================
 EditFeature_Delete
====================

Widget that enables the possibility to delete existing features on vector
layers of the map.

.. note:: This widget can't be drawn with the drawWidget(s) template(s).
          Instead, it must be added to the GeoExtToolbar widget using its
          **__featurepanel__** widget tag value.

.. seealso::

   :ref:`widget-editfeature-label`


XML Sample
------------
Sample configuration

.. code-block:: xml

   <editfeature_delete>
     <name>W_MyEditFeature_Delete</name>
     <options>
       <featurecontroloptions>
         <multiple>true</multiple>
         <box>true</box>
       </featurecontroloptions>
     </options>
   </editfeature_delete>


Mandatory Options
-------------------


Optional Options
------------------
:featurecontroloptions: The options for the OpenLayers control to be created.
                        Can have any
                        <OpenLayers property>value</OpenLayers property>
                        tag of the corresponding Control created, i.e.
                        SelectFeature (editgeom: false) or ModifyFeature
                        (editgeom: true).
:text:                  The text to display for the item menu of the toolbar.
                        You can also define a text node in the datastore
                        params instead.


Service Type
--------------
featureserver


Widget Action
--------------
delete
