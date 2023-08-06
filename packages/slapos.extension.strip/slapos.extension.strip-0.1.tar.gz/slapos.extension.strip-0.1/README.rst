Buildout Extension to strip binaries
====================================

slapos.extension.strip is a buildout extension that finds shared
libraries, binary executables and static libraries, and calls strip(1)
against them to reduce the size. It is triggered at the end of the
buildout process.

Usage
-----

Add ``slapos.extension.strip`` in ``[buildout]`` section's ``extensions`` option like :

::

  [buildout]
  extensions = slapos.extension.strip

Requirements
------------

The following programs are required. If any of them is missing, this
extension does nothing.

- ``file``
- ``find``
- ``strip``

Supported Options
-----------------

``file-binary``

  Path to ``file`` program. Defaults to 'file' which should work on
  any system that has the make program available in the system
  ``PATH``.

``find-binary``

  Path to ``find`` program. Defaults to 'find' which should work on
  any system that has the make program available in the system
  ``PATH``.

``strip-binary``

  Path to ``strip`` program. Defaults to 'strip' which should work on
  any system that has the make program available in the system
  ``PATH``.
