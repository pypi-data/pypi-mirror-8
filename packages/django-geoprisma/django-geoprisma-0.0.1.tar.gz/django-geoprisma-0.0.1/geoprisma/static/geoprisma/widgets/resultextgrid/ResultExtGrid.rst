.. _widget-resultextgrid-label:

========================
 ResultExtGrid
========================

Widget that displays features attributes (fields) in a Ext.grid.GridPanel.  One
grid is created per defined resource (grid).

The following widgets can use the ResultExtGrid widget (using the <result>
tag) :

  * :ref:`widget-queryonclick-label`.


XML Sample
------------
Sample configuration, with only one resource (grid) defined

.. code-block:: xml

   <resultextgrid>
     <name>W_MyResultExtGrid</name>
     <options>
       <inwindow>false</inwindow>
       <grids>
         <grid>
           <displayname>My resource</displayname>
           <resourcename>R_MY_RESOURCE</resourcename>
           <delegatecontext>
             <enabled>true</enabled>
             <label>My Link</label>
           </delegatecontext>
           <fields>
             <field>
               <id>rol_co_cla</id>
               <label>Class</label>
               <type>float</type>
               <width>75</width>
             </field>
           </fields>
         </grid>
       </grids>
     </options>
   </resultextgrid>


Sample configuration, with more than one resource (grid) defined

.. code-block:: xml

    <resultextgrid>
      <name>W_MyResultExtGrid</name>
      <options>
        <inwindow>false</inwindow>
        <grids>
          <grid>
            <resourcename>R_GMAP_PARK</resourcename>
            <delegatecontext>
              <enabled>false</enabled>
              <label>Link to v2</label>
            </delegatecontext>
            <displayname>GMap Parks</displayname>
            <fields>
              <field>
                <id>NAME_E</id>
                <label>Name</label>
                <type>string</type>
                <width>200</width>
              </field>
              <field>
                <id>AREA</id>
                <label>Area</label>
                <type>float</type>
                <width>150</width>
              </field>
              <field>
                <id>PERIMETER</id>
                <label>Perimeter</label>
                <type>float</type>
                <width>150</width>
              </field>
              <field>
                <id>YEAR_EST</id>
                <label>Year</label>
                <type>integer</type>
                <width>50</width>
              </field>
            </fields>
          </grid>
          
          <grid>
            <resourcename>R_GMAP_POPP</resourcename>
            <delegatecontext>
              <enabled>false</enabled>
              <label>Link to v2</label>
            </delegatecontext>
            <displayname>GMap Cities</displayname>
            <fields>
              <field>
                <id>name</id>
                <label>Name</label>
                <type>string</type>
                <width>200</width>
              </field>
              <field>
                <id>reg_code</id>
                <label>Reg #</label>
                <type>integer</type>
                <width>50</width>
              </field>
              <field>
                <id>pop_range</id>
                <label>Population range (code)</label>
                <type>string</type>
                <width>150</width>
              </field>
              <field>
                <id>capital</id>
                <label>Capital (code)</label>
                <type>string</type>
                <width>100</width>
              </field>

            </fields>
          </grid>

          <grid>
            <resourcename>R_GMAP_PROV</resourcename>
            <delegatecontext>
              <enabled>false</enabled>
              <label>Link to v2</label>
            </delegatecontext>
            <displayname>GMap Provinces</displayname>
            <fields>
              <field>
                <id>NAME</id>
                <label>Name</label>
                <type>string</type>
                <width>150</width>
              </field>
              <field>
                <id>NAME_E</id>
                <label>Name (2nd)</label>
                <type>string</type>
                <width>150</width>
              </field>
              <field>
                <id>STATUS</id>
                <label>Status</label>
                <type>string</type>
                <width>100</width>
              </field>
              <field>
                <id>ISLAND_E</id>
                <label>Island Name</label>
                <type>string</type>
                <width>150</width>
              </field>
            </fields>
          </grid>
        </grids>
      </options>
    </resultextgrid>



drawWidget Sample
-------------------
The widget can be drawn with the *drawWidget* function if <inwindow> is set to
*false*.  See :ref:`widget-basics-drawWidgets-label`, else it's automatically
drawn in a Ext.Window.


Mandatory Options
-------------------
:inwindow:   (Boolean) Defaults to *true*.  Automatically draws the widget in a
             Ext.Window if set to *true*.  Setting this to *false* means you
             must draw it manually in a Ext.Panel with the standard drawWidget
             method.


Optional Options
------------------
:useResponseFields: (Boolean) Defaults to *false*.  If set to true, the 'grids'
                    option is ignored and all fields contained in the query
                    response are shown instead.
:grids:      Contains <grid> nodes.  At least one <grid> is mandatory when
             using this option.  If this option  and the 'useResponseFields' are
             not set, then no results are displayed.
:grids/grid/resourcename:            Name of the resource
:grids/grid/displayname:             Title that will appear at the top of the
                                     grid.  Usually the same value as the layer
                                     title.
:grids/grid/fields:                  Contains <field> nodes.  At least one is
                                     mandatory.
:grids/grid/fields/field/id:         Name of the field returned by the
                                     GetFeatureInfo request.
:grids/grid/fields/field/label:      Title of the column of the grid that will
                                     contain this field.
:grids/grid/fields/field/type:       Type of field.
:grids/grid/fields/field/width:      Width of the column of the grid.
:grids/grid/delegatecontext:         Must contains both *enabled* and *label*
                                     nodes if set.
:grids/grid/delegatecontext/enabled: Boolean.  If enabled, a DelegateContext
                                     button will appear at the top of the grid.
:grids/grid/delegatecontext/label:   Label on the DelegateContext button.



Service Type
--------------
wms


Widget Action
--------------
read
