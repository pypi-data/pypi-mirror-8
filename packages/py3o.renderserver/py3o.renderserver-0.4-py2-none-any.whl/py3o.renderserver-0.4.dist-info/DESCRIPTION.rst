Overview
========

This is a rendering server that will wrap an OpenOffice/LibreOffice server and provide
a pythonic API which is remotely callable.

The main advantage is that your client code does not need to import pyuno... This
is a main plus because pyuno is a pain to get working on Windows and some flavors of
Linux, don't even think of Mac :)

Once you deploy a py3o.renderserver all you need in your python code is to use the
py3o.renderclient which is really straightforward...

http://bitbucket.org/faide/py3o.renderclient

Requirements
============

Install the latest JDK for your plateform. Here is an example for Ubuntu 13.04::

  apt-get install default-jdk

This will give you the necessary tools to compile the juno driver.

You will need to install (and compile) the py3o.renderers.juno driver from here http://bitbucket.org/faide/py3o.renderers.juno

Follow the instructions from the driver's documentation to install it and then you're ready to start your own RenderServer

Running the server
==================

Here is how we start the server on a Linux host (Ubuntu 13.04)::

  $ start-py3o-renderserver --java=/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so --ure=/usr/lib --office=/usr/lib/libreoffice --driver=juno --sofficeport=8997

You MUST have a  running LibreOffice (OpenOffice) server somewhere. In our example it is running on localhost with port 8997. Here is how you can start such a server on Linux (Ubuntu 13.04 / LibreOffice 4.0.4)::

  $ libreoffice --nologo --norestore --invisible --headless --nocrashreport --nofirststartwizard --nodefault --accept="socket,host=localhost,port=8997;urp;"

As you can see it works with OpenJDK, LibreOffice and even on 64bit systems :)


