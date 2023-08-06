==============
 Sample
==============

This is a blank *Sample* widget used for creating new ones.


XML Sample
------------
Sample configuration

.. code-block:: xml

    <sample>
        <name>MySampleWidget</name>
        <options>
            <foo>MyFooValue</foo>
        </options>
    </sample>


drawWidgets Sample
-------------------
pContainer is the name of the Ext.Panel object where to add the widgets :

.. code-block:: xslt

    <xsl:call-template name="sample:drawWidgets">
        <xsl:with-param name="pContainer">
            <xsl:text>oWestPanel</xsl:text>
        </xsl:with-param>
    </xsl:call-template>


Mandatory Options
-------------------
:foo: - The *foo* option is mandatory


Optional Options
------------------
:bar: The *bar* option is optional.


Service Type
--------------
wms


Widget Action
--------------
read
