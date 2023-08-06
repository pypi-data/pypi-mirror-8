.. _widget-initialview-label:

=============
 InitialView
=============

Widget that sets the initial center/extent of the map on page load in one of
the following ways :

* by using a **localView** defined as a widget option
* by using a resource **initViewUrlField** option and a specific service

Both use the page url to get the according parameter (and its value) required to
get the correct view informations.

.. note:: This widget is unbound, i.e. it doesn't need to be linked a resource.

.. note:: In order to be able to use resources views, a resource requires
          some options (see in resource options below) and must at least have
          one datastore served by a service of one of the following type :

          * featureserver
          * wfs (**recommended**)

XML Sample
-----------

A basic widget definition with **localViews** :

.. code-block:: xml

    <initialview>
      <name>W_InitialView</name>
      <options>
        <localViews>
          <localView>-7972075,6190176</localView> <!-- 1 Saguenay -->
          <localView>-8199582,5710712</localView> <!-- 2 Montreal -->
          <localView>-13709010,6323890</localView> <!-- 3 Vancouver -->
        </localViews>
        <maxZoom>9</maxZoom>
        <replaceZoomToMaxExtent>true</replaceZoomToMaxExtent>
      </options>
    </initialview>


How to "draw" the widget
-------------------------

This widget doesn't need to be drawn.


Mandatory Options
------------------
N/A


Optional Options
-----------------

:allowLayerToggling: (Boolean) Defaults to true. Whether to toggle the resource
                     layers visibility upon centering on a resource view or not.
:highlight: (Boolean) Defaults to false. Adds vector features on the map for
            each features returned by the query. If the *vectorLayer* option is
            set, it will use that layer, else creates one.
:localViewField: (String) Defaults to *localViewField*. Sets the parameter to
                 use in the page url to access the localViews.
:localViews/localView: (String) A comma-separated list of coordinates
                       representing a view accessible locally (without using a
                       resource). Can be a point location using 2 coordinates
                       (x,y) or an extent with 4 (left,bottom,right,top).
                       To use a localView, set the localViewField value as a
                       parameter in the page url with value equal to the index
                       of the localView wanted.

                       .. note:: The index of localViews starts at 1, not 0.
                       
:localView: (String) When using only one localView, use this option instead. See
            previous option for more.

            .. note:: Use *localViewField=1* when using this option.

:maxZoom: (Integer) The maximum level that can be zoomed to by this widget.
:replaceZoomToMaxExtent: (Boolean) Defaults to false. If set, replaces the map
                         zoomToMaxExtent method for one recentering on the view
                         instead.
:vectorlayer: (String) The name of the :ref:`widget-vectorlayer-label` widget to
              use for highlight purpose. Only used if *highlight* option is set.

              .. warning:: The :ref:`widget-vectorlayer-label` widget must be
                           defined **before** this widget in order for this
                           option to work, otherwise the layer won't be created
                           yet when this widget tries to use it.


Resource Options
-----------------

:initViewUrlField: (String) Mandatory if you want to use a resource view.  Sets
                   the parameter to use in the page url to access a view of the
                   resource.

                   .. note:: This value doesn't need to be unique for a
                             resource. If a same url field is used by multiple
                             resources, they will all attempt to get the
                             according view. The first returning a valid one
                             will be used and others ignored.


Service Types
--------------

If you want to use resourceViews, the resource requires to have the above
mandatory options and it must also be linked to a service of one of following
types :

* featureserver

  .. note:: Requests to get the views are synchronous when using featureserver, 
            so the page might take a while to load. The page still uses the
            original map center at first, then if a view is valid the map will
            zoom to its location.

* wfs (**recommended**)

  .. note:: Requests to get the features are asynchronous when using wfs, so
            the page will load using the original map center at first, then if
            a view is returned the map will zoom to its location.


Widget Action
--------------
read

