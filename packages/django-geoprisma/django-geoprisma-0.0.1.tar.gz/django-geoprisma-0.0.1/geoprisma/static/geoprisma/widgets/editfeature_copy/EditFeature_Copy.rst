.. _widget-editfeature-copy-label:

==================
 EditFeature_Copy
==================

Use the OpenLayers.Control.ModifyFeature control to allow copy/pasting vector
features on the map on a specific resource.

.. note:: Must be added to a GeoExtToolbar widget.


XML Sample
------------
Sample configuration of the widget :

.. code-block:: xml

   <editfeature_copy>
     <name>W_MyEditFeature_Copy</name>
     <options>
       <offset>-15,20</offset>
       <toggleEdit>true</toggleEdit>
     </options>
   </editfeature_copy>


Mandatory Options
-------------------
N/A


Optional Options
------------------
:offset: (String) The **X,Y** offset in pixel units the copied feature should
         be moved from its original. Two integer comma-separated values, first
         for X second for Y. Negative X means "to the left".  Negative Y means
         "to the bottom". Example : **-33,47**, means : "33 pixels to the left
         and 47 pixels to the top".
:toggleEdit: (Boolean) Defaults to false. Only usable if an EditFeature_Update
             widget is linked to the same resource of this widget. If set to
             *true*, on feature drag complete, won't commit the changes.
             Delegate the feature to the update control instead.


Resource options
-----------------
:copyFieldList: (String) A comma-separated list of resource field names.  When
                a feature is copied, if this option is not set (default), then
                all resource fields are copied.  If set to blank, then no fields
                are copied, else only the defined fields are copied.


Resource Options
------------------
:selectorMethod: (String) Only used if this widget has no 'featurepanel' option
                 set. After inserting a single feature, open a window containing
                 what this method returns.
:selectorTemplateHeight: (Integer) If set, defines the height of the window
                         opened after a single insert.  Only used when
                         "selectorMethod" resource option is set.
:selectorTemplateWidth: (Integer) If set, defines the width of the window
                         opened after a single insert.  Only used when
                         "selectorMethod" resource option is set.

Service Type
--------------
featureserver


Widget Action
--------------
create
