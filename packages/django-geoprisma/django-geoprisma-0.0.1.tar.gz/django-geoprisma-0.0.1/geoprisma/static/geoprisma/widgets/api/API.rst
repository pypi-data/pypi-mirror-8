.. _widget-api-label:

=====
 API
=====

The main purpose of this widget is to act as an **API** for GeoPrisma. It can
be used as a single **point of entry** for external JavaScript libraries to
**interact** with GeoPrisma and its widgets.  It is done so using **methods**
and **events**, which are described in details below.

.. note:: 
 * it doesn't need to be defined in the config file
 * **must be included** in your xslt template file
 * doesn't need to be drawn
 * has no options


API Methods
------------

Each method receives a list of arguments and delegate them to an event they
trigger.  Widgets that need to interact with an event need to listen to it and
then react accordingly.

Here's the list of the currently supported methods, each defining their
required *arguments*, an *example* of use and the *widgets* using them.

applyFilters
~~~~~~~~~~~~~

This method fires the 'applyfilters' event.

*Arguments :*

:(Array): An array of hash objects containing the following keys and values :

          * **resource** (String) : the name of the resource to apply the filter
          * **filter** (OpenLayers.Filter) : the filter to apply to the
            resource.

*Example :*

.. code-block:: xml

  GeoPrisma.applyFilters([{
      resource: "R_Park",
      filter: new OpenLayers.Filter.Comparison({
          type: OpenLayers.Filter.Comparison.LIKE,
          property: "REG_CODE",
          value: "24"
      })
  }]);

*Widgets :*

* :ref:`widget-applyfilter-label`


applyFilter
~~~~~~~~~~~~

This method fires the 'applyfilters' event.

*Arguments :*

:(Object): A hash object containing the following keys and values :

          * **resource** (String) : the name of the resource to apply the filter
          * **filter** (OpenLayers.Filter) : the filter to apply to the
            resource.

*Example :*

.. code-block:: xml

  GeoPrisma.applyFilter({
      resource: "R_Park",
      filter: new OpenLayers.Filter.Comparison({
          type: OpenLayers.Filter.Comparison.LIKE,
          property: "REG_CODE",
          value: "24"
      })
  });

*Widgets :*

* :ref:`widget-applyfilter-label`

.. note:: This method fires the same event as the *applyFilters* one.  Its used
          to apply a single filter to a single resource using the object as the
          argument instead of an array.


getCenter
~~~~~~~~~~

This method returns a JavaScript object that contains the information about the
map center.

*Arguments :*

:(String): The projection code we want to have the coordinates displayed in.
           Defaults to the map 'displayProjection' or 'projection' if not set.

*Returns :*

:(Object): A hash object containing the information about the map center.  See
           the 'setCenter' method to know its list of possible keys and values.


*Example :*

.. code-block:: xml

  var center = GeoPrisma.getCenter("EPSG:4326");

.. note:: This method doesn't trigger any event. No external widgets takes
          action for this method.

setCenter
~~~~~~~~~~

This method fires the 'setcenter' event. Widgets listening to it will set the
map current center using user parameters sent and may perform other
widget-related actions.

If there are no widgets currently defined that could do so, the API widget takes
care of recentering the map, but nothing more.

*Arguments :*

:(Object): A hash object containing the following keys and values :

          * **projection** : (String) Optional. The coordinates projection code.
            Defaults to the map projection code if not set.
          * **x**    : (Float) Mandatory. The x coordinate of the center to set
          * **y**    : (Float) Mandatory. The y coordinate of the center to set
          * **zoom** : (Integer) Optional. The zoom level to use.  Defaults to
            the current map zoom level if not set.

*Example :*

.. code-block:: xml

  GeoPrisma.setCenter({
      x: -7912983,
      y: 6176194,
      zoom: 10,
      projection: "EPSG:900913"
  });


*Widgets :*

* :ref:`widget-geoextux-zoomto-label`: the widget will change the center of the
  map and add a marker (if the according option is set, see the widget
  documentation).


Util Methods
-------------

The following methods are available for use internally in GeoPrisma API and is
destined for development use.

getLayers
~~~~~~~~~~

*Returns :*

(Array) of OpenLayers.Layer objects that match the specified search options.

*Arguments :*

:(Object): A hash option that can have any or all of the following search
           criteria :

           * **resourceName** (String) : the resource name the layer must have.
           * **serviceType** (String) : the service type the layer must have.
             Possible values are any of the service **type** in lowercase.

             .. note:: The possible values for this option can be found
                       in this page : :ref:`concepts-service-label`. Look for
                       the **type** property.

*Example :*

.. code-block:: xml

  var matchLayers = GeoPrisma.getLayers({
      resourceName: "R_Park",
      serviceType: "wms"
  });


zoomToFeatureExtent
~~~~~~~~~~~~~~~~~~~~

See in code for more documentation.


Events
-------

In addition to methods, you can use the API widget events to collect information
specific to GeoPrisma and its components. They extend the Ext events, so
listening to them is done the same way.

Some of the events of the API widgets are managed and used internally and are
not meant to be used externally. They are considered private.  Those that can
be used to collect informations are considered public and are mentionned below.


centerchanged
~~~~~~~~~~~~~~
Fired everytime the map center changes, whether by using the setCenter method,
navigating the map, changing it programmatically, etc.

*Callback arguments :*

:(Object): A hash object containing the information about the map center.  See
           the 'setCenter' method to know its list of possible keys and values.


*Example :*

.. code-block:: xml

    GeoPrisma.on("centerchanged", function(values) {
        // do whatever you want with the "values" object
    }, this);


centermarkerchanged
~~~~~~~~~~~~~~~~~~~~
Fired everytime the center marker of a :ref:`widget-geoextux-zoomto-label`
widget changes, whether by using the setCenter method of the API widget, by
dragging it around or when it's removed.

*Callback arguments :*

:(Object): A hash object containing the information about the marker.  Same as
           'setCenter' method to know its list of possible keys and values.


*Example :*

.. code-block:: xml

    GeoPrisma.on("centermarkerchanged", function(values) {
        // do whatever you want with the "values" object
    }, this);


Service Type
--------------
N/A


Widget Action
--------------
read
