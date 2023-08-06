.. _widget-keepactivesession-label:

========================
 KeepActiveSession
========================

Occasionally send empty request to preserve session active until the user close
browser or geoprisma application.

XML Sample
------------
Sample configuration

.. code-block:: xml

   <keepactivesession>
     <name>W_MyKeepActiveSession</name>
     <options>
     </options>
   </keepactivesession>

drawWidget Sample
-------------------
This widget doesn't need to be drawn.


Mandatory Options
-------------------
N/A


Optional Options
------------------

:delay:     (Integer) Number of seconds to wait between each keep alive request. The default is 300 sec.
:url:       (string) Url that you want to check, maybe you'd like to do some sever side stuff or just remove the geoprisma error of calling proxy without oemservice. The default is your proxy.


Service Type
--------------
N/A


Widget Action
--------------
read
