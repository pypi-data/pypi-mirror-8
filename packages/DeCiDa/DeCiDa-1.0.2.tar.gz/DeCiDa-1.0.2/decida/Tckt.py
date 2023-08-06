################################################################################
# CLASS    : Tckt
# PURPOSE  : benchmark test circuit class
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:25:47 2013
# -----------------------------------------------------------------------------
# NOTES    : 
#
# LICENSE  : (BSD-new)
# 
# This software is provided subject to the following terms and conditions,
# which you should read carefully before using the software.  Using this
# software indicates your acceptance of these terms and conditions.  If you
# do not agree with these terms and conditions, do not use the software.
# 
# Copyright (c) 2013 Richard Booth. All rights reserved.
# 
# Redistribution and use in source or binary forms, with or without
# modifications, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following Disclaimer
#       in each human readable file as well as in the documentation and/or
#       other materials provided with the distribution.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following Disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Richard Booth nor the names of contributors
#       (those who make changes to the software, documentation or other
#       materials) may be used to endorse or promote products derived from
#       this software without specific prior written permission.
# 
# Disclaimer
# 
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, INFRINGEMENT AND THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# ANY USE, MODIFICATION OR DISTRIBUTION OF THIS SOFTWARE IS SOLELY AT THE
# USERS OWN RISK.  IN NO EVENT SHALL RICHARD BOOTH OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, INCLUDING,
# BUT NOT LIMITED TO, CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
# DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
# THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
# IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
# NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
# MODIFICATIONS.
################################################################################
import user
import decida
from decida.ItclObjectx      import ItclObjectx
from decida.Data             import Data
from decida.XYplotx          import XYplotx
from decida.FrameNotebook    import FrameNotebook
from decida.TextWindow       import TextWindow
from decida.SelectionDialog  import SelectionDialog
from decida.Pattern          import Pattern
from string import Template
import sys
import os
import os.path
import stat
import string
import math
import re
import subprocess
import shutil
import time
class Tckt(ItclObjectx) :
    """ procedural simulation test-circuit class.

    **synopsis**:

    **constructor arguments**:

        .. option:: \*\*kwargs (dict)

           keyword=value specifications:

           configuration-options

    **configuration options**:

        .. option:: verbose        (bool, default=False)

            Enable/disable verbose mode.

        .. option:: project        (str, default="")

            Specify project name.  The project must be one of the
            supported projects (one of the Tckt._ProjectDB entries)

        .. option:: simulator      (str, default="spectre")

            Specify the circuit simulator. Must be one of:

                * hspice   : Synopsys HSpice

                * sspice   : Silvaco SmartSpice

                * ngspice  : UC Berkeley NGspice

                * spectre  : Cadence Spectre

        .. option:: simulator_args (str, default="")

            string of additional simulator command-line arguments

        .. option:: case           (str, default="case")

            specify the process/supply voltage/temperature case corner, by
            its name.  Must be one of the cases specified for the 
            current project, and one of the supported cases
            (specified in Tckt._CaseDB)

        .. option:: path           (list of str, default=["."])

            list of paths to search for the circuit netlist.

        .. option:: netlistfile    (str, default="")

            name of the netlist file

        .. option:: prefix         (str, default="")

            prefix to generated files.  Should be a unique name for
            each simulation.

        .. option:: title          (str, default="")

            title to be added to top of generated input file.

        .. option:: testdir        (str, default="")

            directory where tests are performed.  (Not currently used).

        .. option:: resultsdir     (str, default="")

            directory where simulation results are written.  If resultsdir
            is not specified, results are written to the current directory.

        .. option:: circuit        (str, default="")

            the name of the device under test.  This is a convenience name for
            documenting generated files.

        .. option:: temp_nom       (float, default=25.0)

            nominal simulation temperature.

        .. option:: temp_low       (float, default=_40.0)

            low simulation temperature.

        .. option:: temp_high      (float, default=150.0)

            high simulation temperature.

        .. option:: supply_nom     (float, default=1.0)

            nominal supply voltage value.

        .. option:: supply_low     (float, default=0.9)

            low supply voltage value.

        .. option:: supply_high    (float, default=1.1)

            high supply voltage value.

    **example**:

    **public methods**:

        * public methods from *ItclObjectx*

    """
    _SimulatorDB = {
        "spice"     : ["spice"],
        "hspice"    : ["spice"],
        "hspiceD"   : ["spice"],
        "sspice"    : ["spice"],
        "ngspice"   : ["spice"],
        "eldo"      : ["spice"],
        "eldoD"     : ["spice"],
        "adit"      : ["spice"],
        "nanosim"   : ["spice"],
        "finesim"   : ["spice"],
        "spectre"   : ["spectre"],
        "UltraSim"  : ["spectre"],
    }
    """ simulator database.
        key = simulator name
        data = netlist format (spice or spectre)
    """
    modeldir = os.path.expanduser("~/.DeCiDa/models/")
    _ProjectDB  = {
        "bird" : [
           "ptm_130nm", modeldir + "ptm_130nm.scs",
           ["tt", "ss", "ff", "fs", "sf"], "", ""
        ],
        "trane" : [
           "ptm_45nm",  modeldir + "ptm_45nm.scs",
           ["tt", "ss", "ff", "fs", "sf"], "", ""
        ],
        "generic" : [
           "ptm_45nm",  modeldir + "ptm_45nm.scs",
           ["tt", "ss", "ff", "fs", "sf"], "", ""
        ],
    }
    """ project database.

        key = project name

        data = technology, model-file, case-corner list,
        (for subcircuit mosfet models) nmos device in subcircuit,
        (for subcircuit mosfet models) pmos device in subcircuit

        example subcircit model:

            for subcircuit mosfet instance xm1, the
            subcircuit mosfet device might be xmnd2.xm1.mn,
            so the field should be ".xm1.mn"
    """
    _CaseDB = {
        "tt"   : [ 0, "tt",  "nom",  "nom" ],
        "ss"   : [ 1, "ss",  "high", "low" ],
        "ff"   : [ 2, "ff",  "low",  "high"],
        "sf"   : [ 3, "sf",  "nom",  "nom" ],
        "fs"   : [ 4, "fs",  "nom",  "nom" ],
        "ssc"  : [ 5, "ss",  "low",  "low" ],
        "ffh"  : [ 6, "ff",  "high", "high"],
    }
    """ database of case corner specifications.

        key = case corner name

        data = case corner index (case_key), process,
        temperature level, voltage-supply level

        temperature (and voltage-supply) levels are
        "nom", "low", or "high", corresponding to
        the Tckt temp_nom, temp_low, temp_high
        (and supply_nom, supply_low, supply_high)
        configuration options
    """
    @staticmethod
    def projects() :
        """ return valid projects in the database. """
        return Tckt._ProjectDB.keys()
    @staticmethod
    def project_tech(project) :
        """ return technology of project in the database. """
        if not project in Tckt._ProjectDB :
            return ""
        return Tckt._ProjectDB[project][0]
    @staticmethod
    def project_modelfile(project) :
        """ return modelfile of project in the database. """
        if not project in Tckt._ProjectDB :
            return ""
        return Tckt._ProjectDB[project][1]
    @staticmethod
    def project_cases(project) :
        """ return PVT case corners of project in the database. """
        if not project in Tckt._ProjectDB :
            return []
        return Tckt._ProjectDB[project][2]
    @staticmethod
    def spectre_dcop_mosfet_id_sort(mosfet1, mosfet2) :
        """ sort two mosfets according to drain current. """
        id1 = abs(string.atof(DevInfo[mosfet1 + "-ids"]))
        id2 = abs(string.atof(DevInfo[mosfet2 + "-ids"]))
        if   id1 <  id2 :
            return 1
        elif id1 == id2 :
            return 0
        else :
            return -1
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Tckt main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #===========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #===========================================================================
    def __init__(self, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__project       = None
        self.__tech          = ""
        self.__modelfile     = ""
        self.__cases         = []
        self.__xnmos         = ""
        self.__xpmos         = ""
        self.__case_key      = 0
        self.__process       = ""
        self.__vdd           = 0
        self.__temp          = 0
        self.__Element       = {}
        self.__netlistRemove = []
        self.__netlistpath   = None
        self.__netlistfooter = None
        self.__netlistparams = None
        self.__inputfile     = ""
        self.__outputfile    = ""
        self.__datafile      = ""
        self.__monitor       = ""
        self.__control       = ""
        self.__Veriloga      = {}
        self.__Stability     = {}
        self.__Postlayout    = {}
        self.__postlayout_instances = []
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        self._add_options({
            "verbose"        : [False, None],
            "project"        : ["",        self._config_project_callback],
            "simulator"      : ["spectre", self._config_simulator_callback],
            "simulator_args" : ["",    None],
            "case"           : ["case",    self._config_case_callback],
            "path"           : [["."],     self._config_path_callback],
            "netlistfile"    : ["",        self._config_netlistfile_callback],
            "prefix"         : ["",        self._config_prefix_callback],
            "title"          : ["",    None],
            "testdir"        : ["",    None],
            "resultsdir"     : ["",        self._config_resultsdir_callback],
            "circuit"        : ["",    None],
            "temp_nom"       : [25.0,  None],
            "temp_low"       : [-40.0, None],
            "temp_high"      : [150.0, None],
            "supply_nom"     : [1.0,   None],
            "supply_low"     : [0.9,   None],
            "supply_high"    : [1.1,   None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in kwargs.items() :
            self[key] = value
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Tckt configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #===========================================================================
    # METHOD  : _config_project_callback
    # PURPOSE : set project and parameters
    #===========================================================================
    def _config_project_callback(self) :
        project = self["project"]
        if project in Tckt._ProjectDB :
            self.__project   = project
            self.__tech      = Tckt._ProjectDB[project][0]
            self.__modelfile = Tckt._ProjectDB[project][1]
            self.__cases     = Tckt._ProjectDB[project][2]
            self.__xnmos     = Tckt._ProjectDB[project][3]
            self.__xpmos     = Tckt._ProjectDB[project][4]
        else :
            self.fatal("project \"" + project + "\" not supported")
    #==========================================================================
    # METHOD : Tckt::_config_simulator_callback
    # PURPOSE : simulator configuration callback
    #==========================================================================
    def _config_simulator_callback(self) :
        simulator = self["simulator"]
        if simulator in Tckt._SimulatorDB :
            self._netlist_format = Tckt._SimulatorDB[simulator][0]
        else :
            self.fatal("simulator \"" + simulator + "\" not supported")
    #===========================================================================
    # METHOD  : _config_case_callback
    # PURPOSE : set named process corner
    #===========================================================================
    def _config_case_callback(self) :
        case = self["case"]
        if case in Tckt._CaseDB :
            self.__case_key = Tckt._CaseDB[case][0]
            self.__process  = Tckt._CaseDB[case][1]
            corner          = Tckt._CaseDB[case][2]
            if   corner == "nom" :
                temp = self["temp_nom"]
            elif corner == "low" :
                temp = self["temp_low"]
            elif corner == "high" :
                temp = self["temp_high"]
            corner          = Tckt._CaseDB[case][3]
            if   corner == "nom" :
                supply = self["supply_nom"]
            elif corner == "low" :
                supply = self["supply_low"]
            elif corner == "high" :
                supply = self["supply_high"]
            self.__temp = temp
            self.__vdd  = supply
        else :
            self.fatal("case \"" + case + "\" not supported")
    #===========================================================================
    # METHOD  : _config_path_callback
    # PURPOSE : establish netlist/test path
    #   * todo check directories
    #===========================================================================
    def _config_path_callback(self) :
        path = self["path"]
    #===========================================================================
    # METHOD  : _config_netlistfile_callback
    # PURPOSE : establish netlist file
    #  * figure out simulator file names
    #===========================================================================
    def _config_netlistfile_callback(self) :
        self.__netlistpath = None
        self.__netlistfooter=None
        self.__netlistparams=None
        netlistfile = self["netlistfile"]
        path = self["path"]
        found = False
        for dir in path :
            netlistpath = dir + "/" + netlistfile
            if os.path.isfile(netlistpath) :
                found = True
                self.__netlistpath = netlistpath
                break
        if found :
            root = os.path.splitext(os.path.basename(netlistpath))[0]
            if self["prefix"] == "" :
                self["prefix"] =  root
            #------------------------------------------------------------------
            # sspice:
            #------------------------------------------------------------------
            defparamfile = root + ".defparams"
            defparampath = dir + "/" + defparamfile
            if os.path.isfile(defparampath) :
                if self["verbose"] :
                    print "copying %s" % (defparampath)
                try:
                    shutil.copyfile(defparampath, defparamfile)
                except:
                    print "failed to copy %s" % (defparampath)
            #------------------------------------------------------------------
            # spectre:
            #------------------------------------------------------------------
            footer = dir + "/netlistFooter"
            params = dir + "/.designVariables"
            if os.path.isfile(footer) :
                self.__netlistfooter=footer
            if os.path.isfile(params) :
                self.__netlistparams=params
        else :
            self.fatal("netlistfile \"" + netlistfile + "\" not found in", str(path))
    #===========================================================================
    # METHOD  : _config_prefix_callback
    # PURPOSE : establish input output data files
    #===========================================================================
    def _config_prefix_callback(self) :
        if re.search("\s", self["prefix"]) :
            self.fatal("prefix \"%s\" contains white-space" % self["prefix"])
        self.__inputfile  = self["prefix"] + ".ckt"
        self.__outputfile = self["prefix"] + ".lis"
        self.__datafile   = self["prefix"] + ".raw"
    #===========================================================================
    # METHOD : _config_resultsdir_callback
    # PURPOSE : setup or register results directory
    #===========================================================================
    def _config_resultsdir_callback(self) :
        rdir = self["resultsdir"]
        #---------------------------------------------------------------
        # if resultsdir is specified as "." or "./" just return
        #---------------------------------------------------------------
        if rdir == "." or rdir == "./" :
            self["resultsdir"] = ""
            return
        #---------------------------------------------------------------
        # results link should include the testbench name, if appropriate
        #---------------------------------------------------------------
        try :
            lpath = string.split(rdir, "/")
            isim = lpath.index(self["simulator"])
            testbench = lpath[isim-1]
            link = "%s_results" % (testbench)
        except :
            link = "results"
        #---------------------------------------------------------------
        # attempt to create results directory, and link to it
        #---------------------------------------------------------------
        try :
            if not os.path.isdir(rdir) :
                os.makedirs(rdir)
            if os.path.islink(link) :
                os.remove(link)
            os.symlink(rdir, link)
            #script=os.script()
            #shutil.copyfile(script, rdir)
        except :
            return(False)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Tckt access methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #===========================================================================
    # METHOD  : get_test
    # PURPOSE : get name of calling routine
    #===========================================================================
    def get_test(self) :
        """ get name of calling routine.

        **results**:    

            * get name of the routine from the calling frame.

        """
        return sys._getframe(1).f_code.co_name
    #===========================================================================
    # METHOD  : get_tech
    # PURPOSE : get technology
    #===========================================================================
    def get_tech(self) :
        """ get technology.

        **results**:    

            * get name of the current technology name.

        """
        return self.__tech
    #===========================================================================
    # METHOD  : get_case_key
    # PURPOSE : get key of current named process corner
    #===========================================================================
    def get_case_key(self) :
        """ get key of current process, voltage, temperature (case) corner.

        **results**:    

            * get the integer index (key) of the current case corner.

        """
        return self.__case_key
    #===========================================================================
    # METHOD  : get_modelfile
    # PURPOSE : get modelfile
    #===========================================================================
    def get_modelfile(self) :
        """ get modelfile.

        **results**:    

            * get the modelfile of the current project.

        """
        return(self.__modelfile)
    #===========================================================================
    # METHOD  : get_xnmos
    # PURPOSE : get nmos subcircuit device
    #===========================================================================
    def get_xnmos(self) :
        """ get nmos subcircuit device.

        **results**:    

            * get the NMOS device path in the NMOS subcircuit model
              for the current project.

        """
        return(self.__xnmos)
    #===========================================================================
    # METHOD  : get_xpmos
    # PURPOSE : get pmos subcircuit device
    #===========================================================================
    def get_xpmos(self) :
        """ get pmos subcircuit device.

        **results**:    

            * get the PMOS device path in the PMOS subcircuit model
              for the current project.

        """
        return(self.__xpmos)
    #===========================================================================
    # METHOD  : get_process
    # PURPOSE : get process
    #===========================================================================
    def get_process(self) :
        """ get process corner.

        **results**:    

            * get the process name (model file library) for the current
              PVT case corner.

        """
        return(self.__process)
    #===========================================================================
    # METHOD  : get_temp
    # PURPOSE : get temperature
    #===========================================================================
    def get_temp(self) :
        """ get temperature.

        **results**:    

            * get the temperature for the current PVT case corner.

        """
        return(self.__temp)
    #===========================================================================
    # METHOD  : get_vdd 
    # PURPOSE : get vdd
    #===========================================================================
    def get_vdd(self) :
        """ get power-supply voltage.

        **results**:    

            * get the power-supply voltage for the current PVT case corner.

        """
        return(self.__vdd)
    #===========================================================================
    # METHOD  : get_inputfile
    # PURPOSE : get inputfile
    #===========================================================================
    def get_inputfile(self) :
        """ get simulator input file.

        **results**:    

            * get the input file path.

        """
        rdir = self["resultsdir"]
        if rdir != "" :
            return(rdir + "/" + self.__inputfile)
        else :
            return(self.__inputfile)
    #===========================================================================
    # METHOD  : get_outputfile
    # PURPOSE : get outputfile
    #===========================================================================
    def get_outputfile(self) :
        """ get simulator output file.

        **results**:    

            * get the output file path.

        """
        rdir = self["resultsdir"]
        if rdir != "" :
            return(rdir + "/" + self.__outputfile)
        else :
            return(self.__outputfile)
    #===========================================================================
    # METHOD  : get_datafile
    # PURPOSE : get datafile
    #===========================================================================
    def get_datafile(self, analysis="tr") :
        """ get simulator waveform data file.

        **arguments**:

            .. option:: analysis (str, default="tr")

                used for HSpice which names the output file with the
                simulation analysis.

        **results**:    

            * get the simulator waveform data file path.

        """
        datafile = self.__datafile
        if self["simulator"] in ["hspice", "hspiceD"] :
            if   analysis in ("tr", "tran"): 
                ext = ".tr0" 
            elif analysis in ("ac"):
                ext = ".ac0"
            else :
                ext = ".dc0"
            datafile = os.path.splitext(os.path.basename(datafile))[0] + ext
        rdir = self["resultsdir"]
        if rdir != "" :
            return(rdir + "/" + self.__datafile)
        else :
            return(datafile)
    #===========================================================================
    # METHOD  : ckey2case
    # PURPOSE : return case name for a case key
    #===========================================================================
    def ckey2case(self, ckey) :
        """ get case corner name from case key.

        **arguments**:

            .. option:: ckey (str)

                case integer index (key)

        **results**:

            * returns a PVT case corner name corresponding to the case key.

        """
        xcase   = None
        project = self["project"]
        cases   = Tckt.project_cases(project)
        for case in cases :
            xckey = Tckt._CaseDB[case][0]
            if xckey == ckey:
                xcase = case
                break
        return xcase
    #===========================================================================
    # METHOD : bin2thm
    # PURPOSE : generate thermometer value from binary value
    #===========================================================================
    def bin2thm(self, binval, nbits) :
        """ generate thermometer value from binary value.

        **arguments**:

          .. option:: binval (int)

              binary value

          .. option:: nbits

              number of bits in thermometer value

        **results**:

          * returns thermometer code string : nbits'b1111...

        """
        thm = ["1" if i < binval else "0" for i in range(nbits)]
        thm.reverse()
        return "%s'b%s" % (nbits, string.join(thm, ""))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Tckt test select (gui)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #===========================================================================
    # METHOD  : test_select
    # PURPOSE : gui for selecting tests (or directly select)
    # NOTES :
    #   * selected tests can contain test without default test detail
    #===========================================================================
    def test_select(self, tests, selected_tests=None) :
        """ display dialog for selecting tests, or directly select tests.

        **arguments**:

            .. option:: tests (list of str)

                list of available tests in the script.

            .. option:: selected_tests (list of str, default=None)

                list of tests which are supplied directly.

        **results**:

            * if selected_tests is not None, return a list of these
              tests in the same order that they appear in the tests
              argument.

            * if selected_tests is None, display a dialog to select
              the tests.

        """
        Default_detail = {}
        test_details = []
        check_specs  = []
        for test_spec in string.split(tests, "\n") :
           tok = string.split(test_spec)
           if len(tok) == 1:
               test    = tok[0]
               test_detail = "%s" % (test)
               test_prompt = "%s" % (test)
               test_details.append(test_detail)
               check_specs.append((test_detail, test_prompt, False))
           elif len(tok) > 1:
               test    = tok[0]
               details = tok[1:]
               Default_detail[test] = tok[1]
               for detail in details :
                   test_detail = "%s:%s" % (test, detail)
                   test_prompt = "%s:%s" % (test, detail)
                   test_details.append(test_detail)
                   check_specs.append((test_detail, test_prompt, False))
        test_list = []
        if selected_tests :
            selected_tests_new = []
            for test in selected_tests :
                if not test in test_details :
                    if test in Default_detail : 
                        test += ":" + Default_detail[test]
                if not test in test_details :
                    self.fatal(
                        "  selected tests : %s" % \
                            string.join(selected_tests),
                        "test \"%s\" not in test list:\n    %s" % \
                            (test, string.join(test_details, "\n    ")))
                selected_tests_new.append(test)
            selected_tests = selected_tests_new

            for test_detail in test_details :
                if test_detail in selected_tests :
                    tok = string.split(test_detail, ":")
                    if   len(tok) == 1:
                        test   = tok[0]
                        test_list.append("%s()" % (test))
                    elif len(tok) == 2:
                        test   = tok[0]
                        detail = tok[1]
                        test_list.append("%s(\"%s\")" % (test, detail))
        else :
            specs = [["check", "Test Circuit Tests", check_specs]]
            sd = SelectionDialog(None, guispecs=specs)
            V = sd.go()
            if V["ACCEPT"] :
                for test_detail in test_details :
                    if V[test_detail] :
                        tok = string.split(test_detail, ":")
                        if   len(tok) == 1:
                            test   = tok[0]
                            test_list.append("%s()" % (test))
                        elif len(tok) == 2:
                            test   = tok[0]
                            detail = tok[1]
                            test_list.append("%s(\"%s\")" % (test, detail))
        return test_list
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Tckt script entry methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #===========================================================================
    # METHOD : monitor
    # PURPOSE : collect monitor specifications
    #===========================================================================
    def monitor(self, string) :
        """ collect monitor specifications.

        **arguments**:

            .. option:: string (str)

                a string of space-separated monitor items.

        **example monitor items**:

           * REF       : monitor voltage of node REF

           * VCD<3:0>  : monitor voltage of nodes VCD_3, ... , VCD_0

           * I(vsc)    : monitor current in voltage source vsc

           * IDN(mn1)  : monitor drain current in mosfet xmn1

           * IR(res)   : monitor current in resistor res

           * IX(xa1.p) : monitor current in subcircuit xa1, node p

           * PN(mn1-vdsat)  : monitor mosfet xmn1 vdsat parameter

           * @Xgmc:    : following specs are for subcircuit Xgmc

           * @Xgmc.Xq: : following specs are for subcircuit Xgmc.Xq

           * @:        : following specs are for top-level circuit

        """
        string = decida.interpolate(string, 2)
        if (self.__monitor == "") :
            self.__monitor = string
        else :
            self.__monitor += " @: " + string
    #===========================================================================
    # METHOD : veriloga
    # PURPOSE : collect one verilog specification
    #===========================================================================
    def veriloga(self, subckt, file, parameters="") :
        """ collect verilog-A specifications.

        **arguments**:

            .. option:: subckt (str)

                subcircuit name to use verilog-A representation.

            .. option:: file (str)

                verilog-A module file.

            .. option:: parameters (str, default="")

                string of space-separated parameter-name=value entries.

        """
        if not os.path.isfile(file) :
            self.fatal("Verilog-A file \"%s\" is not readable" % (file))
        self.__Veriloga[subckt] = (file, parameters)
        if self["simulator"] in ["hspice", "hspiceD"] :
            self.netlist_remove(subckt)
    #===========================================================================
    # METHOD : postlayout
    # PURPOSE : collect one postlayout specification
    #===========================================================================
    def postlayout(self, inst, subckt, file) :
        """ collect postlayout specifications.

        **arguments**:

            .. option:: inst (str)

                full path of instance in testbench schematic
                to replace with postlayout representation.
                used to modify monitor specs.

            .. option:: subckt (str)

                specifies subcircuit to replace.
                Tckt.netlist_remove() is used to remove the subcircuit.

            .. option:: file (str)

                specifies path to postlayout netlist.
                used to generate .include file.

        """
        if not os.path.isfile(file) :
            self.fatal(
                "Postlayout extracted file \"%s\" is not readable" % (file))
        self.__Postlayout[subckt] = file
        self.__postlayout_instances.append(inst)
        self.netlist_remove(subckt)
    #===========================================================================
    # METHOD : netlist_remove
    # PURPOSE : specify subcircuits or instances to remove from netlist
    #===========================================================================
    def netlist_remove(self, s) :
        """ specify subcircuits or instances to remove from the netlist

        **arguments**:

            .. option:: s (str)

                a subcircuit name or instance name to remove from the
                netlist.

        """
        s = decida.interpolate(s, 2)
        s = self.__script_to_netlist(s)
        for line in string.split(s, "\n") :
            tokens = string.split(line)
            for token in tokens :
                ckt = token
                if self._netlist_format == "spice" :
                    ckt = string.lower(ckt)
                self.__netlistRemove.append(ckt)
    #===========================================================================
    # METHOD : elements
    # PURPOSE : collect element replacement specifications
    #===========================================================================
    def elements(self, s) :
        """ collect element value replacement specifications.

        **arguments**:

            .. option:: s (str)

                each (newline-separated) line of s is a specification of
                a value for the sources in the netlist.

        **example element definitions**:

            * vin sin 0.6 0.2 $freq

                replace the value of the voltage source with a sine spec.

            * vbg netlist

                use the existing vbg value in the netlist.  This marks the
                source as recognized and no warning message is printed
                for the source not being specified.

            * vdd $vdd

                use the value of the python-script variable vdd

            * vsd<3:0> 5'b0011 v0=0.0 v1=$vdd

                specify a bus of values.  The digital 0 value is 0.0V and
                the digital 1 value is vdd V.

            * vdac_in<9:0> counter v0=0.0 v1=$vdd edge=$edge hold=$hold

                specify that vdac_in counts up from 0 to the maximum value
                with rise-time = edge and hold-time = hold.

        """
        #-----------------------------------------------------------------------
        # interpolate variables into element specifications
        #-----------------------------------------------------------------------
        s = decida.interpolate(s, 2)
        #-----------------------------------------------------------------------
        # apply element specifications
        #-----------------------------------------------------------------------
        for line in string.split(s, "\n") :
            tokens = string.split(line)
            if len(tokens) >= 2 :
                 #------------------------------------------------------------
                 # element name
                 #------------------------------------------------------------
                 element = tokens.pop(0)
                 if element[0] == "#" :
                     continue
                 nesc_element = element
                 element = self.__script_to_netlist(element)
                 #------------------------------------------------------------
                 # spectre: spectre language
                 #------------------------------------------------------------
                 if tokens[0] == "spectre" :
                     value = string.join(tokens)
                     self.__Element[element] = value
                     continue
                 #------------------------------------------------------------
                 # element value
                 #------------------------------------------------------------
                 value = string.join(tokens)
                 value = string.lower(value)
                 value = re.sub(" *= *", "=", value)
                 value = re.sub(" *, *", " ", value)
                 tok = string.split(value)
                 word1 = tok.pop(0)
                 #------------------------------------------------------------
                 # spice: verbatim
                 # (keyword can be abbreviated)
                 #------------------------------------------------------------
                 m = re.search("^(dc|ac|pul|pl|pwl|pwlfile|sin|exp|sffm)", word1)
                 if m :
                     self.__Element[element] = value
                     continue
                 #------------------------------------------------------------
                 # stability:
                 # parameters for stability
                 # invert: change around ssub orientation from sspice way
                 #    * supplies normally inserted with +/- = output, feedback
                 # fmin, fmax : min, max for ac analyses
                 # method: middlebrook or vbreak
                 #------------------------------------------------------------
                 if word1 == "stability" :
                     inst = tok.pop(0)
                     self.__Stability["inst"]    = inst
                     self.__Stability["xinst"]   = string.split(inst, ".")[-1]
                     self.__Stability["method"]  = "middlebrook"
                     self.__Stability["invert"]  = False
                     self.__Stability["fmin"]    = "1"
                     self.__Stability["fmax"]    = "100G"
                     self.__Stability["vsave"]   = "v(%s.c)"      % (inst)
                     self.__Stability["isave"]   = "i(%s.vinj)"   % (inst)
                     self.__Stability["vdata"]   = "v(%s.c)"      % (inst)
                     self.__Stability["idata"]   = "i(v.%s.vinj)" % (inst)
                     self.__Stability["vblock"]  = 0
                     self.__Stability["iblock"]  = 1
                     pars = string.join(tok)
                     pars = re.sub("=", " ", pars)
                     pars = string.split(pars)
                     while len(pars) > 0 :
                         arg = pars.pop(0)
                         if   arg == "invert" :
                             self.__Stability["invert"] = True
                         elif arg == "fmin" :
                             self.__Stability["fmin"]   = pars.pop(0)
                         elif arg == "fmax" :
                             self.__Stability["fmax"]   = pars.pop(0)
                         elif arg == "method" :
                             self.__Stability["method"] = pars.pop(0)
                         elif arg == "vblock" :
                             self.__Stability["vblock"] = string.atoi(pars.pop(0))
                         elif arg == "iblock" :
                             self.__Stability["iblock"] = string.atoi(pars.pop(0))
                     self.__Element[element] = "stability"
                     continue
                 #------------------------------------------------------------
                 # other:
                 #------------------------------------------------------------
                 args = {}
                 for item in tok :
                     if re.search("=", item) :
                         key, val = string.split(item, "=")
                         args[key] = val
                     else :
                         self.warning("element keyword/value pair has no = : %s" % line)
                 if   word1 == "prbs" :
                     self.__prbs(nesc_element, args)
                 elif word1 == "rand" :
                     self.__rand(nesc_element, args)
                 elif word1 == "bits" :
                     self.__bits(nesc_element, args)
                 elif word1 == "clock" :
                     self.__clock(nesc_element, args)
                 elif word1 == "counter" :
                     self.__counter(nesc_element, args)
                 elif word1 == "therm" :
                     self.__therm(nesc_element, args)
                 else :
                     #-------------------------------------------------
                     # value, "netlist", or verilog-specification:
                     #-------------------------------------------------
                     self.__set_register(nesc_element, word1, args)
    #===========================================================================
    # METHOD : control
    # PURPOSE : interpolate control string
    #===========================================================================
    def control(self, s) :
        """ specify simulation control string.

        **arguments**:

            .. option:: s (str)

                a string to be inserted in the input file directly.  This is
                in the same language of the simulator itself.

        **results**:

            * python variables are interpolated into the control section

            * the control section is included at the end of the
              simulator input file.

        """
        self.__control = decida.interpolate(s, 2)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Tckt output/simulate methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #===========================================================================
    # METHOD : generate_inputfile
    # PURPOSE : collect netlist, control, substitutions, write input file
    #===========================================================================
    def generate_inputfile(self) :
        """ write simulator input file based on netlist, control,
            monitor specs.

        **results**:

            * calls spice or spectre input file generator.

        """
        if   self._netlist_format == "spice" :
            self.generate_spice_inputfile()
        elif self._netlist_format == "spectre" :
            self.generate_spectre_inputfile()
    #===========================================================================
    # METHOD : generate_spectre_inputfile
    # PURPOSE : collect netlist, control, substitutions, write input file
    #===========================================================================
    def generate_spectre_inputfile(self) :
        """ write (spectre) simulator input file based on netlist, control,
            monitor specs.

        **results**:

            * generates input file for spectre.

            * starting with the netlist file, specified element values are 
              inserted, output voltages and currents are specified, and 
              the control section is included.

        """
        olines = []
        #----------------------------------------------------------------------
        # title 
        #----------------------------------------------------------------------
        DATE  = time.asctime(time.localtime(time.time()))
        LIB   = "work"
        CKT   = self["circuit"]
        TITLE = self["title"]
        VIEW  = "schematic"
        MODELFILE = self.get_modelfile()
        olines.append("// spectre simulation of %s" % (CKT))
        olines.append("//" + "=" * 72)
        olines.append("// Generated for: spectre")
        olines.append("// Generated on: %s" % (DATE))
        olines.append("// Design library name: %s" % (LIB))
        olines.append("// Design cell name: %s" % (CKT))
        olines.append("// Design view name: %s" % (VIEW))
        olines.append("//" + "=" * 72)
        olines.append("simulator lang=spectre")
        olines.append("global 0")
        #----------------------------------------------------------------------
        # if there is a template
        #----------------------------------------------------------------------
        error_flag   = False
        do_stability = False
        subckt_list  = []
        if not self.__netlistpath is None :
            #----------------------------------
            # line continuation
            #----------------------------------
            xlines = []
            xline = ""
            fnetlist = open(self.__netlistpath, "r")
            for line in fnetlist :
                line = re.sub("\r", "", line)
                line = re.sub("\n", "", line)
                line = re.sub("\t", " ", line)
                line = string.strip(line)
                if len(line) == 0:
                    if len(xline) > 0:
                        xline = re.sub("[\t ]+", " ", xline)
                        xlines.append(xline)
                    xline = ""
                elif line[-1] == "\\" :
                    xline += line[0:-1]
                else :
                    xline += line
                    xline = re.sub("[\t ]+", " ", xline)
                    xlines.append(xline)
                    xline = ""
            if len(xline) > 0:
                xline = re.sub("[\t ]+", " ", xline)
                xlines.append(xline)
            fnetlist.close()
            #------------------------------------------------------------------
            # fill-in template lines with supply definitions
            #------------------------------------------------------------------
            subckt      = ""
            beg_subckt  = False
            end_subckt  = False
            skip_inst   = False
            skip_subckt = False
            Used = {}
            for line in xlines :
                tokens = string.split(line)
                tword = tokens[0]
                #--------------------------------------------------------------
                # subcircuit begin:
                #--------------------------------------------------------------
                if tword == "subckt" :
                    if len(tokens) > 1 :
                        subckt = tokens[1]
                        beg_subckt = True
                        if subckt in self.__netlistRemove :
                            skip_subckt = True
                        else :
                            subckt_list.append(subckt)
                        if subckt in self.__Postlayout :
                            save_subckt = True
                            Saved_subckt[subckt] = []
                            Saved_subckt[subckt].extend(tokens[2:])
                    else :
                        self.warning("netlist subcircuit line",
                            " with no subcircuit name:\n", line)
                #--------------------------------------------------------------
                # subcircuit end:
                #--------------------------------------------------------------
                elif tword == "ends" :
                    if len(tokens) > 1 :
                        if tokens[1] != subckt :
                            self.warning("end subckt doesn't match beg subckt")
                        subckt = tokens[1]
                        if subckt in self.__netlistRemove :
                            if not skip_subckt :
                                self.warning("ends %s: not skipping subckt but subckt in netlist_remove" % (subckt))
                        subckt = ""
                        end_subckt = True
                    else :
                        self.warning("netlist end subcircuit line",
                            " with no subcircuit name:\n", line)
                #--------------------------------------------------------------
                # comment
                #--------------------------------------------------------------
                elif re.search("^\s*//", line) :
                    pass
                #--------------------------------------------------------------
                # instance
                # July 12, 2014 RVB: change regular expression from
                # m = re.search(r"^\s*([\w\\<>-]+)\s*\((.+)\)\s*([\w\\<>]+)(.*)$", line)
                #--------------------------------------------------------------
                else :
                    m = re.search(r"^\s*([\w\\<>-]+)\s*\(([^\)]+)\)\s*([\w\\<>]+)(.*)$", line)
                    if m :
                        inst = m.group(1)
                        nlst = string.split(string.strip(m.group(2)))
                        sckt = m.group(3)
                        plst = string.split(string.strip(m.group(4)))
                        #-------------------------------------------------
                        # remove instances
                        #-------------------------------------------------
                        if inst in  self.__netlistRemove :
                            skip_inst = True
                        #-------------------------------------------------
                        # replace specified supplies
                        # (every one must be accounted for)
                        #-------------------------------------------------
                        elif sckt in ("vsource", "isource") :
                            pos = nlst[0]
                            neg = nlst[1]
                            val = string.join(plst)
                            if inst in self.__Element :
                                Used[inst] = 1
                                new_val = self.__Element[inst]
                                tok = string.split(new_val)
                                if   new_val == "netlist" :
                                    #-----------------------------------------
                                    # use netlist value
                                    #-----------------------------------------
                                    line = "%s (%s %s) %s %s" % \
                                        (inst, pos, neg, sckt, val)
                                elif string.upper(tok[0]) == "SPECTRE" :
                                    #-----------------------------------------
                                    # source in spectre format
                                    #-----------------------------------------
                                    new_val = string.join(tok[1:])
                                    line = "%s (%s %s) %s %s" % \
                                        (inst, pos, neg, sckt, new_val)
                                elif string.upper(tok[0]) == "SIN" or \
                                     string.upper(tok[0]) == "SINE" :
                                    #-----------------------------------------
                                    # SINE source
                                    #-----------------------------------------
                                    # ngspice 4.1.2
                                    # spectre ref pg 682
                                    if len(tok) >= 4 and len(tok) <= 6:
                                        offset    = tok[1]
                                        amplitude = tok[2]
                                        frequency = tok[3]
                                        delay = 0.0
                                        theta = 0.0
                                        if len(tok) >= 5 : delay = tok[4]
                                        if len(tok) == 6 : theta = tok[5]
                                        line = "%s (%s %s) %s type=sine sinedc=%s ampl=%s freq=%s delay=%s damp=%s" % (inst, pos, neg, sckt, offset, amplitude, frequency, delay, theta)
                                    else :
                                        self.warning("SIN specification has wrong number of fields: %s" % (line))
                                elif string.upper(tok[0]) == "PULSE" :
                                    #-----------------------------------------
                                    # PULSE source
                                    #-----------------------------------------
                                    if len(tok) == 8 :
                                        val0   = tok[1]
                                        val1   = tok[2]
                                        delay  = tok[3]
                                        rise   = tok[4]
                                        fall   = tok[5]
                                        width  = tok[6]
                                        period = tok[7]
                                        line = "%s (%s %s) %s type=pulse val0=%s val1=%s delay=%s rise=%s fall=%s width=%s period=%s" % \
                                            (inst, pos, neg, sckt, val0, val1, delay, rise, fall, width, period)
                                    else :
                                        self.warning("PULSE specification has wrong number of fields: %s" % (line))
                                elif string.upper(tok[0]) == "PWL" :
                                    #-----------------------------------------
                                    # PWL source
                                    #-----------------------------------------
                                    new_val = string.join(tok[1:])
                                    line = "%s (%s %s) %s type=pwl wave=[%s]" % \
                                        (inst, pos, neg, sckt, new_val)
                                elif string.upper(tok[0]) == "AC" :
                                    #-----------------------------------------
                                    # AC source
                                    #-----------------------------------------
                                    acmag=1
                                    dcval=1
                                    acphi=0
                                    for item in tok[1:] :
                                        name, val = string.split(item, "=")
                                        if   name == "dc" :
                                            dcval=val
                                        elif name == "mag" :
                                            acmag=val
                                        elif name == "phase" :
                                            acphi=val
                                    line = "%s (%s %s) %s type=dc dc=%s mag=%s phase=%s" % \
                                    (inst, pos, neg, sckt, dcval, acmag, acphi)
                                else :
                                    #-----------------------------------------
                                    # DC source
                                    #-----------------------------------------
                                    line = "%s (%s %s) %s type=dc dc=%s" % \
                                        (inst, pos, neg, sckt, new_val)
                            else :
                                self.warning("supply \"" + inst + \
                                    "\" was not specified - using netlist value")
                                error_flag = True
                    #----------------------------------------------------------
                    # instance with no nodes (mutual_inductance is one)
                    #----------------------------------------------------------
                    else :
                        m = re.search(r"^\s*([\w\\<>-]+)\s*([\w\\<>]+)(.*)$", line)
                        if m:
                            inst = m.group(1)
                            sckt = m.group(2)
                            plst = string.split(string.strip(m.group(3)))
                            #-------------------------------------------------
                            # remove instances
                            #-------------------------------------------------
                            if inst in  self.__netlistRemove :
                                skip_inst = True
                        else :
                            print "unhandled line:", line
                skip_prefix   = ""
                subckt_prefix = ""
                if (skip_inst or skip_subckt) :
                    skip_prefix = "// <REMOVE> "
                if len(subckt) > 0 and not beg_subckt :
                    subckt_prefix = "    "
                if end_subckt :
                    skip_subckt = False
                skip_inst  = False
                beg_subckt = False
                end_subckt = False
                #--------------------------------------------------------------
                # Sept. 30, 2014: don't split up comments
                #--------------------------------------------------------------
                if re.search("^\s*//", line) :
                    olines.append(skip_prefix + subckt_prefix + line)
                else :
                    xlines = decida.multiline(line, 70)
                    if len(xlines) > 0 :
                        xlinen = xlines.pop(-1)
                        indent = ""
                        for xline in xlines :
                            xline = skip_prefix + subckt_prefix + indent + xline
                            olines.append(xline + " \\")
                            indent = "    "
                        xlinen = skip_prefix + subckt_prefix + indent + xlinen
                        olines.append(xlinen)
        #----------------------------------------------------------------------
        # generate save lines using monitor string
        #----------------------------------------------------------------------
        save_items = self.__spectre_monitor_spec()
        simulator  = self["simulator"]
        if (len(save_items) > 0) :
            olines.append("//" + "=" * 72)
            olines.append("// save lines:")
            olines.append("//" + "=" * 72)
            line = "save"
            for item in save_items :
                if (len(line) + len(item) > 72 ) :
                    olines.append(line + "\\")
                    line = ""
                line += " " + item
            if len(line) > 0 :
                olines.append(line)
        #----------------------------------------------------------------------
        # add control lines and .end
        #----------------------------------------------------------------------
        if self.__control != None :
            olines.append("//" + "=" * 72)
            olines.append("// control section:")
            olines.append("//" + "=" * 72)
            for line in string.split(self.__control, "\n") :
                line = line.strip()
                if len(line) > 0 :
                    olines.append(line)
            olines.append("//" + "=" * 72)
            olines.append("// end of control section")
            olines.append("//" + "=" * 72)
        #----------------------------------------------------------------------
        # verilog-A source files
        # include even if not over-riding subcircuit
        #----------------------------------------------------------------------
        for sname in self.__Veriloga :
            if True or sname in subckt_list :
                va_file = self.__Veriloga[sname][0]
                olines.append("ahdl_include \"%s\"" % (va_file))
        #----------------------------------------------------------------------
        # brute-force include netlist footer and design variables
        # this should be done by RVBdcdlines.il
        #----------------------------------------------------------------------
        if False :
            if not self.__netlistfooter is None:
                f = open(self.__netlistfooter, "r")
                for line in f:
                    line = re.sub("\r", "", line)
                    line = re.sub("\n", "", line)
                    olines.append(line)
                f.close()
            if not self.__netlistparams is None:
                f = open(self.__netlistparams, "r")
                for line in f:
                    line = re.sub("\r", "", line)
                    line = re.sub("\n", "", line)
                    olines.append(line)
                f.close()
        #----------------------------------------------------------------------
        # end of generated input file
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        # check to see if all supply definitions were used:
        #----------------------------------------------------------------------
        for key in self.__Element :
            if not key in Used :
                self.warning("element definition \"%s\" was not used" % (key))
        if error_flag :
            pass
            # self.fatal("errors must be fixed")
        #----------------------------------------------------------------------
        # write inputfile
        #----------------------------------------------------------------------
        f = open(self.get_inputfile(), "w")
        for oline in olines :
            f.write(oline + "\n")
        f.close()
    #===========================================================================
    # METHOD : generate_spice_inputfile
    # PURPOSE : collect netlist, control, substitutions, write input file
    # NOTES :
    #   * add stability subcircuit if stability vsource is marked
    #===========================================================================
    def generate_spice_inputfile(self) :
        """ write (spice) simulator input file based on netlist, control,
            monitor specs.

        **results**:

            * generates input file for spice.

            * starting with the netlist file, specified element values are 
              inserted, output voltages and currents are specified, and 
              the control section is included.

        """
        olines = []
        #----------------------------------------------------------------------
        # title 
        #----------------------------------------------------------------------
        olines.append("* " + self["title"])
        #----------------------------------------------------------------------
        # if there is a template
        #----------------------------------------------------------------------
        error_flag   = False
        do_stability = False
        subckt_list  = []
        if not self.__netlistpath is None :
            #------------------------------------------------------------------
            # fill-in template lines with supply definitions
            # save_subckt for comparing postlayout / prelayout node list
            #------------------------------------------------------------------
            skip_inst = False
            skip_sckt = False
            save_subckt  = False
            Saved_subckt = {}
            Used = {}
            fnetlist = open(self.__netlistpath, "r")
            for line in fnetlist :
                line = re.sub("\r", "", line)
                line = re.sub("\n", "", line)
                line = string.lower(line)
                tokens = string.split(line)
                #--------------------------------------------------------------
                # skip empty lines:
                #--------------------------------------------------------------
                if len(tokens) == 0:
                    continue
                else :
                    tword = tokens[0]
                    ttype = tword[0]
                #--------------------------------------------------------------
                # if skipping inst. and line is not cont. line, stop skipping:
                #--------------------------------------------------------------
                if skip_inst and ttype != "+" :
                    skip_inst = False
                if save_subckt :
                    if ttype == "+" :
                        if len(tword) > 1:
                            Saved_subckt[subckt].append(tword[1:])
                        Saved_subckt[subckt].extend(tokens[1:])
                    else :
                        save_subckt = False
                #--------------------------------------------------------------
                # subcircuit begin:
                #--------------------------------------------------------------
                if tword == ".subckt" :
                    if len(tokens) > 1 :
                        subckt = tokens[1]
                        if subckt in self.__netlistRemove :
                            skip_sckt = True
                        else :
                            subckt_list.append(subckt)
                        if subckt in self.__Postlayout :
                            save_subckt = True
                            Saved_subckt[subckt] = []
                            Saved_subckt[subckt].extend(tokens[2:])
                    else :
                        self.warning("netlist subcircuit line",
                            " with no subcircuit name:\n", line)
                #--------------------------------------------------------------
                # subcircuit end:
                #--------------------------------------------------------------
                elif tword == ".ends" :
                    if len(tokens) > 1 :
                        subckt = tokens[1]
                        if subckt in self.__netlistRemove and not skip_sckt :
                            self.warning(".ends %s: not skipping subckt" % (subckt),
                                " but subckt in netlist_remove")
                    else :
                        if not self["simulator"] in ["eldo", "eldoD"] :
                            self.warning("netlist end subcircuit line",
                                " with no subcircuit name:\n", line)
                    if skip_sckt:
                        line = "*<REMOVE>* " + line
                        skip_sckt = False
                #--------------------------------------------------------------
                # instance
                #--------------------------------------------------------------
                elif re.search("[a-z_]", ttype) :
                    inst, type = tword, ttype
                    #-------------------------------------------------
                    # remove instances
                    #-------------------------------------------------
                    if inst in  self.__netlistRemove :
                        skip_inst = True
                    #-------------------------------------------------
                    # examine subcircuits for veriloga
                    #-------------------------------------------------
                    elif type == "x" :
                        xline = re.sub(" *= *", "=", line)
                        xline = string.split(xline)
                        sname = ""
                        for item in xline :
                            if re.search("=", item) :
                                break
                            sname = item
                        #----------------------------------------------
                        # ADE netlister appends _schematic to subckt name
                        #----------------------------------------------
                        if self["simulator"] == "hspiceD" :
                            m=re.search("(\w+)_schematic", sname)
                            if m:
                                sname = m.group(1)
                        if sname in self.__Veriloga:
                            #----------------------------------------------
                            # ADE netlister appends _schematic to subckt name
                            #----------------------------------------------
                            #et_pars = string.join(tokens[1:])
                            net_pars = []
                            for t in tokens[1:] :
                                if t == "%s_schematic" % (sname) :
                                    t = sname
                                net_pars.append(t)
                            net_pars = string.join(net_pars)
                            va_pars  = self.__Veriloga[sname][1]
                            if self["simulator"] == "sspice" :
                                line = "YVLG_%s %s  %s" % (inst, net_pars, va_pars)
                            else :
                                line =      "%s %s  %s" % (inst, net_pars, va_pars)
                    #-------------------------------------------------
                    # replace specified supplies
                    # (every one must be accounted for)
                    #-------------------------------------------------
                    elif type in ("v", "i") :
                        pos = tokens[1]
                        neg = tokens[2]
                        val = string.join(tokens[3:])
                        if inst in self.__Element :
                            Used[inst] = 1
                            new_val = self.__Element[inst]
                            tok = string.split(new_val)
                            if tok[0] == "stability" :
                                #---------------------------------------------
                                # voltage source replaced with stability
                                # instance (middlebrook or vbreak)
                                #---------------------------------------------
                                do_stability = True
                                xinst = self.__Stability["xinst"]
                                smeth = self.__Stability["method"]
                                ssub  = smeth + "_stability"
                                if self.__Stability["invert"]:
                                    pos, neg = neg, pos
                                line = "%s %s %s %s" % (xinst, pos, neg, ssub)
                            elif new_val == "netlist" :
                                line = "%s %s %s %s" % (inst, pos, neg, val)
                            else :
                                line = "%s %s %s %s" % (inst, pos, neg, new_val)
                        else :
                            self.warning("supply \"" + inst + \
                                "\" was not specified - using netlist value")
                            error_flag = True
                    #-------------------------------------------------
                    # replace specified elements
                    #-------------------------------------------------
                    elif type in ("r", "c") :
                        pos = tokens[1]
                        neg = tokens[2]
                        val = string.join(tokens[3:])
                        if inst in self.__Element :
                            Used[inst] = 1
                            new_val = self.__Element[inst]
                            if new_val != "netlist" :
                                val = new_val
                            line = inst + " " + pos + " " + neg + " " + val
                if skip_sckt or skip_inst :
                    line =  "*<REMOVE>* " + line
                olines.append(line)
            fnetlist.close()
        #----------------------------------------------------------------------
        # if stability subcircuit required
        #----------------------------------------------------------------------
        if do_stability :
            smeth = self.__Stability["method"]
            ssub  = smeth + "_stability"
            vsave = self.__Stability["vsave"]
            isave = self.__Stability["isave"]
            olines.append("*" + "=" * 72)
            olines.append("* stability subcircuit:")
            olines.append("*" + "=" * 72)
            olines.append(".subckt %s a b" % (ssub))
            if   smeth == "middlebrook" :
                olines.append("  vwinj b c 0")
                olines.append("  vinj  c a dc 0 ac _vinj")
                olines.append("  iinj  0 c dc 0 ac _iinj")
            elif smeth == "vbreak" :
                olines.append("  vwinj a c 0")
                olines.append("  vinj  b d dc 0 ac _vinj")
                olines.append(" *crep  c 0 1e-15")
                olines.append("  rbrk  c b r=1e-3 ac=1e12")
                olines.append("  rmak  d 0 r=1e12 ac=1e-3")
            else :
                self.warning("stability method \"" + method + \
                    "\" is not supported")
                error_flag = True
            olines.append(".ends   %s"     % (ssub))
            olines.append(".save %s %s" % (vsave, isave))
        #----------------------------------------------------------------------
        # need to know what the analysis is for the annoying .PROBE <ANALYSIS>
        #----------------------------------------------------------------------
        analysis = "tr"
        if self.__control != None :
            for line in string.split(self.__control, "\n") :
                line = line.strip()
                line = string.lower(line)
                m = re.search("^\.(dc|ac|tran|tr) ", line)
                if m :
                    analysis = m.group(1)
        #----------------------------------------------------------------------
        # generate .save lines using monitor string
        #----------------------------------------------------------------------
        save_items = self.__spice_monitor_spec()
        simulator  = self["simulator"]
        if (len(save_items) > 0) :
            olines.append("*" + "=" * 72)
            olines.append("* save lines:")
            olines.append("*" + "=" * 72)
            if   simulator in ["sspice", "ngspice"] :
                line = ".save"
            elif simulator in ["hspice", "hspicerf", "hspiceD"] :  
                line = ".probe " + analysis
            elif simulator in ["nanosim"] :
                line = "*"
            elif simulator in ["eldo", "adit", "adms", "eldoD"] :
                line = ".plot"
            if simulator != "nanosim" :
                for item in save_items :
                    if (len(line) + len(item) > 72 ) :
                        olines.append(line)
                        line = "+"
                    line += " " + item
                if len(line) > 0 :
                    olines.append(line)
        #----------------------------------------------------------------------
        # add control lines and .end
        #----------------------------------------------------------------------
        if self.__control != None :
            olines.append("*" + "=" * 72)
            olines.append("* control section:")
            olines.append("*" + "=" * 72)
            for line in string.split(self.__control, "\n") :
                line = line.strip()
                if len(line) > 0 :
                    olines.append(line)
            olines.append("*" + "=" * 72)
            olines.append("* end of control section")
            olines.append("*" + "=" * 72)
        #----------------------------------------------------------------------
        # stability ac analysis
        #----------------------------------------------------------------------
        if do_stability :
            fmin  = self.__Stability["fmin"]
            fmax  = self.__Stability["fmax"]
            smeth = self.__Stability["method"]
            olines.append("*" + "=" * 72)
            olines.append("* stability")
            olines.append("*" + "=" * 72)
            olines.append(".parameter _vinj=1 _iinj=0")
            olines.append(".ac dec 100 %s %s" % (fmin, fmax))
            if smeth == "middlebrook" :
                olines.append(".alter AC current injection")
                olines.append(".parameter _vinj=0 _iinj=1")
        #----------------------------------------------------------------------
        # verilog-A source files
        #----------------------------------------------------------------------
        for sname in self.__Veriloga :
            if True or sname in subckt_list :
                va_file = self.__Veriloga[sname][0]
                if self["simulator"] == "sspice" :
                    olines.append(".verilog \"%s\"" % (va_file))
                else :
                    olines.append(".hdl     \"%s\"" % (va_file))
        #----------------------------------------------------------------------
        # postlayout extracted netlist files
        #----------------------------------------------------------------------
        for sname in self.__Postlayout :
            olines.append(".include \"%s\"" % (self.__Postlayout[sname]))
        #----------------------------------------------------------------------
        # compare .subckt lines in netlist and extracted netlist
        #----------------------------------------------------------------------
        for sname in self.__Postlayout :
            fext = open(self.__Postlayout[sname], "r")
            scont = False
            for fline in fext :
                fline = string.lower(fline)
                fline = string.strip(fline)
                m = re.search("^.subckt +([^ ]+) +(.+)$", fline)
                if m :
                    sname_ext = m.group(1)
                    nodes_ext = m.group(2)
                    scont = True
                    continue
                if scont :
                    m = re.search("^\+(.+)$", fline)
                    if m :
                        nodes_ext += " "
                        nodes_ext += m.group(1)
                    else :
                        scont = False
                        break
            fext.close()
            nodes_ext = string.split(nodes_ext)
            snet = "%s: %s" % (sname, string.join(Saved_subckt[sname]))
            sext = "%s: %s" % (sname_ext, string.join(nodes_ext))
            if snet != sext :
                print "schematic netlist subckt doesn't match extracted subckt:"
                print "  schematic netlist: "
                print "     ", snet
                print "  extracted netlist: "
                print "     ", sext
        #----------------------------------------------------------------------
        # end of generated input file
        #----------------------------------------------------------------------
        olines.append(".end")
        #----------------------------------------------------------------------
        # check to see if all supply definitions were used:
        #----------------------------------------------------------------------
        for key in self.__Element :
            if not key in Used :
                self.warning("element definition \"%s\" was not used" % (key))
        if error_flag :
            self.fatal("errors must be fixed")
        #----------------------------------------------------------------------
        # write inputfile
        #----------------------------------------------------------------------
        f = open(self.get_inputfile(), "w")
        for oline in olines :
            f.write(oline + "\n")
        f.close()
    #===========================================================================
    # METHOD : simulate
    # PURPOSE : perform simulation
    #===========================================================================
    def simulate(self, simulate=True, clean=False, remote="") :
        """ perform simulation.

        **arguments**:

            .. option:: simulate (bool, default=True)

                if True, proceed to simulate.  Otherwise simply print the
                simulation command.

            .. option:: clean (bool, default=False)

                if True, remove the input file and output file, leaving only
                the data file.

            .. option:: remote (str, default="")

                if specified, generate a command deck and submit as a batch job
                on the named remote host.

        """
        if   self["simulator"] in ["spectre"] :
            self.__simulate_spectre(simulate, clean, remote)
        elif self["simulator"] in ["hspice", "hspiceD"] :
            self.__simulate_hspice(simulate, clean, remote)
        elif self["simulator"] in ["sspice"] :
            self.__simulate_sspice(simulate, clean, remote)
        elif self["simulator"] in ["ngspice"] :
            self.__simulate_ngspice(simulate, clean, remote)
    #===========================================================================
    # METHOD  : __simulate_spectre
    # PURPOSE : simulation with spectre
    #===========================================================================
    def __simulate_spectre(self, simulate, clean, remote) :
        project = self["project"]
        inpfile = self.get_inputfile()
        outfile = self.get_outputfile()
        datfile = self.get_datafile()
        simargs = self["simulator_args"]
        sim = os.path.expanduser("~/.DeCiDa/bin/") + "run_spectre"
        args = "-format nutbin"
        cmd = "%s -quiet -project %s %s +log %s -raw %s %s %s" % (
            sim, project, inpfile, outfile, datfile, args, simargs
        )
        if remote != "" :
            runfile=os.path.splitext(os.path.basename(inpfile))[0] + ".run"
            cwd = os.getcwd()
            f = open(runfile, "w")
            f.write("#!/bin/bash\n")
            f.write("cd %s\n" % (cwd))
            f.write("%s\n"    % (cmd))
            f.close()
            os.chmod(runfile, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
            cmd = "ssh -t %s '%s/%s'" % (remote, cwd, runfile)
        success = True
        if simulate :
            try:
                subprocess.check_call(string.split(cmd))
            except subprocess.CalledProcessError, err :
                success = False
        else :
            print string.split(cmd)
            success = False
        if success and clean :
            for file in (outfile, inpfile) :
                try:
                    os.remove(file)
                except OSError, err :
                    print "failed to remove ", file
    #===========================================================================
    # METHOD  : __simulate_hspice
    # PURPOSE : simulation with hspice
    #===========================================================================
    def __simulate_hspice(self, simulate, clean, remote) :
        project = self["project"]
        inpfile = self.get_inputfile()
        outfile = self.get_outputfile()
        datfile = self.get_datafile()
        simargs = self["simulator_args"]
        sim  = os.path.expanduser("~/.DeCiDa/bin/") + "run_hspice"
        args = ""
        cmd = "%s -quiet -project %s %s -o %s %s %s" % (
            sim, project, inpfile, outfile, args, simargs
        )
        if remote != "" :
            runfile=os.path.splitext(os.path.basename(inpfile))[0] + ".run"
            cwd = os.getcwd()
            f = open(runfile, "w")
            f.write("#!/bin/bash\n")
            f.write("cd %s\n" % (cwd))
            f.write("%s\n"    % (cmd))
            f.close()
            os.chmod(runfile, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
            cmd = "ssh -t %s '%s/%s'" % (remote, cwd, runfile)
        success = True
        if simulate :
            try:
                subprocess.check_call(string.split(cmd))
            except subprocess.CalledProcessError, err :
                success = False
        else :
            print string.split(cmd)
            success = False
        if success and clean :
            root = os.path.splitext(os.path.basename(inpfile))[0]
            icfile = root + ".ic0"
            stfile = root + ".st0"
            vafile = root + ".valog"
            pvdir  = root + ".pvadir"
            for file in (outfile, inpfile, icfile, stfile, vafile) :
                try:
                    os.remove(file)
                except OSError, err :
                    print "failed to remove ", file
            try :
                shutil.rmtree(pvdir)
            except OSError, err :
                print "failed to remove ", pvdir
    #===========================================================================
    # METHOD  : __simulate_sspice
    # PURPOSE : simulation with sspice
    #===========================================================================
    def __simulate_sspice(self, simulate, clean, remote) :
        project = self["project"]
        inpfile = self.get_inputfile()
        outfile = self.get_outputfile()
        datfile = self.get_datafile()
        simargs = self["simulator_args"]
        sim  = os.path.expanduser("~/.DeCiDa/bin/") + "run_sspice"
        args = "-sb"
        cmd = "%s -quiet -project %s %s -o %s -r %s %s %s" % (
            sim, project, inpfile, outfile, datfile, args, simargs
        )
        if remote != "" :
            runfile=os.path.splitext(os.path.basename(inpfile))[0] + ".run"
            cwd = os.getcwd()
            f = open(runfile, "w")
            f.write("#!/bin/bash\n")
            f.write("cd %s\n" % (cwd))
            f.write("%s\n"    % (cmd))
            f.close()
            os.chmod(runfile, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
            cmd = "ssh -t %s '%s/%s'" % (remote, cwd, runfile)
        success = True
        if simulate :
            try:
                subprocess.check_call(string.split(cmd))
            except subprocess.CalledProcessError, err :
                success = False
        else :
            print string.split(cmd)
            success = False
        if success and clean :
            for file in (outfile, inpfile) :
                try:
                    os.remove(file)
                except OSError, err :
                    print "failed to remove ", file
    #===========================================================================
    # METHOD  : __simulate_ngspice
    # PURPOSE : simulation with ngspice
    #===========================================================================
    def __simulate_ngspice(self, simulate, clean, remote) :
        project = self["project"]
        inpfile = self.get_inputfile()
        outfile = self.get_outputfile()
        datfile = self.get_datafile()
        simargs = self["simulator_args"]
        sim = os.path.expanduser("~/.DeCiDa/bin/") + "run_ngspice"
        args = ""
        cmd = "%s -quiet -project %s -b %s -o %s -r %s %s %s" % (
            sim, project, inpfile, outfile, datfile, args, simargs
        )
        success = True
        if simulate :
            try:
                subprocess.check_call(string.split(cmd))
            except subprocess.CalledProcessError, err :
                success = False
        else :
            print string.split(cmd)
            success = False
        if success and clean :
            for file in (outfile, inpfile) :
                try:
                    os.remove(file)
                except OSError, err :
                    print "failed to remove ", file
    #===========================================================================
    # METHOD : number of data blocks
    # PURPOSE : return number of blocks in the simulated data file
    #===========================================================================
    def number_of_data_blocks(self):
        """ return number of blocks in the simulated data file.

        **results**:

            * count the number of lines begining with "Plotname" in a
              nutmeg-format data file.

        """
        datafile = self.get_datafile()
        f = open(datafile)
        nblocks = 0
        for line in f:
            if re.search("Plotname", line):
                nblocks += 1
        f.close()
        return nblocks
    #===========================================================================
    # METHOD : is_already_done
    # PURPOSE : return true if data file already exists
    #===========================================================================
    def is_already_done(self):
        """ return true if data file already exists.

        **results**:

            * return True if the data file is already present.  Can be used
              to re-perform an uncompleted loop of conditions, and skip
              the ones already performed.

        """
        datafile = self.get_datafile()
        prefix   = self["prefix"]
        if os.path.isfile(datafile) :
            if self["verbose"] :
                print "%s : already done" % (prefix)
            return True
        else :
            return False
    #===========================================================================
    # METHOD : no_data
    # PURPOSE : return true if data file doesn't exist
    #===========================================================================
    def no_data(self):
        """ return true if data file doesn't exist.

        **results**:

            * return True if there is no data file.  Can be used in a
              script report section to skip over loop-conditions which
              haven't been done yet.

        """
        datafile = self.get_datafile()
        prefix   = self["prefix"]
        if not os.path.isfile(datafile) :
            if self["verbose"] :
                print "%s : no data file" % (prefix)
            return True
        else :
            return False
    #===========================================================================
    # METHOD : wait_for_data
    # PURPOSE : wait until datafile appears and is non-zero
    #===========================================================================
    def wait_for_data(self, interval=5):
        """ wait until datafile appears and is non-zero.

        **arguments**:

            .. option:: interval (int, default=5)

                seconds to wait before re-checking for the existence of
                the data file.

        **results**:

            * the script waits until the data file has been produced and
              is not empty.

        """
        datafile = self.get_datafile()
        while True :
            if os.path.isfile(datafile) and os.path.getsize(datafile) > 0 :
                break
            time.sleep(interval)
            sys.stdout.write(".")
            sys.stdout.flush()
        sys.stdout.write("\n")
        return
    #===========================================================================
    # METHOD : stability_analysis
    # PURPOSE : perform stability analysis
    #===========================================================================
    def stability_analysis(self, plot=True, save=True) :
        """ perform stability analysis.

        **arguments**:

            .. option:: plot (bool, default=True)

                If True, plot loop-gain and loop-phase after simulation.

            .. option:: save (bool, default=True)

                If True, save the collated loop simulation results.

        """
        datafile = self.get_datafile()
        smeth  = self.__Stability["method"]
        vblock = self.__Stability["vblock"]
        iblock = self.__Stability["iblock"]
        if smeth == "middlebrook" :
            dv = Data()
            di = Data()
            dv.read_nutmeg(datafile, vblock)
            di.read_nutmeg(datafile, iblock)
            vc = self.__Stability["vdata"]
            ic = self.__Stability["idata"]
            dv.select(vc, "frequency")
            di.select(ic)
            dv.append_data(di)
            del di
            dv.cxset("%s = 1 - %s"  % (ic, ic))
            dv.cxset("AT = 1 / (%s + %s) - 1" % (vc, ic))
            dv.cxset("AV = 1 / %s - 1"  % (vc))
            dv.cxset("AI = 1 / %s - 1"  % (ic))
            if save :
                dv.write_csv("stab.csv")
            if plot :
                fn = FrameNotebook(tab_location="right")
                XYplotx(fn.new_page("AI"),
                    command=[dv, "frequency DB(AI) PH(AI)"],
                    xaxis="log", wait=False)
                XYplotx(fn.new_page("AV"),
                    command=[dv, "frequency DB(AV) PH(AV)"],
                    xaxis="log", wait=False)
                XYplotx(fn.new_page("AT"),
                    command=[dv, "frequency DB(AT) PH(AT)"],
                    xaxis="log", wait=False)
                fn.wait()
            #V=dv.low_pass_pars("frequency", "AV")
            V=dv.low_pass_pars("frequency", "AT")
            del dv
        elif smeth == "vbreak" :
            dv = Data()
            dv.read_nutmeg(datafile, vblock)
            vc = self.__Stability["vdata"]
            dv.select(vc, "frequency")
            dv.cxset("AV = - %s" % (vc))
            if save :
                dv.write_csv("stab.csv")
            if plot :
                fn = FrameNotebook(tab_location="right")
                XYplotx(fn.new_page("AV"),
                    command=[dv, "frequency DB(AV) PH(AV)"],
                    xaxis="log", wait=False)
                fn.wait()
            V=dv.low_pass_pars("frequency", "AV")
            del dv
        return(V)
    #===========================================================================
    # METHOD : dcop (spectre)
    # PURPOSE : view results from dc operating point analysis
    #===========================================================================
    def dcop(self, rawfile=None, lisfile=None,
        idmin=1e-8, vdssmin=0.01, verbose=False, block=0
    ) :
        """ view results from DC operating point analysis.

        **arguments**:

            .. option:: idmin (float, default=1e_8)

                The minimum drain current to consider a device as being on.

            .. option:: vdssmin (float, default=0.01)

                The minimum difference between the drain voltage and the
                saturation voltage to consider a device as being saturated.

            .. option:: verbose (bool, default=False)

                If True, print verbose messages.

            .. option:: block (int, default=0)

                Specify the block to process in the data file.

        """
        if rawfile is None :
            rawfile = self.get_datafile()
        if lisfile is None :
            lisfile = self.get_outputfile()
        idmin   = max(0.0,  idmin)
        vdssmin = max(0.01, vdssmin)
        if verbose :
            print "lisfile = ", lisfile
            print "rawfile = ", rawfile
        #----------------------------------------------------------------------
        # initialize
        #----------------------------------------------------------------------
        Devices = {}
        DevInfo = {}
        for type in ["b", "m", "c", "d", "r", "v", "i"] :
            Devices[type] = []
        Type = {
            "bjt"       : ["b", "devx"],
            "utsoi"     : ["m", "devc"],
            "capacitor" : ["c", "devx"],
            "diode"     : ["d", "devx"],
            "resistor"  : ["r", "devc"],
            "isource"   : ["i", "devx"],
            "vsource"   : ["v", "devx"],
        }
        Scale = {
            "T"   : 1e12,
            "G"   : 1e9,
            "M"   : 1e6,
            "K"   : 1e3,
            "m"   : 1e-3,
            "u"   : 1e-6,
            "n"   : 1e-9,
            "p"   : 1e-12,
            "f"   : 1e-15,
            "a"   : 1e-18,
        }
        mosfmt  = " %-s %2s %-10s %-10s"
        mosfmt += " id=%-12g vgs=%-12g vds=%-12g vbs=%-12g"
        mosfmt += " vth=%-12g vdsat=%-12g"
        mosfmt += " gm=%-12g gds=%-12g gmbs=%-12g"
        mosfmt += " cgs=%-12g cgd=%-12g cgb=%-12g cbs=%-12g cbd=%-12g"
        mosfmt += " vds-vdsat=%-12g"
        resfmt  = " %-s %-5s reff=%-12g i=%-12g v=%-12g power=%-12g"
        #----------------------------------------------------------------------
        # raw file contains voltages and currents
        #----------------------------------------------------------------------
        max_node = 0
        max_elem = 0
        nodes  = []
        elems  = []
        NV     = {}
        IE     = {}
        fn = FrameNotebook()
        if not rawfile :
            print "rawfile was not specified"
        elif not os.path.exists(rawfile) :
            print "rawfile \"%s\" is not readable" % (rawfile)
        else :
            #----------------------------------------------------------
            # parse raw file
            #----------------------------------------------------------
            fn.status("reading operating point *.raw file")
            if verbose : 
                print "reading raw file \"%s\"" % (rawfile)
            fn.status("parsing operating point *.raw file")
            if verbose : 
                print "  parsing"
            d = Data()
            d.read_nutmeg(rawfile, block)
            for name in d.names() :
                value = d.get_entry(0, name)
                m = re.search("^([^:]+):.+$", name)
                if m :
                    vori = "i"
                    norel = m.group(1)
                else :
                    vori = "v"
                    norel = name
                if  vori == "v" :
                    node = norel
                    max_node = max(max_node, len(node))
                    nodes.append(node)
                    NV[node] = value
                elif vori == "i" :
                    elem = norel
                    max_elem = max(max_elem, len(elem))
                    elems.append(elem)
                    IE[elem] = value
            #----------------------------------------------------------
            # raw file: node voltages
            #----------------------------------------------------------
            olines = []
            olines.append("%" * 72)
            olines.append("NODE VOLTAGES")
            olines.append("%" * 72)
            fmt = decida.interpolate(" %-${max_node}s %g")
            nodes.sort()
            for node in nodes :
                olines.append(fmt % (node, NV[node]))
            fnv = fn.new_page("node-voltages")
            tnv = TextWindow(fnv, text_height=30)
            tnv.enter(string.join(olines, "\n"))
            #----------------------------------------------------------
            # raw file: element currents
            #----------------------------------------------------------
            olines = []
            olines.append("%" * 72)
            olines.append("ELEMENT CURRENTS")
            olines.append("%" * 72)
            fmt = decida.interpolate(" %-${max_elem}s %g")
            elems.sort()
            for elem in elems :
                olines.append(fmt % (elem, IE[elem]))
            fec = fn.new_page("element-currents")
            tec = TextWindow(fec)
            tec.enter(string.join(olines, "\n"))
            fn.status("")
            fn.wait("Continue")
        #----------------------------------------------------------------------
        # lisfile contains device operating point info
        #----------------------------------------------------------------------
        if not fn :
            exit()
        if not lisfile :
            print "lisfile was not specified"
        elif not os.path.exists(lisfile) :
            print "lisfile \"%s\" is not readable" % (lisfile)
        else :
            #----------------------------------------------------------
            # parse lis file
            #----------------------------------------------------------
            fn.status("reading operating point *.lis file")
            if verbose:
                print "reading lis file \"%s\"" % (lisfile)
            lislines = decida.readfile2list(lisfile)
            fn.status("parsing operating point *.lis file")
            if verbose:
                print "  parsing"
            vers = None
            type = None
            mode = "null"
            for line in lislines :
                tline = string.split(line)
                if len(tline) > 0 :
                    kwd = tline[0]
                else :
                    kwd = ""
                    mode = "null"
                if kwd == "Version" :
                    if not vers:
                        vers = tline[1]
                    continue
                if kwd == "Total" :
                    type, mode = None, "null"
                    continue
                m = re.search("Instance:\s+([^ ]+)\s*$", line)
                if m :
                    device = m.group(1)
                    master = m.group(1)
                    continue
                m = re.search("Instance:\s+([^ ]+)\s+of\s+([^ ]+)\s*$", line)
                if m :
                    device = m.group(1)
                    master = m.group(2)
                    continue
                m = re.search("Model:\s+([^ ]+)\s*$", line)
                if m:
                    dmodel = m.group(1)
                    continue
                m = re.search("Primitive:\s+(\w+)$", line)
                if m:
                    mtype = m.group(1)
                    model = mtype + ":" + master
                    if   re.search("nfet", model) :
                        chan = "n"
                    elif re.search("pfet", model) :
                        chan = "p"
                    else :
                        chan = "?"
                    if mtype in Type:
                        type, mode = Type[mtype]
                        key = device + "-" + "model"
                        DevInfo[key] = model           # utsoi:masterlvtnfet
                        key = device + "-" + "type"
                        DevInfo[key] = type            # m
                        key = device + "-" + "chan"
                        DevInfo[key] = chan            # p/n
                        Devices[type].append(device)
                    else :
                        type, mode = None, "null"
                    continue
                if   mode == "devc" :
                    m = re.search("\s*(\w+)\s*=\s*([^ ]+)\s*$", line)
                    if m:
                        key = device + "-" + m.group(1)
                        val = m.group(2)
                        DevInfo[key] = val 
                    else :
                        m = re.search("\s*(\w+)\s*=\s*([^ ]+)\s(\w+)\s*$", line)
                        if m :
                            key = device + "-" + m.group(1)
                            val = m.group(2)
                            scale = m.group(3)
                            rval = float(val)
                            if scale in Scale :
                                rval *= Scale[scale]
                            val = str(rval)
                            DevInfo[key] = val 
                        else :
                            # also "node : V(node) = v V"
                            pass
            #----------------------------------------------------------
            # append device information
            #----------------------------------------------------------
            if verbose:
                print "  appending info"
            #---------------------------
            # MOSFETS
            #---------------------------
            olines = []
            triode_lines = []
            olines.append("%" * 72)
            olines.append("MOSFET OPERATING POINT PARAMETERS")
            olines.append(" (printed in NMOS format)")
            olines.append(" flags: p=pchannel n=nchannel -=inverted *=trioded")
            olines.append("%" * 72)
            mosfets = Devices["m"]
            mosfets.sort()
            max_name = 0
            for mosfet in mosfets :
                max_name = max(len(mosfet), max_name)
            name_fmt = decida.interpolate("%-${max_name}s")
            for mosfet in mosfets :
                model = DevInfo[mosfet + "-model"]
                type  = DevInfo[mosfet + "-type" ]
                chan  = DevInfo[mosfet + "-chan" ]
                id    = string.atof(DevInfo[mosfet + "-ids"  ])
                vds   = string.atof(DevInfo[mosfet + "-vds"  ])
                vgs   = string.atof(DevInfo[mosfet + "-vgs"  ])
                vbs   =-string.atof(DevInfo[mosfet + "-vsb"  ])
                vth   = string.atof(DevInfo[mosfet + "-vth"  ])
                vdsat = string.atof(DevInfo[mosfet + "-vdss" ])
                gm    = string.atof(DevInfo[mosfet + "-gm"   ])
                gds   = string.atof(DevInfo[mosfet + "-gds"  ])
                gmbs  = string.atof(DevInfo[mosfet + "-gmb"  ])
                cgs   = string.atof(DevInfo[mosfet + "-cgs"  ])
                cgd   = string.atof(DevInfo[mosfet + "-cgd"  ])
                cgb   = string.atof(DevInfo[mosfet + "-cgb"  ])
                capbs = string.atof(DevInfo[mosfet + "-cbs"  ])
                capbd = string.atof(DevInfo[mosfet + "-cbd"  ])
                #---------------------------
                # p-channel:
                #---------------------------
                if chan == "p" :
                    id = -id
                    vbs = -vbs
                    vgs = -vgs
                    vds = -vds
                    vth = -vth
                    vdsat = -vdsat
                #---------------------------
                # inverted?:
                #---------------------------
                finv = " "
                if vds < 0 :
                    finv = "-"
                    id = -id
                    vbs = vbs - vds
                    vgs = vgs - vds
                    vds = -vds
                #---------------------------
                # saturated?:
                #---------------------------
                sat = vds - vdsat
                fsat = " "
                if sat < vdssmin and abs(id) > idmin :
                    fsat = "*"
                    triode_lines.append(len(olines) + 1)
                #---------------------------
                # eliminate ".xmmaster.m1"
                #---------------------------
                name = re.sub("\.xmmaster\.m1$", "", mosfet)
                name = name_fmt % (name)
                flag = chan + finv + fsat
                olines.append(mosfmt % (name, flag, model, type,
                    id, vgs, vds, vbs,
                    vth, vdsat, gm, gds, gmbs, cgs, cgd, cgb,
                    capbs, capbd, sat))
            fmop = fn.new_page("mosfet-operating-pt")
            tmop = TextWindow(fmop)
            tmop.enter(string.join(olines, "\n"))
            for line in triode_lines :
                tmop.highlight_line(line)
            #---------------------------
            # Resistors
            #---------------------------
            olines = []
            olines.append("%" * 72)
            olines.append("RESISTOR OPERATING POINT PARAMETERS")
            olines.append(" flags: r=default -=inverted")
            olines.append("%" * 72)
            resistors = Devices["r"]
            resistors.sort()
            max_name = 0
            for resistor in resistors :
                max_name = max(len(resistor), max_name)
            name_fmt = decida.interpolate("%-${max_name}s")
            for resistor in resistors :
                model = DevInfo[resistor + "-model"]
                power = string.atof(DevInfo[resistor + "-pwr"])
                i     = string.atof(DevInfo[resistor + "-i"])
                v     = string.atof(DevInfo[resistor + "-v"])
                reff  = string.atof(DevInfo[resistor + "-res"])
                if model == "__rdefault" :
                    model = "r"
                finv = " "
                if v < 0 :
                    finv = "-"
                    v = -v
                    i = -i
                name = name_fmt % (resistor)
                flag = model + finv
                olines.append(resfmt % (name, flag, reff, i, v, power))
            frop = fn.new_page("resistor-operating-pt")
            trop = TextWindow(frop)
            trop.enter(string.join(olines, "\n"))
            #---------------------------
            # MOSFET sorted by current
            #---------------------------
            olines = []
            olines.append("%" * 72)
            olines.append("MOSFETS SORTED BY CURRENT")
            olines.append("%" * 72)
            mosfets = Devices["m"]
            mosfets.sort(cmp=Tckt.spectre_dcop_mosfet_id_sort)
            max_name = 0
            for mosfet in mosfets :
                max_name = max(len(mosfet), max_name)
            name_fmt = decida.interpolate("%-${max_name}s")
            for mosfet in mosfets :
                #---------------------------
                # eliminate ".xmmaster.m1"
                #---------------------------
                name = re.sub("\.xmmaster\.m1$", "", mosfet)
                name = name_fmt % (name)
                id = string.atof(DevInfo[mosfet + "-ids"])
                olines.append(" %-s %-12g" % (name, id))
            fms = fn.new_page("mosfets-by-current")
            tms = TextWindow(fms)
            tms.enter(string.join(olines, "\n"))
            fn.status("")
            fn.wait()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Tckt input file generation support methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #===========================================================================
    # METHOD  : __mosfet_device
    # PURPOSE : monitor ID(), etc. for full path to mosfet device in a subckt
    #===========================================================================
    def __mosfet_device(self, mosfet, type="") :
        name = str(mosfet)
        type = string.upper(type)
        if   type == "N" :
            dev = self.get_xnmos()
            if dev != "" :
                name += dev
        elif type == "P" :
            dev = self.get_xpmos()
            if dev != "" :
                name += dev
        elif type == "" :
            ndev = self.get_xnmos()
            pdev = self.get_xpmos()
            if (ndev == pdev) and ndev != "" :
                name += ndev
        return name
    #===========================================================================
    # METHOD  : __script_to_netlist
    # PURPOSE : map element name or string in script to match netlist
    # NOTES :
    #    * spectre escapes many characters
    #===========================================================================
    def __script_to_netlist(self, s) :
        if   self._netlist_format == "spectre" :
            chars = list("<>[]{}()")
            s2 = []
            for x in s:
                if x in chars:
                    s2.append("\\")
                s2.append(x)
            return(string.join(s2, ""))
            #return(re.escape(s))
        elif self._netlist_format == "spice" :
            return(string.lower(s))
    #===========================================================================
    # METHOD : __spectre_monitor_spec
    # PURPOSE : return save lines for input-file generation
    # NOTES :
    #   * called by generate_spectre_inputfile after simulator has been specified
    # ARGUMENTS :
    #   % flat   = False or True
    #      postlayout schematic is a test-bench with an embedded flat subcircuit
    #      subcircuit spec with % means postlayout starts here
    # EXAMPLES:
    #{
    #  @bx22.i396.%x2mux: ZNN_0
    #    generates save bx22.i396.x2mux.znn_0
    #  @%bx22.i396.x2mux: ZNN_0
    #    generates save bx22.i396/x2mux/znn_0
    #}
    #===========================================================================
    def __spectre_monitor_spec(self, flat=False) :
        delim  = "."
        delim1 = "."
        if flat :
            delim = "/"
        save_spec = []
        subckt = ""
        monitor_items = string.split(self.__monitor)
        for item in monitor_items :
            #-----------------------------------------------------------------
            # @subckt1.subckt2:
            #-----------------------------------------------------------------
            m = re.search("^@([^ ]*):$", item)
            if (m):
                subckt = m.group(1)
                nesc_subckt = subckt
                subckt = self.__script_to_netlist(subckt)
                #---------------------------------------------------------
                # postlayout:
                #---------------------------------------------------------
                for inst in self.__postlayout_instances :
                    m = re.match("%s\.(.+)" % (inst), nesc_subckt)
                    if m:
                        fsub   = m.group(1)
                        subs   = string.split(fsub, ".")
                        subckt = inst + "." + string.join(subs, "/")
                        delim1 = ":"
                        break
                continue
            #-------------------------------------------------------------
            # ID(mx)  (n/p-channel subcircuit mosfet) nch_* pch_*
            #-------------------------------------------------------------
            m = re.search("^ID\(([^ ]+)\)$", item)
            if m:
                mosfet = m.group(1)
                mosfet = self.__script_to_netlist(mosfet)
                mosfet = self.__mosfet_device(mosfet)
                if len(subckt) > 0 :
                    mosfet = subckt + delim1 + mosfet
                save_spec.append(mosfet + ":1")
                continue
            #-------------------------------------------------------------
            # IDN(mx)  (n-channel subcircuit mosfet) nch_*
            # IDP(mx)  (p-channel subcircuit mosfet) pch_*
            #-------------------------------------------------------------
            m = re.search("^ID(N|P)\(([^ ]+)\)$", item)
            if m:
                type   = m.group(1)
                mosfet = m.group(2)
                mosfet = self.__script_to_netlist(mosfet)
                mosfet = self.__mosfet_device(mosfet, type)
                if len(subckt) > 0 :
                    mosfet = subckt + delim1 + mosfet
                save_spec.append(mosfet + ":d")
                continue
            #-------------------------------------------------------------
            # PN(mx-vdsat)  (n-channel subcircuit mosfet) nch_*
            # PP(mx-vdsat)  (p-channel subcircuit mosfet) pch_*
            #-------------------------------------------------------------
            m = re.search("^P(N|P)\(([^ ]+)\)$", item)
            if m :
                type   = m.group(1)
                mospar = m.group(2)
                mosfet, par = string.split(mospar, "-")
                mosfet = self.__script_to_netlist(mosfet)
                mosfet = self.__mosfet_device(mosfet, type)
                if len(subckt) > 0 :
                    mosfet = subckt + delim1 + mosfet
                save_spec.append(mosfet + ":" + par)
                continue
            #-------------------------------------------------------------
            # IR(rx) (subcircuit resistor)
            #-------------------------------------------------------------
            m = re.search("^IR\(([^ ]+)\)$", item)
            if m :
                resistor = m.group(1)
                resistor = self.__script_to_netlist(resistor)
                resistor += ".r1"
                if len(subckt) > 0 :
                    resistor = subckt + delim1 + resistor
                save_spec.append(resistor + ":1")
                continue
            #-------------------------------------------------------------
            # IX(xm.node) (subcircuit)
            #-------------------------------------------------------------
            m = re.search("^IX\(([^ ]+)\)$", item)
            if m :
                x = m.group(1)
                tok = string.split(x, ".")
                if len(tok) == 2 :
                    xckt = tok[0]
                    node = tok[1]
                    xckt = self.__script_to_netlist(xckt)
                    node = self.__script_to_netlist(node)
                else :
                    self.warning("problem with IX specification")
                    return
                if len(subckt) > 0 :
                    xckt     = subckt + delim1 + xckt
                save_spec.append(xckt + ":" + node)
                continue
            #-------------------------------------------------------------
            # I(element)
            #-------------------------------------------------------------
            m = re.search("^I\(([^ ]+)\)$", item)
            if m :
                element = m.group(1)
                element = self.__script_to_netlist(element)
                if len(subckt) > 0 :
                    element = subckt + delim1 + element
                save_spec.append(element + ":1")
                continue
            #-------------------------------------------------------------
            # node1,node2
            #-------------------------------------------------------------
            m = re.search(",", item)
            if m :
                nodes = []
                for node in string.split(item, ",") :
                    node = self.__script_to_netlist(node)
                    if len(subckt) > 0 :
                        node = subckt + delim1 + node
                    nodes.append(node)
                nodes = string.join(nodes, ",")
                save_spec.append(nodes)
                continue
            #-------------------------------------------------------------
            # node_<10:0>
            #-------------------------------------------------------------
            m = re.search("^([a-zA-Z0-9_.!]+)<([0-9]+):([0-9]+)>$", item)
            if m :
                px = m.group(1)
                n2 = string.atoi(m.group(2))
                n1 = string.atoi(m.group(3))
                if n1 > n2 :
                    n1, n2 = n2, n1
                nodes = []
                for indx in range(n1, n2+1) :
                    node = px + "<" + str(indx) + ">"
                    node = self.__script_to_netlist(node)
                    if len(subckt) > 0 :
                        node  = subckt + delim1 + node
                    save_spec.append(node)
                continue
            #-------------------------------------------------------------
            # node
            #-------------------------------------------------------------
            node = item
            node = self.__script_to_netlist(node)
            if len(subckt) > 0 :
                node  = subckt + delim1 + node
            save_spec.append(node)
        return(save_spec)
    #===========================================================================
    # METHOD : __spice_monitor_spec
    # PURPOSE : return save lines for input-file generation
    # NOTES :
    #   * called by generate_inputfile after simulator has been specified
    # ARGUMENTS :
    #   % flat   = False or True
    #      postlayout schematic is a test-bench with an embedded flat subcircuit
    #      subcircuit spec with % means postlayout starts here
    # EXAMPLES:
    #{
    #  @Xbx22.Xi396.%Xx2mux: ZNN_0
    #    generates .save V(xbx22.xi396.xx2mux.znn_0)
    #  @%Xbx22.Xi396.Xx2mux: ZNN_0
    #    generates .save V(xbx22.xi396/xx2mux/znn_0)
    #}
    #===========================================================================
    def __spice_monitor_spec(self, flat=False) :
        delim  = "."
        delim1 = "."
        if flat :
            delim = "/"
        save_spec = []
        subckt = ""
        monitor_items = string.split(self.__monitor)
        for item in monitor_items :
            #-----------------------------------------------------------------
            # @Xsubckt1.Xsubckt2:
            #-----------------------------------------------------------------
            m = re.search("^@([^ ]*):$", item)
            if (m):
                subckt = m.group(1)
                subckt = string.lower(subckt)
                #---------------------------------------------------------
                # subcircuit instances must begin with x
                #---------------------------------------------------------
                slist = []
                for s in string.split(subckt) :
                    if not s[0] == "x":
                        slist.append("x" + s)
                    else :
                        slist.append(s)
                subckt = string.join(slist, ".")
                #---------------------------------------------------------
                # postlayout:
                #---------------------------------------------------------
                for inst in self.__postlayout_instances :
                    m = re.match("%s\.(.+)" % (inst), subckt)
                    if m:
                        fsub   = m.group(1)
                        subs   = string.split(fsub, ".")
                        subckt = inst + "." + string.join(subs, "/")
                        delim1 = ":"
                        break
                continue
            #-------------------------------------------------------------
            # ID(mx)  (n/p-channel subcircuit mosfet) nch_* pch_*
            #-------------------------------------------------------------
            m = re.search("^ID\(([^ ]+)\)$", item)
            if m:
                mosfet = m.group(1)
                mosfet = self.__script_to_netlist(mosfet)
                mosfet = self.__mosfet_device(mosfet)
                if len(subckt) > 0 :
                    mosfet = subckt + delim1 + mosfet
                save_spec.append("ID(" + mosfet + ")")
                continue
            #-------------------------------------------------------------
            # IDN(mx)  (n-channel subcircuit mosfet)
            # IDP(mx)  (p-channel subcircuit mosfet)
            # IDNH(mx) (n-channel subcircuit mosfet) high-v
            # IDPH(mx) (p-channel subcircuit mosfet) high-v
            #-------------------------------------------------------------
            m = re.search("^ID(N|P|NH|PH)\(([^ ]+)\)$", item)
            if m:
                type   = m.group(1)
                mosfet = m.group(2)
                mosfet = self.__mosfet_device(mosfet, type)
                if len(subckt) > 0 :
                    mosfet = subckt + delim1 + mosfet
                save_spec.append("I(" + mosfet + ")")
                continue
            #-------------------------------------------------------------
            # PN(mx-vdsat)  (n-channel subcircuit mosfet)
            # PP(mx-vdsat)  (p-channel subcircuit mosfet)
            # PNH(mx-vdsat) (n-channel subcircuit mosfet) high-v
            # PPH(mx-vdsat) (p-channel subcircuit mosfet) high-v
            #-------------------------------------------------------------
            m = re.search("^P(N|P|NH|PH)\(([^ ]+)\)$", item)
            if m :
                type   = m.group(1)
                mospar = m.group(2)
                mosfet, par = string.split(mospar, "-")
                mosfet = self.__mosfet_device(mosfet, type)
                if len(subckt) > 0 :
                    mosfet = subckt + delim1 + mosfet
                save_spec.append("@" + mosfet + "[" + par + "]")
                continue
            #-------------------------------------------------------------
            # IR(rx) (subcircuit resistor)
            #-------------------------------------------------------------
            m = re.search("^IR\(([^ ]+)\)$", item)
            if m :
                resistor = m.group(1)
                resistor = string.lower(resistor)
                resistor += ".r1"
                if resistor[0] != "x" :
                    resistor = "x" + resistor
                if len(subckt) > 0 :
                    resistor = subckt + delim1 + resistor
                save_spec.append("I(" + resistor + ")")
                continue
            #-------------------------------------------------------------
            # IX(xm.node) (subcircuit)
            #-------------------------------------------------------------
            m = re.search("^IX\(([^ ]+)\)$", item)
            if m :
                x = m.group(1)
                tok = string.split(x, ".")
                if len(tok) == 2 :
                    xckt = tok[0]
                    node = tok[1]
                else :
                    self.warning("problem with IX specification")
                    return
                xckt = string.lower(xckt)
                node = string.lower(node)
                if len(subckt) > 0 :
                    xckt     = subckt + delim1 + xckt
                save_spec.append("I(" + xckt + "." + node + ")")
                continue
            #-------------------------------------------------------------
            # I(element)
            #-------------------------------------------------------------
            m = re.search("^I\(([^ ]+)\)$", item)
            if m :
                element = m.group(1)
                element = string.lower(element)
                if len(subckt) > 0 :
                    type = element[0]
                    element = subckt + delim1 + element
                save_spec.append("I(" + element + ")")
                continue
            #-------------------------------------------------------------
            # node1,node2
            #-------------------------------------------------------------
            m = re.search(",", item)
            if m :
                item = string.lower(item)
                nodes = []
                for node in string.split(item, ",") :
                    if len(subckt) > 0 :
                        node = subckt + delim1 + node
                    nodes.append(node)
                nodes = string.join(nodes, ",")
                save_spec.append("V(" + nodes + ")")
                continue
            #-------------------------------------------------------------
            # node_<10:0>
            #-------------------------------------------------------------
            m = re.search("^([a-zA-Z0-9_.!]+)<([0-9]+):([0-9]+)>$", item)
            if m :
                px = m.group(1)
                n2 = string.atoi(m.group(2))
                n1 = string.atoi(m.group(3))
                if n1 > n2 :
                    n1, n2 = n2, n1
                px = string.lower(px)
                nodes = []
                for indx in range(n1, n2+1) :
                    node = px + str(indx)
                    # gateway:
                    node = px + "<" + str(indx) + ">"
                    if len(subckt) > 0 :
                        node  = subckt + delim1 + node
                    save_spec.append("V(" + node + ")")
                continue
            #-------------------------------------------------------------
            # node
            #-------------------------------------------------------------
            node = string.lower(item)
            if len(subckt) > 0 :
                node  = subckt + delim1 + node
            save_spec.append("V(" + node + ")")
        return(save_spec)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Tckt value-generators for sources
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #===========================================================================
    # METHOD  : __register_setting_to_binary
    # PURPOSE : convert verilog setting format 7'b1010111 to binary number
    # NOTES :
    #   * binary, octal, hexadecimal and decimal format
    #===========================================================================
    def __register_setting_to_binary(self, setting) :
        D = {
            2: "^([0-9]+)'b([01]+)$",
            8: "^([0-9]+)'o([0-7]+)$",
           10: "^([0-9]+)'d([0-9]+)$",
           16: "^([0-9]+)'h([0-9a-fA-F]+)$",
        }
        binary = None
        for base in D.keys() :
            m = re.search(D[base], setting)
            if m :
                nbit = string.atoi(m.group(1))
                num  = m.group(2)
                binary = decida.baseconvert(base, 2, num, nbit)
                break
        return binary
    #===========================================================================
    # METHOD : __set_register
    # PURPOSE : generate bus supply values
    # ARGUMENTS :
    #   % register
    #   % value
    #===========================================================================
    def __set_register(self, register, value, args) :
        v0 = 0.0
        v1 = 1.2
        for key, val in args.items() :
            if   key == "v0" :
                v0 = string.atof(val)
            elif key == "v1" :
                v1 = string.atof(val)
        m = re.search("^([a-zA-Z0-9_.!]+)<([0-9]+):([0-9]+)>$", register)
        if m :
            px = m.group(1)
            n2 = string.atoi(m.group(2))
            n1 = string.atoi(m.group(3))
            if n2 < n1 :
                n2, n1 = n1, n2
            #-----------------------------------------------------------------
            # apply to each supply in the bus
            # value can be a verilog specification, single value, or netlist
            #-----------------------------------------------------------------
            binary = self.__register_setting_to_binary(value)
            if binary :
                if len(binary) != (n2-n1+1) :
                    self.warning("register specification too long or too short")
                for bit, index in zip(binary, range(n2, n1-1, -1)) :
                    vbit = v1 if bit == "1" else v0
                    value = str(vbit)
                    element = px + "<" + str(index) + ">"
                    element = self.__script_to_netlist(element)
                    self.__Element[element] = value
            else :
                for index in range(n1, n2+1) :
                    element = px + "<" + str(index) + ">"
                    element = self.__script_to_netlist(element)
                    self.__Element[element] = value
        else :
            #-----------------------------------------------------------------
            # not a bus
            # value can be number or "netlist"
            #-----------------------------------------------------------------
            element = register
            element = self.__script_to_netlist(element)
            self.__Element[element] = value
    #===========================================================================
    # METHOD : __counter
    # PURPOSE : generate bus supply values for a counter
    # ARGUMENTS :
    #   % register
    #       register expression for control bus
    #   % args
    #       OPTIONS
    # OPTIONS :
    #   % v0        <v>
    #       signal value corresponding to 0 in generated bit pattern (default=0)
    #   % v1        <v>
    #       signal value corresponding to 1 in generated bit pattern (default=1)
    #   % min (or beg)
    #       minimum count (default = 0)
    #   % max (or end)
    #       maximum count (default = 2^(register_high-register_low+1) - 1)
    #   % step
    #       step in count (default = 1)
    #   % random
    #       specify number of random steps between min and max
    #   % tdelay (or delay)
    #       time delay    (default = 0)
    #   % tedge (or edge)
    #       rise and fall times (default = 1ns)
    #   % thold (or hold)
    #       hold time at each bit (default = 100ns)
    #   % continued 
    #       produce continued time/value lines in the netlist (default = 0)
    #   % repeat <count>
    #       repeat counting
    # RESULTS : 
    #   * sets the supply value to the PWL specification
    #===========================================================================
    def __counter(self, register, args) :
        m = re.search("^([a-zA-Z0-9_.!]+)<([0-9]+):([0-9]+)>$", register)
        if m :
            px = m.group(1)
            n2 = string.atoi(m.group(2))
            n1 = string.atoi(m.group(3))
            if n2 < n1 :
                n2, n1 = n1, n2
        else :
            self.fatal("register_expr is not in expected format (ex: VM<9:0>)")
        v0        =  0.0
        v1        =  1.0
        min       =  0
        max       =  pow(2, n2-n1+1) - 1
        step      =  1
        random    =  0
        delay     =  0.0
        edge      =  1e-9
        hold      =  100e-9
        repeat    =  1
        continued =  False
        for key, val in args.items() :
            if   key == "v0" :
                v0 = float(val)
            elif key == "v1" :
                v1 = float(val)
            elif key == "min" or key == "beg":
                min = float(val)
            elif key == "max" or key == "end":
                max = float(val)
            elif key == "step" :
                step = float(val)
            elif key == "random" :
                random = int(val)
            elif key == "delay" or key == "tdelay" :
                delay = float(decida.spice_value(val))
            elif key == "edge"  or key == "tedge" :
                edge = float(decida.spice_value(val))
            elif key == "hold"  or key == "thold" :
                hold = float(decida.spice_value(val))
            elif key == "continued" :
                continued = bool(val)
        #---------------------------------------------------------------------
        # generate counter values
        #---------------------------------------------------------------------
        if random > 0 :
            settings = [int(round(s)) for s in decida.range_sample(min, max, num=random, mode="uniform")]
        else :
            settings = [int(round(s)) for s in decida.range_sample(min, max, step=step)]
        #---------------------------------------------------------------------
        # repeat
        #---------------------------------------------------------------------
        if repeat > 1 :
            newsettings = []
            for i in range(1, repeat+1) :
                newsettings += settings
            settings = newsettings
        #---------------------------------------------------------------------
        # generate pwl values
        #---------------------------------------------------------------------
        time = 0.0
        PWL = {}
        for setting in settings :
            time1 = time  + edge
            time2 = time1 + hold
            mask = 1
            for index in range(n1, n2+1) :
                val = v1 if (setting & mask) != 0 else v0
                mask *= 2
                if time == 0.0 :
                    PWL[index] = (time, val)
                PWL[index] += (time1, val)
                PWL[index] += (time2, val)
            time = time2
        #---------------------------------------------------------------------
        # apply to each supply in the bus
        #---------------------------------------------------------------------
        sep = "\n+" if continued else " "
        for index in range(n1, n2+1) :
            element = px + "<" + str(index) + ">"
            element = self.__script_to_netlist(element)
            value = "PWL"
            for time, val in zip(PWL[index][0::2], PWL[index][1::2]) :
                value += sep + str(time) + " " + str(val)
            if delay > 0.0 :
                value += " TD=" + str(delay)
            self.__Element[element]=value
    #===========================================================================
    # METHOD : __prbs
    # PURPOSE : prbs pattern
    #===========================================================================
    def __prbs(self, element, args) :
        v0        =  0.0
        v1        =  1.0
        size      =  7
        length    =  0
        data_rate =  2.5e9
        edge      =  0.0
        delay     =  0.0
        pre       = ""
        post      = ""
        continued =  False
        for key, val in args.items() :
            if   key == "v0" :
                v0 = float(val)
            elif key == "v1" :
                v1 = float(val)
            elif key == "size" :
                size = int(val)
            elif key == "length" :
                length= int(val)
            elif key == "data_rate" :
                data_rate = float(decida.spice_value(val))
            elif key == "delay" or key == "tdelay" :
                delay = float(decida.spice_value(val))
            elif key == "edge"  or key == "tedge" :
                edge = float(decida.spice_value(val))
            elif key == "pre" :
                pre   = str(val)
            elif key == "post" :
                post   = str(val)
            elif key == "continued" :
                continued = bool(val)
        #---------------------------------------------------------------------
        # generate PWL pattern
        #---------------------------------------------------------------------
        period = 1.0/data_rate
        if edge <= 0 :
            edge = 0.10*period
        if length < 1 :
            length = int(math.pow(2, size))
        ptrn = Pattern(v0=v0, v1=v1, delay=delay, edge=edge, period=period,
            format="pwl", pre=pre, post=post)
        pattern = ptrn.prbs(size=size, length=length)
        del ptrn
        #---------------------------------------------------------------------
        # generate pwl values
        #---------------------------------------------------------------------
        element = self.__script_to_netlist(element)
        value = "PWL"
        sep = "\n+" if continued else " "
        value = "PWL"
        for time, val in zip(pattern[0::2], pattern[1::2]) :
            value += sep + str(time) + " " + str(val)
        self.__Element[element]=value
    #===========================================================================
    # METHOD : __rand
    # PURPOSE : rand pattern
    #===========================================================================
    def __rand(self, element, args) :
        v0        =  0.0
        v1        =  1.0
        length    =  1000
        data_rate =  2.5e9
        edge      =  0.0
        delay     =  0.0
        pre       = ""
        post      = ""
        continued =  False
        seed      = None
        for key, val in args.items() :
            if   key == "v0" :
                v0 = float(val)
            elif key == "v1" :
                v1 = float(val)
            elif key == "length" :
                length= int(val)
            elif key == "data_rate" :
                data_rate = float(decida.spice_value(val))
            elif key == "delay" or key == "tdelay" :
                delay = float(decida.spice_value(val))
            elif key == "edge"  or key == "tedge" :
                edge = float(decida.spice_value(val))
            elif key == "pre" :
                pre   = str(val)
            elif key == "post" :
                post   = str(val)
            elif key == "seed" :
                seed   = str(val)
            elif key == "continued" :
                continued = bool(val)
        #---------------------------------------------------------------------
        # generate PWL pattern
        #---------------------------------------------------------------------
        period = 1.0/data_rate
        if edge <= 0 :
            edge = 0.10*period
        ptrn = Pattern(v0=v0, v1=v1, delay=delay, edge=edge, period=period,
            format="pwl", pre=pre, post=post)
        if not seed is None :
            pattern = ptrn.rand(length=length, seed=seed)
        else :
            pattern = ptrn.rand(length=length)
        del ptrn
        #---------------------------------------------------------------------
        # generate pwl values
        #---------------------------------------------------------------------
        element = self.__script_to_netlist(element)
        value = "PWL"
        sep = "\n+" if continued else " "
        value = "PWL"
        for time, val in zip(pattern[0::2], pattern[1::2]) :
            value += sep + str(time) + " " + str(val)
        self.__Element[element]=value
    #===========================================================================
    # METHOD : __bits
    # PURPOSE : bit pattern
    #===========================================================================
    def __bits(self, element, args) :
        v0        =  0.0
        v1        =  1.0
        data_rate =  2.5e9
        edge      =  0.0
        delay     =  0.0
        pattern   = ""
        continued =  False
        for key, val in args.items() :
            if   key == "v0" :
                v0 = float(val)
            elif key == "v1" :
                v1 = float(val)
            elif key == "data_rate" :
                data_rate = float(decida.spice_value(val))
            elif key == "delay" or key == "tdelay" :
                delay = float(decida.spice_value(val))
            elif key == "edge"  or key == "tedge" :
                edge = float(decida.spice_value(val))
            elif key == "pattern" :
                pattern = str(val)
            elif key == "continued" :
                continued = bool(val)
        #---------------------------------------------------------------------
        # generate PWL pattern
        #---------------------------------------------------------------------
        period = 1.0/data_rate
        if edge <= 0 :
            edge = 0.10*period
        ptrn = Pattern(v0=v0, v1=v1, delay=delay, edge=edge, period=period,
            format="pwl")
        pattern = ptrn.pattern(pattern)
        del ptrn
        #---------------------------------------------------------------------
        # generate pwl values
        #---------------------------------------------------------------------
        element = self.__script_to_netlist(element)
        value = "PWL"
        sep = "\n+" if continued else " "
        value = "PWL"
        for time, val in zip(pattern[0::2], pattern[1::2]) :
            value += sep + str(time) + " " + str(val)
        self.__Element[element]=value
    #===========================================================================
    # METHOD : __clock
    # PURPOSE : clock pattern
    #===========================================================================
    def __clock(self, element, args) :
        v0        =  0.0
        v1        =  1.0
        freq      =  2.5e9
        edge      =  0.0
        delay     =  0.0
        duty      =  50.0
        for key, val in args.items() :
            if   key == "v0" :
                v0 = float(val)
            elif key == "v1" :
                v1 = float(val)
            elif key == "duty" :
                duty = float(val)
            elif key == "length" :
                length= int(val)
            elif key == "freq" :
                freq = float(decida.spice_value(val))
            elif key == "delay" or key == "tdelay" :
                delay = float(decida.spice_value(val))
            elif key == "edge"  or key == "tedge" :
                edge = float(decida.spice_value(val))
        #---------------------------------------------------------------------
        # generate PULSE
        #---------------------------------------------------------------------
        period = 1.0/freq
        if edge <= 0 :
            edge = 0.10*period
        width = duty*0.01*period - edge
        #---------------------------------------------------------------------
        # generate pwl values
        #---------------------------------------------------------------------
        element = self.__script_to_netlist(element)
        value = "PULSE %s %s %s %s %s %s %s" % \
            (v0, v1, delay, edge, edge, width, period)
        self.__Element[element]=value
    #===========================================================================
    # METHOD : __therm
    # PURPOSE : thermometer code
    #===========================================================================
    def __therm(self, register, args) :
        m = re.search("^([a-zA-Z0-9_.!]+)<([0-9]+):([0-9]+)>$", register)
        if m :
            px = m.group(1)
            n2 = string.atoi(m.group(2))
            n1 = string.atoi(m.group(3))
            if n2 < n1 :
                n2, n1 = n1, n2
        else :
            self.fatal("register_expr is not in expected format (ex: VM<9:0>)")
        v0        =  0.0
        v1        =  1.0
        value     =  0
        for key, val in args.items() :
            if   key == "v0" :
                v0 = float(val)
            elif key == "v1" :
                v1 = float(val)
            elif key == "value" :
                value = int(val)
        #---------------------------------------------------------------------
        # generate thermometer code values
        #---------------------------------------------------------------------
        nbits = n2-n1+1
        Thm = [v1 if i < value else v0 for i in range(nbits)]
        Thm.reverse()
        #---------------------------------------------------------------------
        # apply to each supply in the bus
        #---------------------------------------------------------------------
        for index in range(n1, n2+1) :
            element = px + "<" + str(index) + ">"
            element = self.__script_to_netlist(element)
            self.__Element[element]=str(Thm[index-n1])
