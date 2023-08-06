.. _widget-geoexttoolbar-label:

========================
 GeoExtToolbar
========================

Add a navigation Ext.Toolbar to the UI.  OpenLayers controls are added to the
toolbar using GeoExt.Action. It contains the following controls by default :

 * Zoom to maximum map extent
 * Zoom in
 * Zoom out
 * Navigation
 * Last extent
 * Next extent

Beside the default buttons, it's possible to add other button in the toolbar
by using the <widgets> node in the <options> node.

.. note:: This widget must be added to the first widgets of the first resource
          or else it won't be drawn.  It is a bug that should be corrected in
          future releases.

.. note:: This widget must be defined only once.

.. note:: This widget deprecates the original Toolbar widget
          (which comes from the MapFish API).

.. warning:: This widget only works with ExtJS 3.0.0 or higher.


XML Sample
------------
Sample configuration of a toolbar with no widgets added.

.. code-block:: xml

   <geoexttoolbar>
     <name>W_MyToolbar</name>
     <options>
     </options>
   </geoexttoolbar>

Toolbar with more widgets added.

.. code-block:: xml

   <geoexttoolbar>
     <name>W_MyToolbar</name>
     <options>
       <widgets>
         <widget>W_MyQuery</widget>
         <widget>W_MyMeasureTool</widget>
       </widgets>
     </options>
   </geoexttoolbar>

Toolbar using a separator.

.. code-block:: xml

   <geoexttoolbar>
    <name>W_GeoExtToolbar</name>
     <options>
       <widgets>
         <widget>W_MeasureToolLength_One</widget>
         <widget>W_MeasureToolLength_Two</widget>
         <widget>W_MeasureToolLength_Three</widget>
         <widget>__separator__</widget>
         <widget>W_MeasureToolArea_One</widget>
         <widget>W_MeasureToolArea_Two</widget>
         <widget>W_MeasureToolArea_Three</widget>
       </widgets>
     </options>
   </geoexttoolbar>

Toolbar with custom controls.

.. code-block:: xml

    <geoexttoolbar>
      <name>GeoExtToolbar</name>
      <options>
        <controls>
          <control>Pan</control>
          <control>ZoomIn</control>
          <control>ZoomOut</control>
          <control>Separator</control>
        </controls>
        <widgets />
      </options>
    </geoexttoolbar>

drawWidgets Sample
-------------------
The toolbar widget must be drawn inside the GeoExt.MapPanel object. Here's an 
example :

.. code-block:: xslt

   oMyMapPanel = {
       id: 'gpDefaultMap',
       xtype: 'gx_mappanel',
       title: 'Map',
       layout: 'fit',
       region: 'center',
       border: false,
       height: 800,
       width: 800,
       <xsl:call-template name="geoexttoolbar:drawWidgets"/>
       map: oMap
   };

.. note:: The call-template must not be used as the last item since it outputs
          a ','.

          Here's an output example : *tbar: objGPWidgetW_MyToolbar,*


Mandatory Options
-------------------
N/A


Optional Options
------------------
:widgets:   Contains <widget> tags
:widgets/widget:    Must be in the <widgets> tag.  Name of a widget to add in
                    the toolbar.  It can also have "GeoPrisma-specific" values
                    such as :

                      * '__separator__' : to have a separator between the
                                          widgets defined.
                      * '__editfeature__' : to draw the editfeature widgets at
                                            this location in the toolbar

:scrollDelay: Can have an *integer* value or *false*.  Default is *100* if not
              set.  If set, only one zoom event will be performed after the
              delay when the *Navigation* control is active.
:controls:  Contains <control> tags.  If not defined, the default controls
            are automatically added to the toolbar, in a predefined order.
:controls/control:   Must be in the <controls> tag.  Add a specific control to
                     the toolbar.  The order of the <control> tags determines
                     the order they are added in the toolbar.  Possible values 
                     are (**Case sensitive**):

                     * *Separator*, add a separator
                     * *ZoomMax*, add a ZoomToMaxExtent control
                     * *ZoomIn*, add a ZoomIn control
                     * *ZoomOut*, add a ZoomOut control
                     * *Pan*, add a Navigation control.  Is automatically added
                       if not defined.
                     * *History*, add a NavigationHistory control with both 
                       *back* and *next* buttons.

                     .. note:: each control must appear only once.
:separateEditFeatureWidgets: (Boolean) Defaults to true.  Whether a separator
                             should be added between editfeature widgets from
                             different resources.

.. warning:: The old **widgets/separator** option has been replaced by
             **widgets/widget** with value equal to **__separator__**.  The old
             method is no longer supported.


Service Type
--------------
N/A


Widget Action
--------------
read
