Changelog
=========

0.5 2014-11-20
--------------

 * Ignore errors of ended spawned office clients if the cause of the error was a
   signal. Older versions of OpenOffice sometime fail with sigsev (11) after the
   document conversion.

0.4 2014-11-07
--------------

 * Allow to specify search path for the office installation
 * Allow to guess the output format from the output file extension
 * Support the system python environment when running the conversion
 * Support for older Office-/Libreoffice versions which don't understand --
   parameters (e.g. OpenOffice 3.2)

0.3 2014-10-14
--------------

 * Support for Mac OS X
 * Using the new common package for format declarations py3o.formats
 * Fixed problems with starting the OfficeSpawnedClient within the
   Open/-LibreOffice python environment
