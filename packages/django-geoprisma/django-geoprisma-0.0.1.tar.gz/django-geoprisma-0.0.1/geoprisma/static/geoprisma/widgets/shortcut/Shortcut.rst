.. _widget-shortcut-label:

==============
 Shortcut
==============

Build a ExtJS dropdown list from features received from a featureserver or
wfs service.  This widget deprecates the QuickZoom widget.

There are two ways to draw this widget :

* in the GeoExtToolbar widget
  Simply add the widget to the GeoExtToolbar widget
* by using the standard "drawWidgets" method.  See how below.

Only one can be used at a time.  There is no way to have the Shortcut widgets inside the toolbar and in an external panel.


XML Sample
------------
Sample configuration with no activation

.. code-block:: xml

    <shortcut>
        <name>MyShortcutWidget</name>
        <options>
            <field>hap_nm_top</field>
        </options>
    </shortcut>

Sample configuration with highlight turned on

.. code-block:: xml

    <shortcut>
        <name>MyShortcutWidget</name>
        <options>
            <field>hap_nm_top</field>
            <highlight>true</highlight>
        </options>
    </shortcut>

Configuration with self Resource Activation

.. code-block:: xml

    <shortcut>
        <name>MyShortcutWidget</name>
        <options>
            <field>hap_nm_top</field>
            <selfActivate>true</selfActivate>
        </options>
    </shortcut>

Configuration with manual Resource Activation

.. code-block:: xml

    <shortcut>
        <name>MyShortcutWidget</name>
        <options>
            <field>hap_nm_top</field>
            <activeResources>
                <activeResource>
                    <name>MyResourceOne</name>
                    <servicetypes>
                        <servicetype>wms</servicetype>
                        <servicetype>featureserver</servicetype>
                    </servicetypes>
                </activeResource>
                <activeResource>
                    <name>MyResourceTwo</name>
                    <servicetypes>
                        <servicetype>wms</servicetype>
                    </servicetypes>
                </activeResource>
            </activeResources>
        </options>
    </shortcut>


drawWidgets Sample
-------------------
pContainer is the name of the Ext.Panel object where to add the widgets :

.. code-block:: xslt

    <xsl:call-template name="shortcut:drawWidgets">
        <xsl:with-param name="pContainer">
            <xsl:text>oWestPanel</xsl:text>
        </xsl:with-param>
    </xsl:call-template>


Mandatory Options
-------------------
:field:       The field to be displayed in the combobox.

Optional Options
------------------
:highlight: This node can be set to ``true`` or ``false`` (both lower case); if ``true`` the zoomed to feature will be highlighted according to the default (or user configured) ``selected`` style; defaults to ``false``
:maxFeatures: The maximum number of features the request must return.  
:defaultZoom: The level to zoom to when the Geometry of the features is 'Point'.
:selfActivate: Boolean.  When this widget is used, OpenLayers.Layer objects sharing the same Resource this widget uses are automatically shown.
:activeResources: 
    A list of Resources to activate when this widget is used.  Contains 
    activeResource nodes : 
    
    * activeResource
        * name - the name of the resource
        * servicetypes: (optional) contains servicetype nodes.
            * servicetype: can be any valid service type (i.e. 'wms', 'featureserver', etc.)
            
:emptyText: `i18n <../i18n.html>`_ - (ext) The default text displayed by default when no feature is selected.  If ommited, the DataStore 'text' node is used if defined, else the 'ResourceName' is used.  Plus, if the field 'text' node is defined, it's added to the string.
:fieldLabel: `i18n <../i18n.html>`_ - (ext) The default text displayed by default in front of the combobox.  If ommited, the DataStore 'text' node is used if defined, else the 'ResourceName' is used.  Plus, if the field 'text' node is defined, it's added to the string.
:width: (ext) The witdh of the combobox in pixels.

*Any Ext.form.ComboBox properties can also be used as an option.  Among theses, those above with (ext) are the most useful ones.*

.. warning:: The 'activeResources' option was previously 'resourcesToActivate'
             and its childs were 'resource' nodes.  These are not supported
             anymore.


Service Type
--------------
 * featureserver
 * wfs


Widget Action
--------------
read


