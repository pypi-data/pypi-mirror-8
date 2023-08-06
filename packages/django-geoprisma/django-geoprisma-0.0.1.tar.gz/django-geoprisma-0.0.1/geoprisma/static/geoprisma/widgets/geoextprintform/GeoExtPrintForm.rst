.. _widget-geoextprintform-label:

==============================
 GeoExtPrintForm
==============================

A print widget that use the GeoExt print components to control print parameters
sent to the MapFishPrint service.  Their values come from the print service
capabilities.

It basically mimics the following GeoExt example :
  http://dev.geoext.org/trunk/geoext/examples/print-form.html


XML Sample
------------
Sample configuration.

.. code-block:: xml

    <geoextprintform>
      <name>W_GeoExtPrintForm</name>
      <options>
        <servicename>S_MapFishPrint</servicename>
        <defaultResolution>150</defaultResolution>
        <noRotationField>true</noRotationField>
      </options>
    </geoextprintform>


How to 'draw' the widget
---------------------------------
This widget must be drawn using the **drawWidgets** method :
:ref:`widget-basics-drawWidgets-label`


Mandatory Options
-------------------
:servicename: (String) The name of the MapFishService to use with this widget.
              The service **capabilities** will be used to populate the values
              of the fields of this widget (layout, resolution, scale, etc.)


Optional Options
------------------
:defaultMapTitle:   (String) Defaults to "" (empty string).  Sets the default
                    mapTitle value.  This option is ignored if the
                    'noMapTitleField' option is set to *true*.
:defaultComment:    (String) Defaults to "" (empty string).  Sets the default
                    comment value.  This option is ignored if the
                    'noCommentField' option is set to *true*.
:defaultLayout:     (String) Defaults to the first layout name from the
                    MapFishPrint service capabilities if not set.  Sets the
                    default layout name if its matches one of the capabilities
                    layouts.
:defaultResolution: (Integer) Defaults to first resolution value from the
                    MapFishPrint service capabilities if not set.  Sets the
                    default resolution value if its matches one of the
                    capabilities resolutions.
:ieWindowOpen:      (Boolean) Defaults to *false*.  Only used when using an     
                    Internet Explorer browser. If set to *true*, instead of
                    opening the PDF inside the same page, it's opened in a new
                    window. Be sure to allow popups from the page.
:mapTitleFieldLabel: (String) Overrides the default map title field label value.
                     This option supports :ref:`i18n-label`.
:mapTitleMaxLength: (Integer) Restruct the number of characters that can be
                    entered for the map title field.
:noMapTitleField:   (Boolean) Defaults to *false*.  If set to *true*, the
                    'mapTitle' form field won't be rendered and the default
                    value of this field becomes 'Printing Demo'.
:noCommentField:    (Boolean) Defaults to *false*.  If set to *true*, the
                    'comment' form field won't be rendered.
:noLayoutField:     (Boolean) Defaults to *false*.  If set to *true*, the
                    'layout' form field won't be rendered.
:noResolutionField: (Boolean) Defaults to *false*.  If set to *true*, the
                    'resolution' form field won't be rendered.
:noRotationField:   (Boolean) Defaults to *false*.  If set to *true*, the
                    'rotation' form field won't be rendered.
:noScaleField:      (Boolean) Defaults to *false*.  If set to *true*, the
                    'scale' form field won't be rendered.
:title:             (String) Defaults to the widget 'i18n_panel_title'
                    traduction string.  Sets the widget panel title.  This
                    option supports :ref:`i18n-label`.


Service Options
----------------
:vendor: (String) Layers created from a **wms** service with this option set to
         **mapserver** (case insentive) will make sure the GetMap requested by
         the print service are set according to the dpi currently set, which
         means if 300 dpi is set, then the images generated in the pdf document
         will be made in 300 dpi instead of 72.

         .. note:: This feature is supported in MapServer >= 5.6.


Service Type
--------------
mapfishprint


Widget Action
--------------
read
