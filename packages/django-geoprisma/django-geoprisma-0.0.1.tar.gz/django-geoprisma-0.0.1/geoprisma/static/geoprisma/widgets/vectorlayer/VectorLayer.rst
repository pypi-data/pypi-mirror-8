.. _widget-vectorlayer-label:

=============
 VectorLayer
=============

Creates a blank OpenLayers.Layer.Vector object that can be used by other
widgets.


XML Sample
------------
Sample configuration of the widget :

.. code-block:: xml

   <vectorlayer>
     <name>W_MyVectorLayer</name>
     <options>
       <title>Cosmetic</title>
     </options>
   </vectorlayer>


Mandatory Options
-------------------
N/A


Optional Options
------------------

:title: (String) The string value to use as the layer's name (OpenLayers).

You can also define any of the :ref:`widgets-layer-label` widget option as well
that are valid OpenLayers.Layer.Vector API properties.


Service Type
--------------
N/A


Widget Action
--------------
read
