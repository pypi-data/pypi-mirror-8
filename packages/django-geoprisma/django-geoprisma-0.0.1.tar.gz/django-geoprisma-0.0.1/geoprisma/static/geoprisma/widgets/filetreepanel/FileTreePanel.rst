.. _widget-filetreepanel-label:

==============
 FileTreePanel
==============

Use the Ext.ux.FileTreePanel widget to build a 'tree' of files.  Each file 
related to a resource that has a datastore linked to a 'file' service.  The
datastore can point to a file directly or a folder, thus allowing all files
of that folder to be read.

On load, the widget lunches a query to get the root of the service.  Each
resources the user have access to that have the according datastore linked to
this service will be fetched and added to the tree.


XML FileTreePanel
------------------
FileTreePanel configuration

.. code-block:: xml

    <filetreepanel>
      <name>MyFileTreePanelWidget</name>
      <options>
        <servicename>root_tmp</servicename>
      </options>
    </filetreepanel>


How to 'draw' the widget
-------------------------
This widget must be drawn using the **drawWidgets** method :
:ref:`widget-basics-drawWidgets-label`


Mandatory Options
------------------
:servicename: (String) The name of the **FileService** to use with this widget.


Optional Options
-----------------
This widget supports any options you could set to a Ext.ux.FileTreePanel widget.
Here's the most commonly used ones :

:downloadClick:     (String) Defaults to 'single'.  Can be either 'single' or
                    'double'.  The number of click required to download a file.
:enableNewFolder:   (Boolean) Defaults to false.  If set, enables the creation
                    of new folders feature.
:enableUpload:      (Boolean) Defaults to false.  If set, enables the uploading
                    new files feature.

                    .. note:: This options requires you to include the
                    Ext.ux.form.FileUploadField in your template file.  It is
                    not added in the printWidgetSource template.

:fileMaxSize:       (Integer) Defaults to 524288.  Specifies the max file size 
                    directive in the HTML form used when uploading files.
                    Only used when *enableUpload* is set.

                    .. note:: Consider setting up the **upload_max_filesize**
                              directive in php.ini as well.

:title:             (String) Defaults to the widget 'i18n_panel_title'
                    traduction string.  Sets the widget panel title.  This
                    option supports :ref:`i18n-label`.

Service Type
-------------
file


Widget Action
--------------

* read
* create
