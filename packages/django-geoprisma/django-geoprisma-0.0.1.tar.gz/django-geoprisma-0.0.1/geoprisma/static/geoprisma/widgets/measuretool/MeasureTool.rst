.. _widget-measuretool-label:

=============
 MeasureTool
=============

Creates a MesureTool button menu containing "Length" and "Area and Perimeter"
measure tools.  The default units used are : metric and english.


XML Sample
-----------
Sample configuration with *Length* type

.. code-block:: xml

   <measuretool>
     <name>W_MeasureTool</name>
     <options />
   </measuretool>


How to draw the widget
-----------------------

The MeasureTool widget doesn't need to be drawn.  Instead, it must be added to
a GeoExtToolbar widget :

.. code-block:: xml

   <geoexttoolbar>
     <name>W_Toolbar</name>
     <options>
       <widgets>
         <widget>W_MeasureTool</widget>
       </widgets>
     </options>
   </geoexttoolbar>


Mandatory Options
-------------------
N/A


Optional Options
------------------
:units:         Contains <unit> tags
:units/unit:    Must be in the <units> tag.  Can be the name of the measure unit
                that you want to see appear in the measure window or the name of
                an units group able to show the must suitable unit for every
                situations. You can use one of the following groups :

                  * *metric* (km, m, cm)
                  * *english* (mile, foot)

                You can also add one of these simple unit :

                  * *50kilometers*
                  * *150kilometers*
                  * *BenoitChain*
                  * *BenoitLink*
                  * *Brealey*
                  * *CaGrid*
                  * *CapeFoot*
                  * *Centimeter*
                  * *ClarkeChain*
                  * *ClarkeFoot*
                  * *ClarkeLink*
                  * *Decameter*
                  * *Decimeter*
                  * *Dekameter*
                  * *Fathom*
                  * *Foot*
                  * *Furlong*
                  * *GermanMeter*
                  * *GoldCoastFoot*
                  * *GunterChain*
                  * *GunterLink*
                  * *Hectometer*
                  * *IFoot*
                  * *IInch*
                  * *IMile*
                  * *IYard*
                  * *Inch*
                  * *IndianFoot*
                  * *IndianFt37*
                  * *IndianFt62*
                  * *IndianFt75*
                  * *IndianYard*
                  * *IndianYd37*
                  * *IndianYd62*
                  * *IndianYd75*
                  * *IntnlChain*
                  * *IntnlLink*
                  * *Kilometer*
                  * *Lat-66*
                  * *Lat-83*
                  * *Meter*
                  * *MicroInch*
                  * *Mil*
                  * *Mile*
                  * *Millimeter*
                  * *ModAmFt*
                  * *NautM*
                  * *NautM-UK*
                  * *Perch*
                  * *Pole*
                  * *Rod*
                  * *Rood*
                  * *SearsChain*
                  * *SearsFoot*
                  * *SearsLink*
                  * *SearsYard*
                  * *Yard*
                  * *ch*
                  * *cm*
                  * *dd*
                  * *degrees*
                  * *dm*
                  * *fath*
                  * *ft*
                  * *in*
                  * *inches*
                  * *ind-ch*
                  * *ind-ft*
                  * *ind-yd*
                  * *km*
                  * *kmi*
                  * *link*
                  * *m*
                  * *mi*
                  * *mm*
                  * *nmi*
                  * *us-ch*
                  * *us-ft*
                  * *us-in*
                  * *us-mi*
                  * *us-yd*
                  * *yd*


:calibrationValue:  (Float) Used to set when the units swap in an units group
                the system will auto-select the closest superior value to the
                calibration value.
:geodesic:      (Boolean) Defaults to false. Set to true when the map is in a
                geodesic projection.
:immediate:     (Boolean) Defaults to true. Whether the partial measure should be
                updated on sketch immediate change (true) or single click (false).
:showLastSegmentMeasure: (Boolean) Defaults to false. Whether the measuse of the
                last segment should be displayed in the popup.
:tooltipAtCursor: (Boolean) Defaults to true. The information tooltip follow
                the cursor when user click.
:hectare:       *(Deprecated)* (Boolean) Defaults to false. Whether to add the
                hectare metric unit.


Service Type
--------------
N/A


Widget Action
--------------
read