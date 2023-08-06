============================
Building mod_wsgi on Windows
============================

Overview
--------

Running Apache/mod_wsgi on Windows can be a bit tricky. The key is ensuring
that you are using the correct precompiled binary distributions of both
Apache and Python, and that you are using the correct version of Microsoft
Visual Studio.

There are three factors that need to be considered.

1. Ensuring that you are using either 32 bit or 64 bit versions of
everything. You cannot mix these. You either have to use all 32 bit, or all
64 bit.

2. That you are using a precompiled Apache binary built with the same
version of the Microsoft C/C++ compiler as the version of Python you are
using.

3. That you are using the correct version of Microsoft Visual Studio when
compiling mod_wsgi.

Python 2.6, 2.7, 3.2 (32 Bit Only)
----------------------------------

Use the latest Python 2.6, 2.7 or 3.2 binary available from the PSF:

* https://www.python.org/downloads/release/python-279/

You must use the 32 bit version which is labelled as:

* Windows x86 MSI installer

Python 2.6, 2.7 and 3.2 are compiled with the Microsoft C/C++ compiler from
Visual Studio 2008. This is referred to as being compiled for VC9.

You must therefore use a version of Apache compiled for VC9.

For Apache, you can use the binary available from ApacheLounge:

* http://www.apachelounge.com/download/additional/

There are only 32 bit versions available. You can use either the Apache 2.4
or 2.2 (legacy) versions.

For Microsoft Visual Studio 2008, you need to download it from Microsoft.

You have two options here. The first is to download the '.iso' images
described in the following post on StackOverflow.

* http://stackoverflow.com/a/15319069/128141

Use the one labelled as:

* VS 2008 Express SP1

The direct link is:

* http://download.microsoft.com/download/E/8/E/E8EEB394-7F42-4963-A2D8-29559B738298/VS2008ExpressWithSP1ENUX1504728.iso

If this stops working see the StackOverflow post in case an updated link
is added.

This version of Visual Studio can only compile 32 bit binaries. This is
okay as only a 32 bit binary for Apache is available from ApacheLounge for
VC9.

The second option for the Microsoft C/C++ compiler is that from:

* http://www.microsoft.com/en-us/download/details.aspx?id=44266

This can supposedely compile both 32 bit and 64 bit binaries but because
only a 32 bit version of Apache is available, you are still restricted to
using the 32 bit compiler. This variant of the Microsoft C/C++ compiler
hasn't been tried at this point.

Python 3.3, 3.4 (32 Bit)
------------------------

Use the latest Python 3.3 or 3.4 binary available from the PSF:

* https://www.python.org/downloads/release/python-279/

For Python 3.4 and 3.4 you have a choice of being able to use either
a 32 bit or 64 bit binary. Only use the 32 bit version.

You must use the 32 bit version which is labelled as:

* Windows x86 MSI installer

Python 3.3 and 3.4 are compiled with the Microsoft C/C++ compiler from
Visual Studio 2010. This is referred to as being compiled for VC10.

You must therefore use a version of Apache compiled for VC10.

For Apache, you can use the binary available from ApacheLounge:

* http://www.apachelounge.com/download/additional/

There are both 32 and 64 bit versions available for Apache 2.4. Only
use the 32 bit version.

For Microsoft Visual Studio 2010, you need to download it from Microsoft.

* http://www.visualstudio.com/downloads/download-visual-studio-vs#DownloadFamilies_4

Use the one labelled as:

* Visual C++ 2010 Express

This version of Visual Studio can only compile 32 bit binaries.

Installation
------------

Once Python, Apache and Visual Studio are installed, start up the Visual
Studio 2008/2010 Command Prompt window corresponding to the version of
Visual Studio required for your Python version. Make your way to this
directory. You then need to do:

1. Find the appropriate makefile in the directory for your combination
   of Apache and Python.
2. Edit the makefile and set the path to where you installed both Apache
   and Python.
3. Run ``nmake -f apXYpyXY.mk clean``. Subsitute 'XY' in each case for the
   version of Apache and Python being used.
4. Run ``nmake -f apXYpyXY.mk``. This will build mod_wsgi.
5. Run ``nmake -f apXYpyXY.mk install``. This will install the mod_wsgi
   module into the modules directory of your Apache installation.
6. Add the ``LoadModule`` line to the Apache configuration which was
   displayed when the ``install`` target was run.
7. Edit the Apache configuration as covered in mod_wsgi documentation or
   otherwise to have mod_wsgi host your WSGI application.
