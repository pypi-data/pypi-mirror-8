.. _widget-getmouseposition-label:

========================
 GetMousePosition
========================

Widget that pops the mouse position in geographic value when the user clicks
on the map.

XML Sample
------------
Sample configuration

.. code-block:: xml

   <getmouseposition>
     <name>W_MyGetMousePosition</name>
     <options>
     </options>
   </getmouseposition>


Mandatory Options
-------------------
N/A


Optional Options
------------------
:displayProjectionString: (String) The EPSG string in which to display the
                          location clicked.  If not set, the projection of the
                          map is used.  If set to anything other than 
                          "EPSG:4326" and "EPSG:900913", then you need to load
                          the according proj definition first using **Proj4JS**.


Service Type
--------------
N/A


Widget Action
--------------
read
