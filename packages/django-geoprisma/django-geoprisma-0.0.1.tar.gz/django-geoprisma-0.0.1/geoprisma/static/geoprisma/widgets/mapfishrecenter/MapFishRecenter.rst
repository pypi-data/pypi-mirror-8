.. _widget-mapfishrecenter-label:

========================
 MapFishRecenter
========================

.. note:: This widget is **deprecated**.

Widget that basically use the Recenter widget from MapFish.  It's a textbox
field where the user can input some text.  A request is send on the server and
matching results are returned in a dropdown list.  The selection of one element
from the list recenters the map to it.


XML Sample
------------
Sample configuration

.. code-block:: xml

   <mapfishrecenter>
     <name>W_MyMapFishRecenter</name>
     <options>
       <title>Search</title>
       <forcefilters>true</forcefilters>
       <defaultzoom>10</defaultzoom>
       <fields>
         <field>
           <queryparam>field1</queryparam>
           <displayfield>field1</displayfield>
           <label>Field #1</label>
           <filter>%#</filter>
         </field>
         <field>
           <queryparam>field2</queryparam>
           <displayfield>field2</displayfield>
           <label>Field #2</label>
         </field>
       </fields>
     </options>
   </mapfishrecenter>

drawWidget Sample
-------------------
The widget must be drawn with the *drawWidget* function.  See
:ref:`widget-basics-drawWidgets-label`.



Mandatory Options
-------------------
:fields/field/queryparam:   The field to be searched in the database
:fields/field/displayfield: The field to be shown in the combobox, can be
                            setted to a different value than the queryparam
:fields/field/label:        The label to be printed with the combobox


Optional Options
------------------
:fields/field/filter:       For this field to be used, the forcefilters 
                            parameter must be set to true.  The '%' are the
                            jokers and the '#' is replaced by the query. Setted
                            to '%#%' by default
:forcefilters:              Set to true to remove the radiobuttons and force
                            the filters per field
:defaultzoom:               The zoom level to zoom to when recentering on a 
                            Point geometry.

Service Type
--------------
featureserver


Widget Action
--------------
read
