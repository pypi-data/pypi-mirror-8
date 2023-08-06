.. _widget-featurepanel-customform-label:

=========================
 FeaturePanel_CustomForm
=========================

Widget that uses an external script to generate user-custom forms.  Used with
the editing widgets :

  * :ref:`widget-editfeature-create-label`
  * :ref:`widget-editfeature-update-label`

.. note:: This widget automatically link itselt to all the widgets above.

.. note:: This widget needs to be linked to the resources having custom forms.


XML Sample
------------
Sample configuration of the widget :

.. code-block:: xml

   <featurepanel_customform>
     <name>W_FeaturePanel_CustomForm</name>
     <options>
       <formURL>./path/to/script</formURL>
     </options>
   </featurepanel_form>


Mandatory Options
-------------------

:formURL: (String) URL path to the script managing the custom forms.


Optional Options
------------------
N/A


Service Type
--------------
featureserver


Widget Action
--------------
read
