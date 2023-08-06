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
Windows is currently not supported by the pyuno driver (Patches are welcome!).
It is recommended to use the java based driver py3o.renderers.juno which is
really easier to deploy on Windows.

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

Example with explicit output format::

    from py3o.renderers.pyuno import Convertor

    c = Convertor()

    c.convert("py3o_example.odt", "py3o_example.out", "pdf")

Example with guessing the output format::

    from py3o.renderers.pyuno import Convertor

    c = Convertor()

    c.convert("py3o_example.odt", "py3o_example.pdf")

Example with explicit host and port::

    from py3o.renderers.pyuno import Convertor

    c = Convertor(host="127.0.0.1", port="8997")

    c.convert("py3o_example.odt", "py3o_example.pdf")

For more information please read the API documentation.

License
=======

This software is licensed under the MIT License


