Installation
************************

Library Installation
--------------------
You must have GNU Octave 3.6 or newer installed and in your PATH
(see instructions below).
Additionally, you must have the Numpy and Scipy libraries installed.  On Windows, you can get the install files here_.

The best way to install this library is by using pip_::

   pip install oct2py



.. _here: http://scipy.org/Download
.. _pip: http://www.pip-installer.org/en/latest/installing.html


GNU Octave Installation
-----------------------
- On Linux platforms, try your package manager, or follow the
  instructions from Octave_.  You must also have gnuplot installed, and
  gnuplot-x11, if available.

.. _Octave:  http://www.gnu.org/software/octave/doc/interpreter/Installation.html

- On Windows, download the latest MinGW or .NET version_.
  The MinGW version requires the 7zip_ program for installation.
  Make sure to install gnuplot if prompted.
  Finally, to add Octave to your path. You can do so from the Environmental Variables dialog for your version of Windows, or set from the command prompt::

      setx PATH "%PATH%;<path-to-octave-bin-dir>

.. _version: http://sourceforge.net/projects/octave/files/Octave%20Windows%20binaries/
.. _7zip: http://portableapps.com/apps/utilities/7-zip_portable
