.. _widget-templatepopup-label:

===============
 TemplatePopup
===============

A button that, when activated, allow the user to click the map on WMS or Vector
features (fetched with WFS) (only one at a time) and display a single popup
displaying custom content about the first feature clicked.

The content of the popup is controlled by the 'templatepopup' resource option.


XML Sample
------------
Sample configuration

.. code-block:: xml

   <templatepopup>
     <name>W_TemplatePopup</name>
     <options>
     </options>
   </templatepopup>


drawWidget Sample
------------------
This widget doesn't need to be drawn, but must be added to the toolbar.


Mandatory Options
------------------
:title: (String) Popup title.
:serviceName: (String) Name of service to use to build URL. Can normally be
                either a **wms** or **wfs** service, but **wfs** services
                are not currently supported.
:queryVisible: (boolean) Defaults to 'true'. Set to 'false' to only query
                all available layers, ignoring visibility status.


Optional Options
-----------------
N/A


Resource Options
-----------------
:templatepopup: (String) Mandatory.  Content used to compile a new
                Ext.XTemplate object to display in the popup. Each resource that
                wants their according layer to display a popup must define this
                option.


Service Type
-------------
 * wms
 * wfs


Widget Action
--------------
read
