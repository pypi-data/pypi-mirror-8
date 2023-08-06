How to release this package
===========================

Commit everything in your working directory. Make sure you have no
outstanding changes.

run::

  $ python setup.py release

This will create a dist directory with diverse files. Inspect the
resulting zip and tar.gz files. Those are the source distributions.

They should contain everything a developper needs to work on the project
 or rebuild from source. Take great care to make sure every asset file is
 present in those source dists because they are commonly used by Linux
 distribution packagers to rebuild your project.

If any asset file is missing from the source dists you should edit MANIFEST.in
to point distutils to it.

.. note::
   Beware of installing wheel package before running python setup.py release

Now you're ready
================

Make sure you have a pypi account and you already logged into it with
distutils. (ie: it works)

run the following command::

  $ python setup.py release_upload

This will push all files to pypi.

You're not done YET
===================

Immediately after a successful push to pypi you MUST tag the project.
Do so by using the same version number as the one in setup.py!

Then IMMEDIATELY after tagging the project you MUST bump the setup.py version
to the next development version. (if you see 0.3 in there and just created
a "0.3" tag, then you should write 0.4 in setup.py)

Commit this version bump. And do not forget to PUSH it to bitbucket!!

Why?
====

Because this ensures a few things: first a tag always points to the same
version number that can be found on pypi.

Secondly this ensures that anyone that just clones our repository and
begins hacking, either with `setup.py develop` or `setup.py install` will
have the dev version and not the same version as the release one.

You'll note that his version will also be appended with `dev` ie: if setup.py
contains version = "0.4" the developper's version in site-packages will
be 0.4dev

Believe me on this... it will save you headhaches down the road!

A last word
===========

Once a package is uploaded to pypi you MUST NEVER re-upload the same
package without first bumping versions an tags. NEVER ... EVER...

Even if you realise you released a bug... (hell, shit happens!) just fix your
bug, replay this release procedure and upload a new version with your bugfix.
