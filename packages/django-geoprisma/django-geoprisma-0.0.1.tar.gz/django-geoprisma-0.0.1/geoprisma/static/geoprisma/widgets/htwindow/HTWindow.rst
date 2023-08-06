.. _widget-htwindow-label:

========================
 HTWindow
========================

Widget that create a window containing a web page.

.. note:: Does not work with cross domain pages.


XML Sample
------------

.. code-block:: xml

   <htwindow>
     <name>W_MyHTWindow</name>
     <options>
       <formurl>folder/page.php</formurl>
       <width>800</width>
       <height>600</height>
     </options>
   </htwindow>


How to 'draw' the widget
---------------------------------
This widget must be drawn inside a GeoExtToolbar widget :

.. code-block:: xml

    <geoexttoolbar>
      <name>W_MyHTWindow</name>
      <options>
        <widgets>
          <widget>W_MyHTWindow</widget>
        </widgets>
      </options>
    </geoexttoolbar>


Mandatory Options
-------------------

:width:   (Integer) Width of the window.
:height:  (Integer) Height of the window.


Optional Options
------------------

:formurl:       (String)  Relative or absolute URL to the page. Mandatory if
                'formmethod' is is undefined.
:formmethod:    (String) The reference to a custom function returning a
                new instance of an Ext.Container. Mandatory if 'formurl' is
                undefined.
:modal:         (Boolean) Defaults to *false*.  Whether the Ext.Window should be
                shown as 'modal' or not.
:iconcls:       (String) An alternative class name for the menu icon image.
                The class name should also be defined in a .css file.
:windowIconcls: (String) An alternative class name for the window icon image.
                The class name should also be defined in a .css file.
:windowIcon:    (Boolean) Defaults to *false*. Add the iconcls class to the window.
:tooltip:       (String) The tooltip to display when hovering the button.
:id:            (String) The id string to use for the Ext.Window object created.
:text:          (String) The text to display next in the Ext.Button created and
                as title for the Ext.Window.
:collapsible:   (Boolean) Defaults to *false*. Whether the Ext.Window should be
                'collapsible' or not.
:plain:         (Boolean) Defaults to *true*. True to render the window body with
                a transparent background so that it will blend into the framing
                elements, false to add a lighter background color to visually
                highlight the body element and separate it more distinctly from
                the surrounding frame.
:resizable:     (Boolean) Defaults to *false*. Allow user resizing at each edge
                and corner of the window.
:autoScroll:    (Boolean) Defaults to *true*. true to use overflow:'auto' on the
                components layout element and show scroll bars automatically when
                necessary, false to clip any overflowing content.
:constrain:     (Boolean) Defaults to *true*. True to constrain the window within
                its containing element, false to allow it to fall outside of its
                containing element. By default the window will be rendered to
                document.body.
:layout:        (String) Defaults to *fit*. Define the extJs layout of the window.


Service Type
--------------
N/A


Widget Action
--------------
N/A
