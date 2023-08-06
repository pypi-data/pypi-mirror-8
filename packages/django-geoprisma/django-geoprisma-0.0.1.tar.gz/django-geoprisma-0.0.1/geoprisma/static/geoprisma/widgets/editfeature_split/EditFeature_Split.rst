.. _widget-editfeature-split-label:

===================
 EditFeature_Split
===================

Use the OpenLayers.Control.SplitFeature control to allow splitting vector
features on the map on a specific resource.

.. note:: Must be added to a GeoExtToolbar widget.


XML Sample
------------
Sample configuration of the widget :

.. code-block:: xml

   <editfeature_split>
     <name>W_MyEditFeature_Split</name>
     <options>
     </options>
   </editfeature_split>


Mandatory Options
-------------------
N/A


Optional Options
------------------
:splitWindow: (String) The name of the Ext.Window element to show after spliting
              a polygon.  I must have 'closeAction': 'hide set.  It receives a
              '_splitInfo' property which contains the splited features and the
              control.


Service Type
--------------
featureserver


Widget Action
--------------
create
