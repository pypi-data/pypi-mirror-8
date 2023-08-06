.. _widget-editfeature-confirm-label:

=====================
 EditFeature_Confirm
=====================

This widget creates a small popup with "confirm" and "cancel" buttons, which
can be used by other EditFeature widgets to control the commits it makes. It
automatically link itself to them according to the following requirements :

 * the foreign EditFeautre widget has no FeaturePanel already linked
 * the foreign EditFeature widget is not already linked to an other one

By default, an EditFeature widget that follow the above requirements but that
are not linked to this widget make commits automatically without any form of
confirmation.

Here's the list of widgets that this one can be linked to :

 * :ref:`widget-editfeature-copy-label`
 * :ref:`widget-editfeature-create-label`
 * :ref:`widget-editfeature-drag-label`
 * :ref:`widget-editfeature-update-label`


XML Sample
------------
Sample configuration of the widget :

.. code-block:: xml

   <editfeature_confirm>
     <name>W_MyEditFeature_Confirm</name>
     <options />
   </editfeature_copy>


How to draw the widget
-----------------------
This widget doesn't need to be drawn.


Mandatory Options
-------------------
N/A


Optional Options
------------------
N/A


Resource options
-----------------
N/A


Service Type
--------------
featureserver


Widget Action
--------------
read
