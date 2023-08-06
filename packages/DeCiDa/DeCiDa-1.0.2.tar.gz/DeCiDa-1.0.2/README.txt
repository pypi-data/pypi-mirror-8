**DeCiDa Data Analysis and Procedural Simulation Python Library**
=================================================================

DeCiDa == Device and Circuit Data Analysis.

DeCiDa is a Python Library of functions and classes for
device characterization, circuit design and data analysis.

DeCida is written in pure python (2.7), and requires no code-compilation.
It is portable to any operating system where python is installed, and runs
under MacOS, Windows, Cygwin, and Linux.  Many DeCiDa classes and functions
require the numpy and Tkinter packages.

For circuit analysis, DeCiDa provides a flexible scripting class for
performing simulations with various circuit simulation tools, such as
(Synopsys) HSpice, (Cadence) Spectre, (Silvaco) SmartSpice,
(UC Berkeley) NGspice and others.
The Tckt class is used to provide a database of process corners for
each project, and to provide netlist templating for performing procedural
simulations and post-processing.
Scripts using Tckt access the database to obtain
the corner conditions, modify the netlist, and allow full python looping
structures for running the simulation, viewing and analyzing
the simulated data.

For data analysis, DeCiDa provides a Data class for reading-in and 
analyzing data in a number of formats, including nutmeg
(NGspice, Spectre, LTspice), CSDF (HSpice), CSV (comma-separated value),
SSV (space-separated value), and others.
The Data object can be viewed using the XYplot, Histogram or DataViewx classes.
DataViewx has commands via menu entries to manipulate and plot the data in
different ways, including frequency versus time, eye- and scope-diagrams
and column calculations.

DeCiDa started out as a Tcl/Tk application for analyzing measurements
of electron devices for performing routine compact-model parameter extraction.
To do this fitting, a least-squares optimization algorithm was used.
This python version of DeCiDa has a function LevMar (for Levenberg-Marquardt),
based on the mpfit package.  It is still under development.

What is in the distribution
---------------------------

* The decida python library of functions and classes (./decida).
  This is installed into the site-packages directory.

* A test library under decida.test for testing the distribution (./decida/test).
  This is also installed into the site-packages directory.

* Applications in the distribution bin directory (./bin).
  These are installed into the python bin directory.

* HTML documentation of the functions and classes (./doc/html).
  This is not installed.

* Tool-specific scripts (./etc):

   * simulation tool wrappers (./etc/wrappers)

      Circuit simulation tool wrappers that DeCiDa interfaces with.
      These are installed into ~/.DeCiDa/bin

   * cython (./etc/cython)

      Setup scripts for using cython to compile the Data and XYplotx classes.
      These are installed into ~/.DeCiDa/cython

   * dot files (./etc/dot)

      Several resource files to be placed in user home directory
      for Cadence and python.
      These are installed into ~/.DeCiDa/dot

   * user local lib directory (./etc/lib)

      A place to put user python code.
      This is set up as ~/.DeCiDa/lib

   * models (./etc/models)

      Case-corners and models for two example technologies from
      the Predictive Technology Models web-site.
      These are installed into ~/.DeCiDa/models

   * projects (./etc/projects)

      Two example project simulation directories (bird and trane).
      These are installed into ~/.DeCiDa/projects

   * Cadence skill files (./etc/skill)

      Several scripts for automatically generating DeCiDa python
      procedural simulation scripts,
      and verilog test-bench environments.
      These are installed into ~/.DeCiDa/skill

   * stdcell (./etc/stdcell)

      Two example standard cell libraries for the two example
      PTM technologies, from the NangateOpenCell Library.
      These are installed into ~/.DeCiDa/stdcell

   * verilog (./etc/verilog)

      Files for running Cadence NCsim and viewing the results using SimVision.
      These are installed into ~/.DeCiDa/verilog


DeCiDa applications
-------------------

All of these should be in the path after installation:

+----------------------+---------------------------------------------------------------------------------------------+
| application:         | description:                                                                                |
+======================+=============================================================================================+
| calc                 | scientific calculator                                                                       |
+----------------------+---------------------------------------------------------------------------------------------+
| dataview             | read, plot and analyze data                                                                 |
+----------------------+---------------------------------------------------------------------------------------------+
| plotter              | plot Cartesian, Parametric, or Polar functions                                              |
+----------------------+---------------------------------------------------------------------------------------------+
| twin                 | text editor, with additional capability                                                     |
+----------------------+---------------------------------------------------------------------------------------------+
| gifimg               | create embedded GIF image python class from a GIF image                                     |
+----------------------+---------------------------------------------------------------------------------------------+
| pllss                | plot PLL small-signal transfer functions, S-domain and Z-domain                             |
+----------------------+---------------------------------------------------------------------------------------------+
| pll_phase_noise      | plot PLL phase noise components and total phase noise                                       |
+----------------------+---------------------------------------------------------------------------------------------+
| ngsp                 | UC Berkeley NGspice gui                                                                     |
+----------------------+---------------------------------------------------------------------------------------------+
| op                   | read Cadence Spectre operating-point analysis, display node voltages and operating points   |
+----------------------+---------------------------------------------------------------------------------------------+
| create_sspice_script | create a Silvaco SmartSpice DeCiDa script                                                   |
+----------------------+---------------------------------------------------------------------------------------------+
| simvision_csv2col    | convert exported Cadence SimVision csv data to column data                                  |
+----------------------+---------------------------------------------------------------------------------------------+

Simulation tool wrapper scripts
-------------------------------

These scripts are installed in ~/.DeCiDa/bin

+--------------------+--------------------------------------+
| wrapper script:    | description:                         |
+====================+======================================+
| run_hspice         | wrapper to run Synopsys HSpice       |
+--------------------+--------------------------------------+
| run_ngspice        | wrapper to run UC Berkeley NGspice   |
+--------------------+--------------------------------------+
| run_sspice         | wrapper to run Silvaco SmartSpice    |
+--------------------+--------------------------------------+
| run_spectre        | wrapper to run Cadence Spectre       |
+--------------------+--------------------------------------+

Thanks to
---------

1. `Python distribution documentation <http://docs.python.org/2/distutils/index.html>`_, `more Python distribution documentation <http://guide.python-distribute.org/creation.html>`_ .
  
2. `Canopy installation documentation <https://support.enthought.com/entries/23389761-Installing-packages-into-Canopy-User-Python-from-the-command-line>`_ .

3. decida/ItclObjectx:

   Concepts from [incr Tcl], described in chapter 2, "Object-Oriented
   Programming with [incr Tcl]," by Michael McLennan, of "Tcl/Tk Tools,"
   Mark Harrision, 1997, O'Reilly. 

4. decida/FrameNotebook:

   Adapted from the Tcl/Tk example in
   Mark Harrison and Michael McLennan, "Effective Tcl/Tk Programming",
   1997, Addison-Wesley.

5. decida/Data.read_nutmeg method:

   Modified from the 
   `read_spice module <http://www.h-renrew.de/h/python_spice/spicedata.html>`_
   from Werner Hoch (python_spice-0.0.3).
    
6. decida/LevMar:

   Modified from the
   `mpfit module <https://code.google.com/p/astrolibpy>`_
   from Sergey Koposov, Craig Markwardt and Mark Rivers (mpfit_2013).

7. bin/gifimg:

   Modified from the 
   `img2pytk module <http://www.3dartist.com/WP/python/code/img2pytk.py>`_
   from Bill Allen (imageEmbedder-1.0).

8. Example model files:

   From `Predictive Technology Model <http://ptm.asu.edu>`_ from the
   Nanoscale Integration and Modeling (NIMO) group at Arizona State University.

9. Example standard cell libraries:

   From `Si2 <https://www.si2.org>`_ openEDA project, Nangate 45nm
   Open Cell Library, a generic open-source, non-manufacturable
   standard-cell library.

10. George Howlett, Michael McLennan, Sani Nassif, Mike Toth and others
    for developing many of the original concepts which are incorporated in
    DeCiDa.

11. Dean Gonzales, Sanquan Song and Phillip Johnson for supplying test
    data files and test-driving DeCiDa.

**Installing DeCiDa**
=====================

Download and prepare the distribution
-------------------------------------

* unzip/untar the distribution::

    tar xvfz DeCiDa.1.0.2-tar.gz

* cd into the distribution directory::

    cd DeCiDa-1.0.2

* you may want to install the DeCiDa html documentation (in ./doc/html)
  to an appropriate place for future reference.
  use a browser to read the documentation, using the url file:// specification
  to point to the index.html file in the html directory.

* manually modify the wrapper scripts in the distribution
  ./etc/wrapper directory (run_*), to point to correct tool locations.
  
  The wrappers have the following references to other tools.  
  Adjust these as needed, as required by your local environment.

+----------------+-------------------------------+
| wrapper:       | expected tool location:       |
+================+===============================+
| run_hspice     | /tools/hspice/bin/hspice      |
+----------------+-------------------------------+
| run_ngspice    | /opt/local/bin/ngspice        |
+----------------+-------------------------------+
| run_sspice     | /tools/silvaco/bin/sspice     |
+----------------+-------------------------------+
| run_spectre    | /tools/cds/bin/spectre        |
+----------------+-------------------------------+

Installing under Enthought Canopy
---------------------------------

* install in the Canopy Python User Virtual Environment

    refer to: `Installing packages into Canopy <https://support.enthought.com/entries/23389761-Installing-packages-into-Canopy-User-Python-from-the-command-line/>`_, `Canopy python default <https://support.enthought.com/entries/23646538-Make-Canopy-s-Python-be-your-default-Python-i-e-on-the-PATH->`_

* be sure that User python is in your path::

    python
    >>> import sys; sys.prefix

  you should see a path like one of the following::

    /Users/<user>/Library/Enthought/Canopy_32bit/User (MacOs)

    /home/<user>/Enthought/Canopy_32bit/User (Linux)


* install the distribution::

    python setup.py install

* you will find a new directory .DeCiDa in your home directory containing
  various tool specific scripts, models and other data

* the DeCiDa libraries are installed under site-packages

* the DeCiDa applications are installed in the python bin directory
  so they should be in the user path (may require a shell rehash)

Installing under (2.7) python
-----------------------------

* be sure that python2.7 is in your path::

    python
    >>> import sys; sys.prefix

  you should see a path like one of the following::

    /Library/Frameworks/Python.framework/Versions/2.7 (MacOS)

    /opt/local/lib/python2.7 (Linux)

* install the distribution::

    python setup.py install

Installing as a local library
-----------------------------

* DeCiDa can also be installed in a user's directory without requiring sysadmin
  privileges.

* select or make a directory for putting python libraries::

    mkdir ~/python/library

* copy the decida library to the python library in your home directory::

    cp -R ./decida ~/python/library

* edit the python resource file in ./etc/dot (.pythonrc.py).
  change the pylib definition appropriately to point to ~/python/library

* copy the resource file to your home directory::

    cp ./etc/dot/.pythonrc.py ~/.

* to use decida, import the user package, which imports ~/.pythonrc.py::

    >>> import user

* alternatively, define the PYTHONPATH environment variable to include
  ~/python/library in the path

* copy the applications to the user home bin directory::

    cp ./bin/* ~/bin

Test the distribution using the distribution tests
--------------------------------------------------

* test the distribution with one or more individual tests::

    python
    >>> import decida.test.test_Calc

  should display a calculator

    >>> import decida.test.test_Plotterx

  should display a plot and equation-set text-window

* list all of the tests::

     python
     >>> import decida.test
     >>> decida.test.test_list()

  should print all of the tests

* do all of the tests::

     python
     >>> import decida.test_all

  this may or may not complete depending on the sequence of closing windows

* the tests can also be run directly in the unzipped/tarred (pre-install) directory::

     cd DeCiDa-1.0.2/decida/test
     test_DataViewx_4.py

* test the applications installed in the python bin::

     twin

  should display a text-window (text-editor)

