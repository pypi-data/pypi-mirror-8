Zero POS
========

A zeroconf based POS printing daemon

What is Zero POS
----------------

Zero POS was designed to solve a very specific problem we faced at
Openlabs, but we thought could be generic enough for others to use. Here
is the use case:

The Tryton iPad based POS should be able to print to the commonly found
POS printer - a thermal printer like the Epson TM-T81. The printer only
talks over USB and does not have wireless printing capabilities!

With zeropos, you could bundle the printer with a low cost computer like
the Raspberry Pi and connect the printer to it and run zeropos daemon on
the raspberry pi. The printing service can be discovered over zero conf
from the iPad application and your application could send a POST request
to the service to print ZPL to the printer.

Installation
-------------

The quickest way to install this software is using pip

:: 

    pip install zeropos


Administration
--------------

The daemon can be adminisered by opening the service URL from a browser.


TODO
----

1. Implement secutiry for the admin interface.
2. Write API documentation for the admin HTTP API.
