.. _widget-resultvectorlayer-label:

========================
 ResultVectorLayer
========================

Widget that displays features inside a vector layer.

The following widgets can use it (using the <result> tag) :

  * :ref:`widget-queryonclick-label`.


.. warning:: Only features with **geometry** are added to the layer.  If using
             WMSGetFeatureInfo requests, be sure to setup your server in order
             to have the geometry included in the features.

XML Sample
------------
Sample configuration. Not defining a 'vectorlayer' option lets the widget
creates its own OpenLayer.Layer.Vector layer.

.. code-block:: xml

   <resultvectorlayer>
     <name>W_MyResultVectorLayer</name>
     <options />
   </resultvectorlayer>


Sample configuration, with a 'vectorlayer' option defined, which makes the
widget use the :ref:`widget-vectorlayer-label` widget's OpenLayer.Layer.Vector
instead of creating one.

.. code-block:: xml

   <resultvectorlayer>
     <name>W_MyResultVectorLayer</name>
     <options>
       <vectorlayer>W_MyVectorLayer</vectorlayer>
     </options>
   </resultvectorlayer>


drawWidget Sample
-------------------
This widget doesn't need to be drawn.


Mandatory Options
-------------------
N/A


Optional Options
------------------
:vectorlayer: (String) The name of the :ref:`widget-vectorlayer-label` widget
              to use its defined OpenLayers.Layer.Vector instead of letting
              this widget creating its own.
:singleMode: (Boolean) Defaults to false.  When set to true, the first valid
             feature added to the layer that is linked to a resource will set
             the 'singleResource' property equal to the feature's resource,
             which means that from there on, only features (inside the remaining
             query results) of this specific resource will be added to the
             layer.  The 'singleResource' property get automatically reseted
             if a new query is made that was not in 'multiple' mode
             (see :ref:`widget-queryonclick-label` 'multipleKey' option).


Service Type
--------------
wms


Widget Action
--------------
read
