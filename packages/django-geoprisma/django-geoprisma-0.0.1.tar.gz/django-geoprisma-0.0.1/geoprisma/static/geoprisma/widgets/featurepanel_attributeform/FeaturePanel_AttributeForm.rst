.. _widget-featurepanel-attributeform-label:

============================
 FeaturePanel_AttributeForm
============================

Widget that displays features attributes (fields) in a Ext.form.FormPanel.
Only one feature can be displayed at a time in the form.  Each attribute of a
feature being edited are automatically added to the form, all in plain text
boxes.

The following widgets can use this widget
(using the <featurepanel> tag) :

  * :ref:`widget-editfeature-create-label`
  * :ref:`widget-editfeature-update-label`


XML Sample
------------
Sample configuration of the widget :

.. code-block:: xml

   <featurepanel_attributeform>
     <name>W_MyFeaturePanelAttributeForm</name>
     <options>
     </options>
   </featurepanel_attributeform>


.. note:: This widget **requires** resource **fields** to work properly.

.. code-block:: xml

    <resource>
      <name>R_GMAP_POPP</name>
      <datastores>
        <datastore>DS_WMS_DEV4G_GMAP_POPP</datastore>
        <datastore>DS_FS_DEV4G_GMAP_POPP</datastore>
      </datastores>
      <widgets>
        <widget>W_CreatePoint</widget>
        <widget>W_FeaturePanelAttributeForm</widget>
      </widgets>
      <fields>
        <field>
          <name>name</name>
          <title>City name</title>
          <options/>
        </field>
      </fields>
    </resource>


Mandatory Options
-------------------
N/A


Optional Options
------------------
N/A


Service Type
--------------
featureserver


Widget Action
--------------
read
