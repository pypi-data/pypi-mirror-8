################################################################################
# CLASS    : XYplotx
# PURPOSE  : Plot y vector(s) versus x
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:27:05 2013
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
from decida.PlotBase import PlotBase
from decida.Data import Data
from Tkinter import *

class XYplotx(PlotBase) :
    """ plot y vector(s) versus x vector.

    **synopsis**:

    XYplotx plots one or more y_vs_x curves.  The curves are specified by
    the *command* argument to the XYplotx instance call. 
    The command specifies a list of pairs of Data object instances, and
    string of data-column names to plot.  Curves attributes: color, symbol
    symbol-size and line-width can be changed after the plot has been created.
    Log/Lin axes check-boxes toggle the axes between logarithmic and linear.
    The plots can be annotated with lines, arrows, rectangles, and/or text.

    **constructor arguments**:

        .. option:: parent (Tkinter handle) (default=None)

              handle of frame or other widget to pack plot in.
              if this is not specified, top-level is created.

        .. option:: \*\*kwargs (dict)

              keyword=value specifications:
              options or configuration-options

    **options**:

        .. option:: command 

              list of pairs of data-object, string of x, y1, ?y2, ...?
              columns

              example: [d1, "x y1 y2", d2, "x y1 y2"]:
                 x, y1 and x, y2 curves will be plotted for each
                 data object d1 and d2.  Each curve will also be plotted
                 with color, symbol, symbol-size, line-width, and
                 trace-direction selected from the successive item in
                 the respective list of specified configured options:
                 colors, symbols, ssizes, wlines, traces.  Selection
                 wraps around if the respective list is shorter than
                 the number of curves.

    **configuration options**:

        .. option::  verbose (bool, default=False)

              enable/disable verbose mode

        .. option::  title (str, default="")

              main title

        .. option::  xtitle (str, default="")

              x-axis title

        .. option::  ytitle (str, default="")

              y-axis title

        .. option::  plot_height (str, default="10i" for MacOS, else "6i")

              Height of plot window (Tk inch  or pixelspecification)

        .. option::  plot_width  (str, default="10i" for MacOS, else "6i")

              Width of plot window (Tk inch or pixel specification)

        .. option::  plot_background (str, default="GhostWhite")

              Background color of plot window

        .. option::  legend_background (str, default="AntiqueWhite2")

              Background color of legend

        .. option::  colors (list of str, default =
                "blue", "red", "green", "orange", "cyan",
                "brown", "black", "blue violet", "cadet blue",
                "dark cyan", "dark goldenrod", "dark green",
                "dark magenta", "dark olive green", "dark orange",
                "dark red", "dark slate blue", "dark slate gray",
                "dodger blue", "forest green", "steel blue", "sienna"
              )

              list of colors for curves.
              Used to populate color menu, and to specify curve colors
              in scripted "command" option.

        .. option::  symbols (list of str, default = 
                "none", "dot", "square", "diamond",
                "triangle", "itriangle",
                "dash", "pipe", "plus", "cross",
                "spade", "heart", "diam", "club", "shamrock",
                "fleurdelis", "circle", "star"
              ) 

              list of symbols for curves.
              Used to populate symbol menu, and to specify curve symbols
              in scripted "command" option.

        .. option::  ssizes (list of floats, default = [0.01])

              list of symbol sizes for curves.
              Used to specify curve symbol sizes
              in scripted "command" option.

        .. option::  wlines (list of ints, default = [1])

              list of line widths for curves.
              Used to specify curve line widths
              in scripted "command" option.

        .. option::  traces (list, default = ["increasing"])

              list of traces for curves.  each trace can be one of:
              "increasing", "decreasing", or "both".
              Used to specify curve trace directions
              in scripted "command" option.

        .. option::  xaxis (str, default="lin")

              linear or logarithmic axis: "lin" or "log"

        .. option::  yaxis (str, default="lin")

              linear or logarithmic axis: "lin" or "log"

        .. option::  xmin  (float, default=0.0)

              xaxis minimum

        .. option::  xmax  (float, default=0.0)

              xaxis maximum

        .. option::  ymin  (float, default=0.0)

              yaxis minimum

        .. option::  ymax  (float, default=0.0)

              yaxis maximum

        .. option::  grid  (bool, default=True)

              if true, show grid on plot

        .. option::  legend  (bool, default=True)

              if true, show legend on plot

        .. option::  postscript  (bool, default=False)

              if true, generate a PostScript file.

        .. option::  postscript_file (str, default="plot.ps")

              name of PostScript file to plot to

        .. option::  wait (bool, default=False)

              wait in main-loop until window is destroyed.

        .. option::  destroy (bool, default=False)

              destroy main window after it has been displayed.
              useful for displaying, generating PostScript, then
              destroying window.

    **example** (from test_XYplotx_6): ::

        from decida.Data import Data
        from decida.XYplotx import XYplotx
        
        d = Data()
        d.read("LTspice_ac_ascii.raw")
        xyplot=XYplotx(None, command=[d, "frequency DB(V(vout1)) PH(V(vout1)) DB(V(vout2)) PH(V(vout2)) DB(V(vout3)) PH(V(vout3))"], title="AC analysis", xaxis="log", ymin=-60.0, ymax=0.0)

    **public methods**:

        * public methods from *PlotBase* (2-dimensinal plot base class)

        * public methods from *ItclObjectx*

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # XYplotx main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, **kwargs) :
        PlotBase.__init__(self, parent=parent)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        # keyword arguments are *not* all configuration options
        #----------------------------------------------------------------------
        for key, value in kwargs.items() :
            if key == "command" :
                command = value
            else :
                self[key] = value
        #----------------------------------------------------------------------
        # parse command before building gui:
        #----------------------------------------------------------------------
        idata  = 0
        datobj = None
        for item in command :
            if isinstance(item, Data) :
                idata += 1
                datobj = item
                dname = "data_%d" % (idata)
            elif type(item) == str :
                cols = string.split(item)
                xcol = cols.pop(0)
                if not self.was_configured("xtitle") :
                    self["xtitle"] = xcol
                if not self.was_configured("ytitle") :
                    self["ytitle"] = string.join(cols)
                for ycol in cols:
                    self.add_curve(datobj, xcol, ycol, dname=dname)
        #----------------------------------------------------------------------
        # build gui:
        #----------------------------------------------------------------------
        self._gui()
        self._mainloop()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # XYplotx GUI
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _gui
    # PURPOSE : build graphical user interface
    #==========================================================================
    def _gui(self) :
        PlotBase._gui(self)
