==============================
 GeoExtux_RedLiningPanel
==============================

This widget is directly taken from the GeoExt.ux eXtensions.  Basically, it's
a panel that controls drawing and editing of vector features on a blank vector
layer.  It's also possible to import external features from files and to do the
same for export.

.. seealso::

   http://trac.geoext.org/wiki/ux/Redlining

.. note::

   Resources linked to this widget won't have their vector layer linked to it.
   This is a feature that should be available when the widget would support
   multiple layers.

.. note::

   This widget should be included only once.


XML Sample
------------
Sample configuration.

.. code-block:: xml

    <geoextux_redliningpanel>
      <name>W_MyRedLiningPanel</name>
      <options>
        <title>MyRedLiningPanel</title>
      </options>
    </geoextux_redliningpanel>


Sample configuration with import disabled

.. code-block:: xml

    <geoextux_redliningpanel>
      <name>W_MyRedLiningPanel</name>
      <options>
        <import>false</import>
      </options>
    </geoextux_redliningpanel>


How to 'draw' the widget
---------------------------------
You can either *draw* the widget in a standard panel with the *drawWidgets* 
template **or** add it to a *GeoExtToolbar* widget.  

.. warning::

   You can't draw this widget in toolbar and a panel at the same time.

.. note::

   When added to a toolbar, the options normally in the panel won't be
   availables.  Only the widget buttons are added to the toolbar.


Here's an example on how to add the widget to a GeoExtToolbar :

.. code-block:: xml

    <geoexttoolbar>
      <name>W_MyGeoExtToolbar</name>
      <options>
        <widgets>
          <widget>W_MyGeoExtuxRedLiningPanel</widget>
        </widgets>
      </options>
    </geoexttoolbar>

Here's an example on how to draw the widget in a panel with the *drawWidgets* 
template

.. code-block:: xml

   <xsl:call-template name="geoextux_redliningpanel:drawWidgets">
     <xsl:with-param name="pContainer">
       <xsl:text>oWestPanel</xsl:text>
     </xsl:with-param>
   </xsl:call-template>


Mandatory Options
-------------------
There are no mandatory options for this widget.


Optional Options
------------------
You can define any valid *Ext.form.FormPanel* options.  Here are some of them
you might find useful to define :

:title: The text to display on top of the panel.

Here's the list of *widget-specific* options you can define

:import: Can be *true* or *false*.  If not defined, *true* is the default value.
         Add the *import* button.
:export: Can be *true* or *false*.  If not defined, *true* is the default value.
         Add the *export* button.
:styler: The type of styler to use (none used if not defined, which is the
         default behavior).  Possible values are : *combobox*.
:popupOptions: Can have any GeoExt.Popup valid option.  See below for some
               examples.
:popupOptions/anchored: Can be *true* or *false*.  If not defined, *true* is
                        the default value.  Anchors the popup to the feature.
:popupOptions/unpinnable: Can be *true* or *false*.  If not defined, *true* is
                          the default value.  Allows the popup to be 
                          *unanchored* to the feature.
:popupOptions/draggable: Can be *true* or *false*.  If not defined, *false* is
                         the default value.  While the popup is *anchored* to
                         a feature, it mustn't be draggable.  If you want to
                         set this to *true*, you must set both *unpinnable* and
                         *anchored* options to *false*.
:vectorlayer: (String) The name of the :ref:`widget-vectorlayer-label` widget
              to use its defined OpenLayers.Layer.Vector instead of letting
              this widget creating its own.


Service Type
--------------
N/A


Widget Action
--------------
N/A
