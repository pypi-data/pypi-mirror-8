.. _widget-toggle-label:

========
 Toggle
========

This widget allow a layers from resources to follow the visibility of other
resources using the 'toggleResource' option.

The resource that has the 'toggleResource' option(s) is considered the 'mother'
resource.  Each defined 'toggleResource' follow this resource layers visibility.

.. note:: This widget must appear only once and doesn't need to be drawn.


XML Sample
------------
Sample configuration of the widget :

.. code-block:: xml

   <toggle>
     <name>W_MyToggle</name>
     <options />
   </toggle>


Sample configuration of a resource toggling an other :

.. code-block:: xml

    <resource>
      <name>R_GMAP_BASE</name>
      <datastores>
        <datastore>DS_TC_DEV4G_GMAP_BASE</datastore>
      </datastores>
      <widgets>
        <widget>W_Layer_TC_BASE</widget>
      </widgets>
      <options>
        <toggleResource>R_GMAP_PROV</toggleResource>
      </options>
    </resource>


Mandatory Options
-------------------
N/A


Optional Options
------------------
N/A


Service Type
--------------
N/A


Widget Action
--------------
read
