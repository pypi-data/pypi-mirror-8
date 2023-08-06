.. _widget-featurepanel-form-label:

====================
 FeaturePanel_Form
====================

Widget that displays features attributes (fields) in a Ext.form.FormPanel.
Only one feature can be displayed at a time in the form.  Each attribute (field)
that has to be displayed in the form must be defined in the options of the
widget.  In addition, the field must also be defined in the corresponding
DataStore.

The FormPanel can be displayed in a Ext.Window if inWindow is set to true, else
it can be normally added to an existing panel in the template.

The following widgets can use the FeaturePanel_Form widget
(using the <featurepanel> tag) :

  * :ref:`widget-editfeature-create-label`
  * :ref:`widget-editfeature-update-label`


XML Sample
------------
Sample configuration of the widget :

.. code-block:: xml

   <featurepanel_form>
     <name>W_FeaturePanelForm_GMapCities</name>
     <options>
       <inwindow>true</inwindow>
       <windowoptions>
         <title>GMap cities edition</title>
         <autoScroll>true</autoScroll>
       </windowoptions>
       <defaults>
         <width>150</width>
         <listWidth>150</listWidth>
       </defaults>
       <fields>
         <field>
           <name>name</name>
           <xtype>textfield</xtype>
         </field>
         <field>
           <name>reg_code</name>
           <xtype>textfield</xtype>
         </field>
         <field>
           <name>pop_range</name>
           <xtype>combo</xtype>
         </field>
         <field>
           <name>capital</name>
           <xtype>combo</xtype>
         </field>
       </fields>
     </options>
   </featurepanel_form>

In addition to the widget definition, the DataStore must have some <field> nodes
defined.  If a field has <values> then any combobox created will have these 
values.  Example :

.. code-block:: xml

   <datastore>
     <name>DS_FS_DEV4G_GMAP_POPP</name>
     <service>S_FS_DEV4G</service>
     <params>
       <layers>gmap_popp</layers>
       <text>GMap Cities (FS)</text>
       <fields>
         <field>
           <name>name</name>
           <text>Name</text>
           <type>string</type>
         </field>
         <field>
           <name>reg_code</name>
           <text>Reg #</text>
           <type>integer</type>
         </field>
         <field>
           <name>pop_range</name>
           <text>Population</text>
           <type>integer</type>
           <values>
             <value>
               <value>1</value>
               <text>Less than 10,000</text>
             </value>
             <value>
               <value>2</value>
               <text>More than 10,000</text>
             </value>
             <value>
               <value>3</value>
               <text>More than 50,000</text>
             </value>
             <value>
               <value>4</value>
               <text>More than 100,000</text>
             </value>
             <value>
               <value>5</value>
               <text>More than 250,000</text>
             </value>
             <value>
               <value>6</value>
               <text>More than 500,000</text>
             </value>
           </values>
         </field>
         <field>
           <name>capital</name>
           <text>Type</text>
           <type>integer</type>
           <values>
             <value>
               <value>0</value>
               <text>City</text>
             </value>
             <value>
               <value>1</value>
               <text>National Capital</text>
             </value>
             <value>
               <value>2</value>
               <text>Province Capital</text>
             </value>
             <value>
               <value>3</value>
               <text>Territory Capital</text>
             </value>
           </values>
         </field>
       </fields>
     </params>
   </datastore>


Mandatory Options
-------------------
N/A

Optional Options
------------------
:inwindow:           Boolean.  Default is 'false'.  Display the panel in a
                     Ext.Window if set to 'true'.
:defaults:           The default properties of the ext items (fields) of the
                     panel.  Can be any Ext.form.'chosen_form_xtype' 
                     properties.  Here's some possible useful tags :
                     
                     * width
                     * editable
                     * mode
                     * triggerAction
                     * lazyRender
                     * lazyInit
                     * listWidth
  
.. seealso:: `ExtJS Documentation <http://www.extjs.com/deploy/dev/docs/>`_

:windowoptions:      The options used by the Ext.Window.  Any property set will
                     overwrite its corresponding default value.  Possible tags
                     can be any Ext.Window properties.  Some possible useful
                     tags :

                     * autoScroll: (optional) set to 'true' to allow 
                       autoscrolling inside the form
                     * title: (optional) the text to display in the title bar
                       of the window
                     
.. seealso:: `ExtJS Documentation - Ext.Window <http://extjs.com/deploy/dev/docs/?class=Ext.Window>`_

:fields:             contains <field> nodes


:field:              Must be set in the <fields> node.  Define each ExtJS
                     property you want the field to have here.  Possible tags
                     can be any Ext.form.'chosen_field' properties.  Some are
                     required :

                     * name: (required) the name of the field, as defined
                       in the DataStore
                     * xtype: (required) the type of form element to render the
                       field.  Currently support only two : combo, textfield
                     * isfid: (optional) indicates if the field should be sought
                       in the *id* geojson object rather than in the *properties* list
                     * width: (optional) the width of the element
                     * fieldLabel: (optional) to set a new fieldLabel property
                       if no <text> node was defined in the DataStore field or
                       if you simply want to redefine the text to display in
                       front of the element
                     * disabled: (optional) to set the field as **readonly**
                     * ... and any ExtJS property of the corresponding xtype...

Service Type
--------------
featureserver


Widget Action
--------------
read
