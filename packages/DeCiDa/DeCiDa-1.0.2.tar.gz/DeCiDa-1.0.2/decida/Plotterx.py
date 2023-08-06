################################################################################
# CLASS    : Plotterx
# PURPOSE  : function plotting class
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:23:41 2013
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
import sys
import os
import os.path
import string
import re
import numpy
import decida
import math
import time
import stat
from decida.entry_emacs_bindings import *
from decida.ItclObjectx      import ItclObjectx
from decida.Data             import Data
from decida.DataViewx        import DataViewx
from decida.XYplotx          import XYplotx
from decida.SelectionDialog  import SelectionDialog
from decida.EquationParser   import EquationParser
import Tkinter
from Tkinter import *
import tkFileDialog

class Plotterx(ItclObjectx, Frame) :
    """ graphical user-interface to plot equation sets.

    **synopsis**:

    Plotterx is a graphical user-interface to plot the left-hand-side
    variables of a set of equations, specified in a text-window in the panel.
    Cartesian, parametric, polar or polar-parametric curves can be specified
    and plotted.  The equation set experiments can be saved to a script
    which, when invoked, puts up the same Plotterx window.

    The DeCiDa application *plotter* simply instantiates one Plotterx object.

    **constructor arguments**:

        .. option:: parent (Tkinter handle)

           handle of frame or other widget to pack plot in.
           if this is not specified, top-level is created.

        .. option:: \*\*kwargs (dict)

           configuration-options

    **configuration options**:
 
        .. option:: verbose (bool, default=False)

           Enable or disable verbose mode

        .. option:: plot_width (string, default="5i")

           Plot width, specified in Tk inch or pixel units

        .. option:: plot_height (string, default="5i")

           Plot height, specified in Tk inch or pixel units

        .. option:: plot_type (string, default="cartesian")

           Plot type: one of "cartesian", "cartesian-parametric",
               "polar", or "polar-parametric"

           * Cartesian plots: y vs x, require specification
             of an x variable to vary, its range,
             and a y variable.

           * Parametric plots: y(t) vs x(t), require specification
             of a parameter variable to vary, its range,
             and x and y variables to plot.

           * Polar plots: r(a) require specification
             of an angle variable to vary, its range, and a radius variable.
             x(r,a) and y(r,a) are plotted.

           * Polar-parametric plots: r(t), a(t), require specification
             of a parameter variable to vary, its range,
             and angle and radius variables.
             x(r,a) and y(r,a) are plotted.

        .. option:: sample_type (string, default="linear")

           Sample type: one of "linear", or "logarithmic"

           * linear sampling: equally-spaced samples from the minimum
             to maximum values of the varied variable or parameter

           * logarithmic sampling: the parameter is varied according to
             (maximum_value/minimum_value)^(i/(number_of_points - 1)),
             for i in range(0, number_of_points)
           
        .. option:: xcol (string) (default="x")

           x-axis column (sweep for caresian plots)

        .. option:: ycol (string) (default="y")

           y-axis column

        .. option:: acol (string) (default="a")

           angle column (sweep for polar plots)

        .. option:: rcol (string) (default="r")

           radius column (for polar and polar-parametric plots)

        .. option:: tcol (string) (default="t")

           parameter column (sweep for cartesian-parametric and 
              polar-parametric plots)

        .. option:: npts (int) (default=1000)

           number of sample points

        .. option:: min (float) (default=0.0)

           minimum of sampling

        .. option:: max (float) (default=5.0)

           maximum of sampling

    **example**: (from test_Plotterx) ::

        from decida.Plotterx import Plotterx
        Plotterx(ycol="v", xcol="time", equations="v=sin(time*3)")

    **public methods**:

        * public methods from *ItclObjectx*

    """
    _Curves = {
        "Hyperbola":     (
             "cartesian", -100, 100, 
             """
               # Hyperbola
               A=3
               y=A/x
             """
        ),
        "WitchOfAgnesi": (
             "cartesian", -100, 100,
             """
               # Witch of Agnesi
               A=2
               y=A/((x/A)^2 + 1)
             """
        ),
        "Serpentine" : (
             "cartesian", -100, 100,
             """
               # Serpentine
               A=2; B=3
               y=x/((x/A)^2 + B^2)
             """
        ),
        "QuatrixOfHippias" : (
             "cartesian", 0.1, 8,
             """
               # Quatrix of Hippias
               A=3
               y=x/tan(A*x)
             """
        ),
        "TridentOfNewton" : (
             "cartesian", -6, 6,
             """
               # Trident of Newton
               A=3; B=4; C=5; D=7
               y=A/x+B+C*x+D*x*x
             """
        ),
        "Polynomial" : (
             "cartesian", -100, 100,
             """
               # Polynomial
               A=3; B=4; C=5; D=7
               y=A+B*x+C*x^2+D*x^3
             """
        ),
        "NormalErrorCurve" : (
             "cartesian", -4, 4,
             """
               # Normal Error Curve
               A=0; S=1
               q=S*(x-A)
               pi=acos(-1)
               y=S/exp(pi*q*q)
             """
        ),
        "Catenary" : (
             "cartesian", -5, 5,
             """
               # Catenary Curve,
               A=2
               q=A*x
               e=exp(q)
               cosh=0.5*(e+1/e)
               y=cosh/(2*A)
             """
        ),
        "CrossCurve" : (
             "cartesian-parametric", -10, 10,
             """
               # Cross Curve
               A=3; B=4
               x=A/cos(t)
               y=B/sin(t)
             """
        ),
        "BulletNose" : (
             "cartesian-parametric", -10, 10,
             """
               # Bullet Nose
               A=3
               x=A*cos(t)
               y=A/tan(t)
             """
        ),
        "LemniscateOfBernoulli" : (
             "cartesian-parametric", -3.142, 3.142,
             """
               # Lemniscate of Bernoulli
               A=3
               x=A*cos(t)/(sin(t)*sin(t)+1)
               y=A*sin(t)*cos(t)/(sin(t)*sin(t)+1)
             """
        ),
        "LemniscateOfGerono" : (
             "cartesian-parametric", -3.142, 3.142,
             """
               # Lemniscate of Gerono
               A=3
               x=A*cos(t)
               y=A*sin(t)*cos(t)
             """
        ),
        "LissajousPattern" : (
             "cartesian-parametric", -3.142, 3.142,
             """
               # Lissajous Pattern
               A=3; B=4; C=5; D=6
               x=A*sin(t)
               y=B*sin(C*t+D)
             """
        ),
        "Epitrochoid" : (
             "cartesian-parametric", -3.142, 3.142,
             """
               # Epitrochoid
               A=3; B=5; C=7
               x=A*(B*cos(t)-C*cos(B*t))
               y=A*(B*sin(t)-C*sin(B*t))
             """
        ),
        "Hypotrochoid" : (
             "cartesian-parametric", -3.142, 3.142,
             """
               # Hypotrochoid
               A=3; B=5; C=7
               x=A*(B*cos(t)+C*cos(B*t))
               y=A*(B*sin(t)-C*sin(B*t))
             """
        ),
        "Trochoid" : (
             "cartesian-parametric", -20, 20,
             """
               # Trochoid
               A=3; B=5
               x=A*(t-B*sin(t))
               y=A*(1-B*cos(t))
             """
        ),
        "PedalsOfParabola" : (
             "cartesian-parametric", -1.5, 1.5,
             """
               # Pedals of a Parabola
               A=3; B=5
               x=A*cos(t)*cos(t)*(tan(t)*tan(t)-B)
               y=A*sin(t)*cos(t)*(tan(t)*tan(t)-B)
             """
        ),
        "InvoluteOfCircle" : (
             "cartesian-parametric", -20, 20,
             """
               # Involute of a Circle
               A=3
               x=A*(cos(t)+t*sin(t))
               y=A*(sin(t)-t*cos(t))
             """
        ),
        "LimaconOfPascal" : (
             "polar", -3.142, 3.142,
             """
               # Limacon of Pascal
               A=2; B=0.5
               r=A*(cos(a)+B)
             """
        ),
        "ConchoidOfNichomedes" : (
             "polar", -3, 3,
             """
               # Conchoid of Nichomedes
               A=3; B=5
               r=A*(cos(a)+B)/cos(a)
             """
        ),
        "KappaCurve" : (
             "polar", -10, 10,
             """
               # Kappa Curve
               A=3
               r=A/tan(a)
             """
        ),
        "KampyleOfEudoxus" : (
             "polar", -1.5, 1.5,
             """
               # Kampyle of Eudoxus
               A=3
               c=cos(a)
               r=A/(c*c)
             """
        ),
        "Folium" : (
             "polar", 0, 3.142,
             """
               # Folium
               A=3; B=0.3
               c=cos(a)
               s=sin(a)
               r=A*c*(s*s-B)
             """
        ),
        "FoliumOfDescartes" : (
             "polar", -0.6, 2.2,
             """
               # Folium of Descartes
               A=3
               c=cos(a)
               s=sin(a)
               r=A*c*s/(c^3+s^3)
             """
        ),
        "SemiCubicalParabola" : (
             "polar", -1.5, 1.5,
             """
               # Semi-cubical Parabola
               A=3
               c=cos(a)
               q=tan(a)
               r=A*q*q/c
             """
        ),
        "Cochleoid" : (
             "polar", -100, 100,
             """
               # Cochleoid
               A=3
               r=A*sin(a)/a
             """
        ),
        "Rhodonea" : (
             "polar", -3.142, 3.142,
             """
               # Rhodonea
               A=4
               r=cos(A*a)
             """
        ),
        "NephroidOfFreeth" : (
             "polar-parametric", -3.142, 3.142,
             """
               # Nephroid of Freeth
               A=3
               a=2*t
               r=A*(sin(t)+0.5)
             """
        ),
        "CayleysSextic" : (
             "polar-parametric", 0, 3.142,
             """
               # Cayley's Sextic
               A=3
               a=3*t
               q=cos(t)
               r=A*(q*q*q)
             """
        ),
        "TschirnhausensCubic" : (
             "polar-parametric", -1.5, 1.5,
             """
               # Tschirnhausen's Cubic
               A=3
               a=3*t
               q=cos(t)
               r=A/(q*q*q)
             """
        ),
        "LogarithmicSpiral" : (
             "polar-parametric", -10, 10,
             """
               # Logarithmic Spiral
               A=3; B=7
               a=t/B
               r=A*exp(t)
             """
        ),
        "ArchimedesSpiral" : (
             "polar-parametric", -10, 10,
             """
               # Archimede's Spiral
               A=3
               a=t
               r=A*t
             """
        ),
        "HyperbolicSpiral" : (
             "polar-parametric", -10, 10,
             """
               # Hyperbolic Spiral
               A=3
               a=t
               r=A/t
             """
        ),
        "EpiSpiral" : (
             "polar-parametric", -1.5, 1.5,
             """
               # Epi Spiral
               A=3; B=7
               a=t/B
               r=A/cos(t)
             """
        ),
        "PoinsotsSpiral1" : (
             "polar-parametric", -10, 10,
             """
               # Poinsot's Spiral number 1
               A=3; B=7
               a=t/B
               e=exp(t)
               cosh=0.5*(e+1/e)
               r=A/cosh
             """
        ),
        "PoinsotsSpiral2" : (
             "polar-parametric", -10, 10,
             """
               # Poinsot's Spiral number 2
               A=3; B=7
               a=t/B
               e=exp(t)
               sinh=0.5*(e-1/e)
               r=A/sinh
             """
        ),
    }
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Plotterx main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__parent    = parent
        self.__Component = {}
        self.__data_obj  = None
        self.__dataview  = None
        self.__equations = None
        self.__plotter_root = "plot"
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        if sys.platform == "darwin" :
            plot_width  = "8i"
            plot_height = "8i"
        else :
            plot_width  = "5i"
            plot_height = "5i"
        self._add_options({
            "verbose"        : [False, None],
            "plot_width"     : [plot_width, None],
            "plot_height"    : [plot_height, None],
            "plot_type"      : ["cartesian", self._config_plot_type_callback],
            "sample_type"    : ["linear",    self._config_sample_type_callback],
            "xcol"           : ["x",         self._config_xcol_callback],
            "ycol"           : ["y",         self._config_ycol_callback],
            "acol"           : ["theta",     self._config_acol_callback],
            "rcol"           : ["r",         self._config_rcol_callback],
            "tcol"           : ["t",         self._config_tcol_callback],
            "npts"           : [1000,        self._config_npts_callback],
            "min"            : [0.0,         self._config_min_callback],
            "max"            : [5.0,         self._config_max_callback],
        })
        #----------------------------------------------------------------------
        # keyword arguments are *not* all configuration options
        #----------------------------------------------------------------------
        for key, value in kwargs.items() :
            if key == "equations" :
                self.__equations = value
            else :
                self[key] = value
        #----------------------------------------------------------------------
        # build gui:
        #----------------------------------------------------------------------
        self.__gui()
    #===========================================================================
    # METHOD  : __del__
    # PURPOSE : destructor
    #===========================================================================
    def __del__(self) :
        if self.__toplevel :
            self.__toplevel.destroy()
        else :
            self.destroy()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Plotterx configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #===========================================================================
    # METHOD  : _config_xcol_callback
    # PURPOSE : configure xcol
    #===========================================================================
    def _config_xcol_callback(self) :
        self.__entry_enter("xcol")
    #===========================================================================
    # METHOD  : _config_ycol_callback
    # PURPOSE : configure ycol
    #===========================================================================
    def _config_ycol_callback(self) :
        self.__entry_enter("ycol")
    #===========================================================================
    # METHOD  : _config_acol_callback
    # PURPOSE : configure acol
    #===========================================================================
    def _config_acol_callback(self) :
        self.__entry_enter("acol")
    #===========================================================================
    # METHOD  : _config_rcol_callback
    # PURPOSE : configure rcol
    #===========================================================================
    def _config_rcol_callback(self) :
        self.__entry_enter("rcol")
    #===========================================================================
    # METHOD  : _config_tcol_callback
    # PURPOSE : configure tcol
    #===========================================================================
    def _config_tcol_callback(self) :
        self.__entry_enter("tcol")
    #===========================================================================
    # METHOD  : _config_npts_callback
    # PURPOSE : configure npts
    #===========================================================================
    def _config_npts_callback(self) :
        self.__entry_enter("npts")
    #===========================================================================
    # METHOD  : _config_min_callback
    # PURPOSE : configure min
    #===========================================================================
    def _config_min_callback(self) :
        self.__entry_enter("min")
    #===========================================================================
    # METHOD  : _config_max_callback
    # PURPOSE : configure max
    #===========================================================================
    def _config_max_callback(self) :
        self.__entry_enter("max")
    #===========================================================================
    # METHOD  : _config_plot_type_callback
    # PURPOSE : configure plot_type
    #===========================================================================
    def _config_plot_type_callback(self) :
        plot_type = self["plot_type"]
        plot_types = ("cartesian", "cartesian-parametric",
            "polar", "polar-parametric")
        if not plot_type in plot_types :
            self.fatal("plot_type must be one of: %s" % \
                str(plot_types))
        if   plot_type == "cartesian" :
            self.__swept_col = "xcol"
            self.__show_cols = ("xcol", "ycol")
        elif plot_type == "cartesian-parametric" :
            self.__swept_col = "tcol"
            self.__show_cols = ("xcol", "ycol", "tcol")
        elif plot_type == "polar" :
            self.__swept_col = "acol"
            self.__show_cols = ("xcol", "ycol", "rcol", "acol")
        elif plot_type == "polar-parametric" :
            self.__swept_col = "tcol"
            self.__show_cols = ("xcol", "ycol", "rcol", "acol", "tcol")
        if "plot_type_var" in self.__Component :
            self.__Component["plot_type_var"].set(plot_type)
        for col in ("xcol", "ycol", "acol", "rcol", "tcol") :
            ekey = "%s_entry" % (col)
            lkey = "%s_label" % (col)
            if not ((ekey in self.__Component) and (lkey in self.__Component)) :
                continue
            entry = self.__Component[ekey]
            label = self.__Component[lkey]
            label_text = label["text"]
            label_text = re.sub(" \(swept\) ", "", label_text)
            scolor = "white"
            lcolor = label["background"]
            if col == self.__swept_col :
                label_text += " (swept) "
                scolor = "antiquewhite1"
            if col in self.__show_cols :
                entry["state"]      = NORMAL
                entry["background"] = scolor
                entry["foreground"] = "black"
                label["foreground"] = "black"
                label["text"]       = label_text
            else :
                entry["state"]      = DISABLED
                entry["background"] = lcolor
                entry["foreground"] = lcolor
                label["background"] = lcolor
                label["foreground"] = lcolor
                label["text"]       = label_text
    #===========================================================================
    # METHOD  : _config_sample_type_callback
    # PURPOSE : configure sample_type
    #===========================================================================
    def _config_sample_type_callback(self) :
        sample_type  = self["sample_type"]
        sample_types = ("linear", "logarithmic")
        if not sample_type in sample_types :
            self.fatal("sample must be one of: %s" % str(sample_types))
        if "sample_type_var" in self.__Component :
            self.__Component["sample_type_var"].set(sample_type)
    #===========================================================================
    # METHOD  : __entry_enter
    # PURPOSE : used by config callbacks for entries
    #===========================================================================
    def __entry_enter(self, var) :
        val = self[var]
        key = "%s_entry" % (var)
        if key in self.__Component :
            entry = self.__Component[key]
            entry.delete(0, END)
            entry.insert(0, str(val))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Plotterx GUI
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __gui
    # PURPOSE : build graphical user interface
    #==========================================================================
    def __gui(self) :
        #---------------------------------------------------------------------
        # top-level:
        #---------------------------------------------------------------------
        if self.__parent == None:
            if not Tkinter._default_root :
                root = Tk()
                root.wm_state("withdrawn")
            self.__toplevel = Toplevel()
            self.__toplevel.wm_state("withdrawn")
            Frame.__init__(self, self.__toplevel, class_ = "Plotterx")
        else:
            self.__toplevel = None
            Frame.__init__(self, self.__parent,   class_ = "Plotterx")
        self.pack(side=TOP, fill=BOTH, expand=True)
        #---------------------------------------------------------------------
        # option database:
        #---------------------------------------------------------------------
        if sys.platform == "darwin" :
            self.option_add("*Plotterx*Menubutton.width", 10)
            self.option_add("*Plotterx*Menubutton.height", 1)
            self.option_add("*Plotterx*Label.width", 10)
            self.option_add("*Plotterx*Label.anchor", E)
            self.option_add("*Plotterx*Label.relief", SUNKEN)
            self.option_add("*Plotterx*Label.bd", 2)
            self.option_add("*Plotterx*Entry.width", 15)
            self.option_add("*Plotterx*Checkbutton.width", 12)
            self.option_add("*Plotterx*Checkbutton.anchor", W)
            self.option_add("*Plotterx*Checkbutton.bd", 2)
            self.option_add("*Plotterx*Checkbutton.relief", RAISED)
            self.option_add("*Plotterx*Checkbutton.highlightThickness", 0)
            self.option_add("*Plotterx*Radiobutton.anchor", W)
            self.option_add("*Plotterx*Radiobutton.highlightThickness", 0)
            self.option_add("*Plotterx*Button.highlightThickness", 0)
            self.option_add("*Plotterx*Button.width", 10)
            self.option_add("*Plotterx*Button.height", 1)
            self.option_add("*Plotterx*Entry.font", "Courier 20 normal")
            self.option_add("*Plotterx*Text.width", 20)
            self.option_add("*Plotterx*Text.height", 8)
            self.option_add("*Plotterx*Text.font", "Courier 20 normal")
        else :
            self.option_add("*Plotterx*Menubutton.width", 10)
            self.option_add("*Plotterx*Menubutton.height", 1)
            self.option_add("*Plotterx*Label.width", 10)
            self.option_add("*Plotterx*Label.anchor", E)
            self.option_add("*Plotterx*Label.relief", SUNKEN)
            self.option_add("*Plotterx*Label.bd", 2)
            self.option_add("*Plotterx*Entry.width", 20)
            self.option_add("*Plotterx*Checkbutton.width", 12)
            self.option_add("*Plotterx*Checkbutton.anchor", W)
            self.option_add("*Plotterx*Checkbutton.bd", 2)
            self.option_add("*Plotterx*Checkbutton.relief", RAISED)
            self.option_add("*Plotterx*Checkbutton.highlightThickness", 0)
            self.option_add("*Plotterx*Radiobutton.anchor", W)
            self.option_add("*Plotterx*Radiobutton.highlightThickness", 0)
            self.option_add("*Plotterx*Button.highlightThickness", 0)
            self.option_add("*Plotterx*Button.width", 10)
            self.option_add("*Plotterx*Button.height", 1)
            self.option_add("*Plotterx*Entry.font", "Courier 12 normal")
            self.option_add("*Plotterx*Text.width", 20)
            self.option_add("*Plotterx*Text.height", 8)
            self.option_add("*Plotterx*Text.font", "Courier 12 normal")
        #---------------------------------------------------------------------
        # main layout
        #---------------------------------------------------------------------
        mbar = Frame(self, relief=SUNKEN, bd=2)
        mbar.pack(side=TOP, expand=False, fill=X,    padx=2, pady=2)
        fcnt = Frame(self, relief=SUNKEN, bd=2)
        fcnt.pack(side=TOP, expand=False, fill=X,    padx=2, pady=2)
        fplt = Frame(self, relief=SUNKEN, bd=2, background="blue")
        fplt.pack(side=TOP, expand=True, fill=BOTH, padx=2, pady=2)

        cont = Frame(fcnt, relief=FLAT)
        cont.pack(side=LEFT, expand=True, fill=BOTH, padx=2, pady=2)
        ftxt = Frame(fcnt, relief=FLAT, bd=2)
        ftxt.pack(side=RIGHT, expand=True, fill=BOTH)
        tobj = Text(ftxt, relief=SUNKEN, bd=2, height=5)
        tobj.pack(side=RIGHT, expand=True, fill=BOTH)

        if not self.__equations is None:
            tobj.delete(1.0, END)
            tobj.insert(1.0, self.__equations)

        self.__Component["plot_frame"] = fplt
        self.__Component["text"] = tobj
        #---------------------------------------------------------------------
        # menu-bar
        #---------------------------------------------------------------------
        file_mb = Menubutton(mbar, text="File")
        file_mb.pack(side=LEFT, padx=5, pady=5)
        ptyp_mb = Menubutton(mbar, text="Plot Type")
        ptyp_mb.pack(side=LEFT, padx=5, pady=5)
        samp_mb = Menubutton(mbar, text="Sample")
        samp_mb.pack(side=LEFT, padx=5, pady=5)
        curv_mb = Menubutton(mbar, text="Curves")
        curv_mb.pack(side=LEFT, padx=5, pady=5)

        file_menu=Menu(file_mb)
        ptyp_menu=Menu(ptyp_mb)
        samp_menu=Menu(samp_mb)
        curv_menu=Menu(curv_mb)
        file_mb["menu"] = file_menu
        ptyp_mb["menu"] = ptyp_menu
        samp_mb["menu"] = samp_menu
        curv_mb["menu"] = curv_menu

        samp_bt = Button(mbar, text="Sample/Plot")
        samp_bt.pack(side=LEFT, padx=5, pady=5)
        samp_bt["background"] = "red"
        samp_bt["foreground"] = "white"
        samp_bt["command"] = self.__sample_plot

        mblist = [file_mb, ptyp_mb, samp_mb, curv_mb, samp_bt]
        #tk_menuBar(mblist)
        #---------------------------------------------------------------------
        # file menu
        #---------------------------------------------------------------------
        file_menu.add_command(
            label="Write Plotterx file",
            command=self.__write_plotter)
        file_menu.add_command(
            label="Write Data",
            command=self.__write_ssv)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self.__exit_cmd)
        #---------------------------------------------------------------------
        # plot_type menu
        #---------------------------------------------------------------------
        var = StringVar()
        self.__Component["plot_type_var"] = var
        def cmd(self=self) :
            self["plot_type"] = "cartesian"
        ptyp_menu.add_radiobutton(
            label="Cartesian", command=cmd,
            variable=var, value="cartesian")
        def cmd(self=self) :
            self["plot_type"] = "cartesian-parametric"
        ptyp_menu.add_radiobutton(
            label="Cartesian-Parametric", command=cmd,
            variable=var, value="cartesian-parametric")
        def cmd(self=self) :
            self["plot_type"] = "polar"
        ptyp_menu.add_radiobutton(
            label="Polar", command=cmd,
            variable=var, value="polar")
        def cmd(self=self) :
            self["plot_type"] = "polar-parametric"
        ptyp_menu.add_radiobutton(
            label="Polar-Parametric", command=cmd,
            variable=var, value="polar-parametric")
        #---------------------------------------------------------------------
        # sample menu
        #---------------------------------------------------------------------
        var = StringVar()
        self.__Component["sample_type_var"] = var
        def cmd(self=self) :
            self["sample_type"] = "linear"
        samp_menu.add_radiobutton(
            label="Linear Sampling", command=cmd,
            variable=var, value="linear")
        def cmd(self=self) :
            self["sample_type"] = "logarithmic"
        samp_menu.add_radiobutton(
            label="Logarithmic Sampling", command=cmd,
            variable=var, value="logarithmic")
        #---------------------------------------------------------------------
        # curves menu
        #---------------------------------------------------------------------
        for curve in Plotterx._Curves :
            def cmd(curve=curve) :
                self.__plot_curve(curve)
            curv_menu.add_command(label=curve, command=cmd)
        #---------------------------------------------------------------------
        # plot entries
        #---------------------------------------------------------------------
        def entrybindcmd(event, self=self):
            self.__sample_plot(new=False)
        def textbindcmd(event, self=self):
            self.__sample_plot(new=False)

        entry_list = []
        for item in (
            ["xcol", "x column"],
            ["ycol", "y column"],
            ["acol", "angle column"],
            ["rcol", "radius column"],
            ["tcol", "parameter column"],
            ["npts", "number of samples"],
            ["min",  "minimum of sweep"],
            ["max",  "maximum of sweep"],
        ) :
            var, text = item
            val = self[var]
            f = Frame(cont, relief=FLAT)
            f.pack(side=TOP, expand=True, fill=X)
            l = Label(f, relief=FLAT, anchor=W, text=text, width=24)
            l.pack(side=LEFT, expand=True, fill=X)
            e = Entry(f, relief=SUNKEN, bd=2)
            e.pack(side=LEFT, expand=True, fill=X)
            self.__Component["%s_label" % (var)] = l
            self.__Component["%s_entry" % (var)] = e
            e.delete(0, END)
            e.insert(0, str(val))
            e.bind("<Control-Key-s>", entrybindcmd)
            e.bind("<Return>", entrybindcmd)
            entry_list.append(e)
        text = self.__Component["text"]
        text.bind("<Control-Key-s>", textbindcmd)
        entry_emacs_bindings(entry_list)
        #---------------------------------------------------------------------
        # update / mainloop
        #---------------------------------------------------------------------
        self._config_plot_type_callback()
        self._config_sample_type_callback()
        self.update()
        if not self.__equations is None:
            self.__sample_plot()
        if  self.__toplevel :
            self.__toplevel.geometry("+20+20")
            self.__toplevel.wm_state("normal")
        self.wait_window()
        if  self.__toplevel :
            self.__toplevel.destroy()
        else :
            self.destroy()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Plotterx GUI construction methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Plotterx GUI file menu callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #--------------------------------------------------------------------------
    # METHOD  : __exit_cmd
    # PURPOSE : exit file menu callback
    #--------------------------------------------------------------------------
    def __exit_cmd(self) :
        self.quit()
        if self.__toplevel :
             self.__toplevel.destroy()
        else :
             self.destroy()
        exit()
    #--------------------------------------------------------------------------
    # METHOD  : __write_ssv
    # PURPOSE : write data file
    #--------------------------------------------------------------------------
    def __write_ssv(self, file=None) :
        if not file :
            initialfile = "%s.ssv" % (self.__plotter_root)
            file = tkFileDialog.asksaveasfilename(
                parent = self,
                title = "data file name to save?",
                initialfile=initialfile,
                initialdir = os.getcwd(),
                defaultextension = ".col",
                filetypes = (
                    ("space-separated data format files", "*.col"),
                    ("space-separated data format files", "*.ssv"),
                    ("all files", "*")
                )
            )
        if not file:
            return
        self.__plotter_root = os.path.splitext(os.path.basename(file))[0]
        # file/format dialog?
        self.__data_obj.write_ssv(file)
    #--------------------------------------------------------------------------
    # METHOD  : __write_plotter
    # PURPOSE : write executable plotter file
    #--------------------------------------------------------------------------
    def __write_plotter(self, file=None) :
        if not file :
            initialfile = "%s.plt" % (self.__plotter_root)
            file = tkFileDialog.asksaveasfilename(
                parent = self,
                title = "plotter file name to save?",
                initialfile=initialfile,
                initialdir = os.getcwd(),
                defaultextension = ".plt",
                filetypes = (
                    ("plotter/python files", "*.plt"),
                    ("plotter/python files", "*.py"),
                    ("all files", "*")
                )
            )
        if not file:
            return
        #-------------------------------
        # Plotterx parameters
        #-------------------------------
        self.__plotter_root = os.path.splitext(os.path.basename(file))[0]
        plot_type   = self.__Component["plot_type_var"].get()
        sample_type = self.__Component["sample_type_var"].get()
        npts = self.__Component["npts_entry"].get()
        xmin = self.__Component["min_entry"].get()
        xmax = self.__Component["max_entry"].get()
        xcol = self.__Component["xcol_entry"].get()
        ycol = self.__Component["ycol_entry"].get()
        acol = self.__Component["acol_entry"].get()
        rcol = self.__Component["rcol_entry"].get()
        tcol = self.__Component["tcol_entry"].get()
        tobj = self.__Component["text"]
        eqns = tobj.get(1.0, END)
        eqns = str(eqns)
        #----------------------------------------------------------------------
        # write executable plotter file
        #----------------------------------------------------------------------
        print "writing plot to %s" % (file)
        timestamp = time.time()
        datetime  = time.asctime(time.localtime(timestamp))
        f = open(file, "w")
        f.write("#! /usr/bin/env python\n")
        f.write("#" * 72 + "\n")
        f.write("# NAME : %s\n" % (file))
        f.write("# CREATED BY : Plotterx\n")
        f.write("# DATE : %s\n" % (datetime))
        f.write("#" * 72 + "\n")
        f.write("import user\n")
        f.write("import decida\n")
        f.write("from decida.Plotterx import Plotterx\n")
        f.write("Plotterx(\n")
        f.write("    plot_type=\"%s\",\n"   % (plot_type))
        f.write("    sample_type=\"%s\",\n" % (sample_type))
        f.write("    npts=%s,\n"            % (npts))
        f.write("    min=%s,\n"             % (xmin))
        f.write("    max=%s,\n"             % (xmax))
        f.write("    xcol=\"%s\",\n"        % (xcol))
        f.write("    ycol=\"%s\",\n"        % (ycol))
        if len(acol) > 0 :
            f.write("    acol=\"%s\",\n" % (acol))
        if len(rcol) > 0 :
            f.write("    rcol=\"%s\",\n" % (rcol))
        if len(tcol) > 0 :
            f.write("    tcol=\"%s\",\n" % (tcol))
        f.write("    equations=\"\"\"\n")
        for line in string.split(eqns, "\n") :
            line=string.strip(line)
            if len(line) > 0:
                f.write("        %s\n" % (line))
        f.write("    \"\"\"\n")
        f.write(")\n")
        f.close()
        os.chmod(file, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Plotterx GUI plot callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #--------------------------------------------------------------------------
    # METHOD  : __sample
    # PURPOSE : sample swept variable
    # NOTES :
    #     * tobj comes out as unicode
    #--------------------------------------------------------------------------
    def __sample(self) :
        plot_type   = self.__Component["plot_type_var"].get()
        sample_type = self.__Component["sample_type_var"].get()
        key    = "%s_entry" % (self.__swept_col)
        sweep  = self.__Component[key].get()
        npts   = int(self.__Component["npts_entry"].get())
        xmin   = float(self.__Component["min_entry"].get())
        xmax   = float(self.__Component["max_entry"].get())
        mode   = sample_type[0:3]
        values = decida.range_sample(xmin, xmax, num=npts, mode=mode)
        #-------------------------------
        # get and preprocess equations
        #-------------------------------
        tobj   = self.__Component["text"]
        eqns   = tobj.get(1.0, END)
        eqns   = str(eqns)
        #-------------------------------
        # split on newline and semicolon
        #-------------------------------
        eqnlines = string.split(eqns, "\n")
        newlines = []
        for eqnline in eqnlines :
            sublines = string.split(eqnline, ";")
            for subline in sublines :
                newlines.append(subline)
        eqnlines = newlines
        #-----------------------------------
        # eliminate comments and blank lines
        #-----------------------------------
        eqnlist = []
        for eqnline in eqnlines :
            eqnline = re.sub("#.*$", "", eqnline)
            eqnline = string.strip(eqnline)
            if len(eqnline) > 0 : 
                eqnlist.append(eqnline)
        #--------------------------------------
        # start with new data object, sample x
        #--------------------------------------
        if  not self.__data_obj is None:
            del self.__data_obj
        self.__data_obj = Data()
        self.__data_obj.read_inline(sweep, values)
        #--------------------------------------
        # evaluate equations
        #--------------------------------------
        for eqn in eqnlist :
            self.__data_obj.set(eqn)
        #--------------------------------------
        # polar to cartesian
        #--------------------------------------
        angle = "radians"
        if angle == "degrees" :
            cvt = math.pi / 180.0
        else :
            cvt = 1.0
        if plot_type in ["polar", "polar-parametric"] :
            xcol = self.__Component["xcol_entry"].get()
            ycol = self.__Component["ycol_entry"].get()
            acol = self.__Component["acol_entry"].get()
            rcol = self.__Component["rcol_entry"].get()
            self.__data_obj.set("%s=%s*cos(%s*%s)" % (xcol, rcol, acol, cvt))
            self.__data_obj.set("%s=%s*sin(%s*%s)" % (ycol, rcol, acol, cvt))
    #--------------------------------------------------------------------------
    # METHOD  : __sample_plot
    # PURPOSE : generate XY plot
    # NOTES :
    #    ignore new for now
    #    must defer packing until dataview requests geometry
    #--------------------------------------------------------------------------
    def __sample_plot(self, new=True) :
        self.__sample()
        xcol = self.__Component["xcol_entry"].get()
        ycol = self.__Component["ycol_entry"].get()
        if not xcol in self.__data_obj.names() :
            self.warning("data object does not have (x) column %s" % (xcol))
            return
        if not ycol in self.__data_obj.names() :
            self.warning("data object does not have (y) column %s" % (ycol))
            return

        if new or self.__dataview is None :
            if  not self.__dataview is None :
                # del should have destroyed it
                self.__dataview.destroy()
                del self.__dataview
            fplt = self.__Component["plot_frame"]
            fplt.pack_forget()
            # dataview command partially implemented
            if True :
                self.__dataview = DataViewx(fplt,
                    data=self.__data_obj,
                    command=[
                       ["%s %s" % (xcol, ycol),
                       "traces=[\"both\"], legend=False"],
                    ],
                    plot_height=self["plot_height"]
                )
            else :
                self.__dataview = XYplotx(fplt, 
                    command=[self.__data_obj, "%s %s" %(xcol, ycol)],
                    traces=["both"], legend=False
                )
            fplt.pack(side=TOP, expand=True, fill=BOTH, padx=2, pady=2)
            self.update()
        else :
            if True :
                xyplot = self.__dataview.current_plot()
            else :
                xyplot = self.__dataview
            curve = "data_%d_:_%s_vs_%s" % (1, ycol, xcol)
            xyplot.delete_curve(curve)
            xyplot.add_curve(self.__data_obj, xcol, ycol,
                start=True, autoscale_x=True, autoscale_y=True, strict=False)
    #--------------------------------------------------------------------------
    # METHOD  : __plot_curve
    # PURPOSE : plot a pre-defined curve
    #--------------------------------------------------------------------------
    def __plot_curve(self, curve) :
        plot_type, xmin, xmax, equations = Plotterx._Curves[curve]
        self["sample_type"] = "linear"
        self["plot_type"] = plot_type
        self["xcol"] = "x"
        self["ycol"] = "y"
        self["acol"] = "a"
        self["rcol"] = "r"
        self["tcol"] = "t"
        self["min"]  = xmin
        self["max"]  = xmax
        #-------------------------------------------
        # left-justify the equations for text-window
        #-------------------------------------------
        lines = string.split(equations, "\n")
        newlines = []
        for line in lines :
            line = string.strip(line)
            if len(line) > 0:
                newlines.append(line)
        equations = string.join(newlines, "\n")
        #-------------------------------------------
        # enter equations and sample/plot
        #-------------------------------------------
        self.__equations = equations
        tobj = self.__Component["text"]
        tobj.delete(1.0, END)
        tobj.insert(1.0, self.__equations)
        self.__sample_plot()
