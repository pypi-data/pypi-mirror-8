.. _widget-featurepanel-selector-label:

========================
 FeaturePanel_Selector
========================

Widget that displays features attributes (fields) in a Ext.grid.GridPanel.  One
feature can be selected and opened in a custom form.  Each attribute (field)
that has to be displayed in the form must be defined in the options of the
widget.  In addition, the field must also be defined in the corresponding
DataStore.

There must be an featurepanel_selector for each resources that are to be shown.

The following widgets can use the FeaturePanel_Selector widget (using the
<featurepanel> tag option if only one or <featurepanel> inside <featurepanels>
if more than one) :

  * :ref:`widget-queryonclick-label`.


XML Sample
------------
Sample configuration

.. code-block:: xml

   <featurepanel_selector>
     <name>W_MyFeaturePanel_Road</name>
     <options>
       <template>http://myserver/url/to/myroad.php</template>
       <width>600</width>
       <height>400</height>
       <fid>ogc_fid</fid>
       <fields>
         <field>
           <name>ID</name>
           <type>key</type>
         </field>
         <field>
           <name>ogc_fid</name>
           <type>value</type>
         </field>
       </fields>
     </options>
   </featurepanel_selector>


drawWidgets Sample
-------------------
The widget must be drawn with the *drawWidgets* function.  See
:ref:`widget-basics-drawWidgets-label`.

Can be drawn in a Ext.Panel or Ext.Window.


Mandatory Options
-------------------
:fid:                String.  The primary key for this resource.
:fields/field/name:  The name of the field, as defined in the DataStore.  Can
                     be non-existant (in which case you should use "key" in
                     the type node)
:fields/field/type:  The type of the field. Insert "value" to print the value
                     of the field, "key" to print the name of the field



Optional Options
------------------
:width:  Integer.  The width of the template window. Default to 500.
:height:           Integer.  The height of the template window. Default to 500.
:template:         String.  The path to a custom form file. Mandatory if
                   'method' is undefined.
:method:           String.  The reference to a custom function returning a
                   new instance of an Ext.Container. Mandatory if
                   'template' is undefined.


Resources Options
-------------------
:selectorTitle: (String) Optional.  Sets title column's value.  Supports 
                :ref:`i18n-label`.


Service Type
--------------
wms


Widget Action
--------------
read
