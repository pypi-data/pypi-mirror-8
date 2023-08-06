.. _widget-queryonclickwizard-label:

====================
 QueryOnClickWizard
====================

This widget automatically creates the following widgets :

  * :ref:`widget-queryonclick-label`
  * :ref:`widget-vectorlayer-label`
  * :ref:`widget-resultvectorlayer-label`

These are automatically created with pre-defined options that cannot be changed.
The query button is also automatically added to the toolbar as the **first**
element, right after the default controls.

.. warning:: This widget is only supported by the
             :ref:`config-pgsqlmapcontextconfig-label` driver.


XML Sample - draw
------------------
This widget doesn't need to be drawn.


Created widget *"default options"*
-----------------------------------
Here's the list of default options set for each widget created :

:QueryOnClick: drowDownList: false, multipleKey: shiftKey, noMarker: true, 
               toggle: true, displayClass: olControlQueryOnClickWizard
:VectorLayer: *No default options set*
:ResultVectorLayer: singleMode: true


Mandatory Options
-------------------
N/A


Optional Options
------------------
:iconCls:   (String) Defaults to 'queryonclickwizard'. Sets the *"iconCls"*
            option of the QueryOnClick widget created.
:layerName: (String) Sets the *"title"* option of the VectorLayer widget
            created.


Service Type
--------------
wms


Widget Action
--------------
read
