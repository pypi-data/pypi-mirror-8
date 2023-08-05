Juno for py3o
=============

py3o.renderers.juno is a Java driver for py3o to transform
an OpenOffice document into a PDF

It is intended to be used in conjunction with `py3o.renderserver`_
But can be used outside it if you wish.

  .. _py3o.renderserver: https://bitbucket.org/faide/py3o.renderserver/

Note for end-users
==================

If you just search for an easy way to render LibreOffice files to PDF or DOCX, with ot without
templating capabilities, you should directly look at `py3o.fusion`_

`py3o.fusion`_ is a packaged webservice that lets you send a template, a target format and your data
 and will return the resulting file.

  .. _py3o.fusion: https://bitbucket.org/faide/py3o.fusion/

Prerequisites
=============

Since this is a Java implementation you will need to install
jpype and to have a recent Java runtime on the rendering machine.
You will also need a running OpenOffice instance. (If you are on
windows this can be addressed by using the py3o.renderserver
Open Office service.)

This has been tested to build correctly with:

  - Oracle JDK 1.6 and OpenOffice 3.2.1 on Windows 7 and Windows server 2003
  - Oracle JDK 1.6 and LibreOffice 3.4 on Windows 7 64bit
  - OpenJDK 6 and LibreOffice 3.4 on Linux (Ubuntu and RHEL 5)
  - OpenJDK 7 and LibreOffice 4.0.4 on Linux (Ubuntu 13.04)
  - OpenJDK 7 and LibreOffice 4.2.4.2 on Linux (Ubuntu 14.04)

For example if you are on Ubuntu you should run this command::

  $ sudo apt-get install default-jdk

Usage
=====

::

    from py3o.renderers.juno import start_jvm, Convertor, formats
    import datetime

    # first arg is the jvm.so or .dll
    # second arg is the basedir where we can find the basis3.3/program/classes/unoil.jar
    # third argument it the ure basedir where we can find ure/share/java/*.jar containing
    # java_uno.jar, juh.jar, jurt.jar, unoloader.jar
    # the fourth argument was the openoffice version but is no more used
    # fifth argument is the max memory you want to give to the JVM
    start_jvm(
            "/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so",
            "/usr/lib/libreoffice",
            "/usr/lib",
            "",
            140)
    c = Convertor("127.0.0.1", "8997")

    t1 = datetime.datetime.now()
    c.convert("py3o_example.odt", "py3o_example.pdf", formats['PDF'])
    t2 = datetime.datetime.now()

For more information please read the example provided in the examples dir and read the API documentation.

Installation
============

  $ pip install --upgrade py3o.renderers.juno

Requirements
~~~~~~~~~~~~

We just made a change of requirement from jpype to jpype1 in version 0.6 which should be pip installable by anyone with the correct toolchain. This means all requirements should now install automatically on a development machine.

Driver compilation and installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NOTE: this is optionnal and reserved for developpers who want to compile the jar file by themselves

If you want to install from source you'll need to clone our repository::

  $ hg clone http://bitbucket.org/faide/py3o.renderers.juno
  $ cd py3o.renderers.juno/java/py3oconvertor
  $ ./compilelibroffice.sh
  $ cd ../../
  $ python setup.py develop

Please note how you must first compile the jar file with our script (some more example scripts are available for windows and OpenOffice).
If something fails, first try to edit the script and find if all referenced jar files are present on your system.


