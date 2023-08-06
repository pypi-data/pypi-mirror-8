.. _widget-editfeature-drag-label:

==================
 EditFeature_Drag
==================

Use the OpenLayers.Control.ModifyFeature control to allow dragging vector
features on the map on a specific resource.

.. note:: Must be added to a GeoExtToolbar widget.


XML Sample
------------
Sample configuration of the widget :

.. code-block:: xml

   <editfeature_drag>
     <name>W_MyEditFeature_Drag</name>
     <options>
       <toggleEdit>true</toggleEdit>
     </options>
   </editfeature_drag>


Mandatory Options
-------------------
N/A


Optional Options
------------------
:toggleEdit: (Boolean) Defaults to false. Only usable if an EditFeature_Update
             widget is linked to the same resource of this widget. If set to
             *true*, on feature drag complete, won't commit the changes.
             Delegate the feature to the update control instead.

Service Type
--------------
featureserver


Widget Action
--------------
update
