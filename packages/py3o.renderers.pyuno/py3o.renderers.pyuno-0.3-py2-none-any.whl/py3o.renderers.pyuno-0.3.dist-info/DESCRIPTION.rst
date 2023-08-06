pyuno for py3o
==============

py3o.renderers.pyuno is a pyuno based driver for py3o to transform
an OpenOffice document into a PDF or other supported format.

Prerequisites
=============

You will need an installed version of Open-/LibreOffice.

This has been tested with LibreOffice 4.0 on Linux and LibreOffice 4.2 on
Mac OS X.

Important Note
==============

Windows
-------
If you are under Windows the pyuno driver will not work with your system python.
This will still work if you install everything inside the embedded python
shipped with Open-/LibreOffice. It is recommended to use the java based driver
py3o.renderers.juno which is really easier to deploy on Windows.

Linux / Mac OS X
----------------
If you are under Linux or Mac OS X, this driver will work with your system
python as long as pyuno is correctly installed. It is not possible to call the
pyuno bride directly if python shipped with Open-/LibreOffice has not the same
version as the system python. To circumvent this problem the driver tries to
determine the paths to the python version of Open-/LibreOffice and spawns a
child proccess for the conversion which runs within this python environment.

Usage
=====

Example::

    from py3o.renderers.pyuno import Convertor

    c = Convertor("127.0.0.1", "8997")

    t1 = datetime.datetime.now()
    c.convert("py3o_example.odt", "py3o_example.pdf", "pdf")
    t2 = datetime.datetime.now()

For more information please read the API documentation.

License
=======

This software is licensed under the MIT License


Changelog
=========

0.3 2014/10/14
--------------

 * Support for Mac OS X
 * Using the new common package for format declarations py3o.formats
 * Fixed problems with starting the OfficeSpawnedClient within the
   Open/-LibreOffice python environment
Contributors by alphabetic order
================================

  - Aide Florent
  - Björn Ricks

If anyone is missing to this list please let us know!


