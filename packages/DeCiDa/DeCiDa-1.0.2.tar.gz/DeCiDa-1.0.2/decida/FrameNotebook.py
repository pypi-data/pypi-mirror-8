################################################################################
# CLASS   : FrameNotebook
# PURPOSE : tab notebook for other windows
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:20:44 2013
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
import string
import re
import decida
from decida.ItclObjectx import ItclObjectx
import Tkinter
from Tkinter import *

class FrameNotebook(ItclObjectx, Frame) :
    """ tab-notebook widget.
       
    **synopsis**:

    FrameNotebook is a widget for packing other frames containing content
    in a tabbed-notebook.  Tabs and associated frames can be added 
    after the notebook has been created.

    FrameNotebook is used by DataViewx to organize the plots in a
    tabbed-notebook format.  It is also used to display TextWindow and
    DataViewx help information.

    **constructor arguments**:
        .. option::  parent (Tkinter handle)

            handle of frame or other widget to pack frame notebook in.
            if this is not specified, top-level is created.

        .. option::  header (bool) (optional, default=True)

            if true, add quit/status line

        .. option::  \*\*kwargs (dict)

            configuration-options

    **configuration options**:

        .. option::  verbose (bool) (default=False)

            enable/disable verbose mode

        .. option::  tab_location (string) (default="top")

            notebook tab location = top or right

        .. option::  wait (bool) (default=False)

            wait in main-loop until window is destroyed

        .. option::  wait_to_display (bool) (default=False)

            display only after wait (for help windows)

    **example**: (from test_FrameNotebook_1) ::

        from decida.FrameNotebook import FrameNotebook
        from decida.TextWindow import TextWindow
        from decida.XYplotx import XYplotx
        from decida.Data import Data
        
        fn = FrameNotebook(tab_location="top", destroy=False)
        tw = TextWindow(fn.new_page("text"))
        d = Data()
        d.read("LTspice_ac_ascii.raw")
        XYplotx(fn.new_page("plot"), command=[d, "frequency DB(V(vout1)) PH(V(vout1))"], title="AC analysis", xaxis="log", ymin=-60.0, ymax=0.0, wait=False)

        fn.status("waiting to add new page")
        fn.wait("continue")
        fn.status("")

    **public methods**:

        * public methods from *ItclObjectx*

    """
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__parent      = parent
        self.__Component   = {}
        self.__tabids      = []
        self.__TabText     = {}
        self.__TabID_frame = {}
        self.__PageFrame   = {}
        self.__current_tab = None
        self.__pending     = None
        self.__header      = True
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        self._add_options({
            "verbose"        : [False, None],
            "tab_location"   : ["top", self.__refresh],
            "wait"           : [False, None],
            "wait_to_display": [False, None],
            "destroy"        : [True,  None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are *NOT* all configuration options
        #----------------------------------------------------------------------
        for key, value in kwargs.items() :
            if key == "header" :
                self.__header = value
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
    # FrameNotebook GUI
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
            Frame.__init__(self, self.__toplevel, class_ = "FrameNotebook")
            self.__toplevel.protocol('WM_DELETE_WINDOW', self.__quit_cmd)
            if not self.was_configured("wait") :
                self["wait"] = False
            #-----------------------------------------------------------------
            # following for textwindow/dataview help:
            #-----------------------------------------------------------------
            if self["wait_to_display"] :
                self.__toplevel.withdraw()
        else:
            self.__toplevel = None
            Frame.__init__(self, self.__parent,   class_ = "FrameNotebook")
            if not self.was_configured("wait") :
                self["wait"] = False
        self.pack(side=TOP, fill=BOTH, expand=True)
        #---------------------------------------------------------------------
        # option database:
        #---------------------------------------------------------------------
        if sys.platform == "darwin" :
            self.option_add("*FrameNotebook.tabMargin",      6)
            #elf.option_add("*FrameNotebook.tabNormalColor", "#7777cc")
            #elf.option_add("*FrameNotebook.tabActiveColor", "#cc7777")
            self.option_add("*FrameNotebook.tabNormalColor", "#4188ff")
            self.option_add("*FrameNotebook.tabActiveColor", "#ffff00")
            self.option_add("*FrameNotebook.tabFont",        "Helvetica 18")
        else :
            self.option_add("*FrameNotebook.tabMargin",      6)
            #elf.option_add("*FrameNotebook.tabNormalColor", "#7777cc")
            #elf.option_add("*FrameNotebook.tabActiveColor", "#cc7777")
            self.option_add("*FrameNotebook.tabNormalColor", "#4188ff")
            self.option_add("*FrameNotebook.tabActiveColor", "#ffff00")
            self.option_add("*FrameNotebook.tabFont",        "Helvetica 12 bold")
        #---------------------------------------------------------------------
        # main layout
        #---------------------------------------------------------------------
        self.__Component["wbut"] = None
        if self.__header :
            mbar = Frame(self, relief=RAISED, bd=3)
            mbar.pack(side=TOP, fill=X)
            stat = Label(mbar, relief=SUNKEN, bd=1, height=1, anchor=W)
            stat.pack(side=RIGHT, expand=True, fill=X)
        else :
            mbar = None
            stat = None
        hubb = Frame(self, relief=RAISED, bd=3, background="orange")
        hubb.pack(side=TOP, expand=True, fill=BOTH)
        self.__Component["mbar"] = mbar
        self.__Component["stat"] = stat
        self.__Component["hubb"] = hubb
        #---------------------------------------------------------------------
        # mbar
        #---------------------------------------------------------------------
        if self.__header :
            qbut = Button(mbar, text="Quit", command=self.__quit_cmd)
            qbut.pack(side=LEFT)
        #---------------------------------------------------------------------
        # tabs and book
        #---------------------------------------------------------------------
        tabs = Canvas(hubb, bd=4, relief=RIDGE)
        tabs["highlightthickness"] = 0
        book = Frame(hubb, bd=2, relief=SUNKEN)
        book.pack_propagate(0)
        loc = self["tab_location"]
        if   loc == "top" :
            tabs.pack(side=TOP,    fill=X)
            book.pack(side=BOTTOM, fill=BOTH, expand=True)
        elif loc == "right" :
            tabs.pack(side=RIGHT,  fill=Y)
            book.pack(side=LEFT,   fill=BOTH, expand=True)
        book["background"] = "steel blue"
        self.__Component["tabs"] = tabs
        self.__Component["book"] = book
        #---------------------------------------------------------------------
        # update / mainloop
        #---------------------------------------------------------------------
        self.update()
        if self["wait"] :
            self.wait()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # FrameNotebook user commands
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : wait
    # PURPOSE : wait in main-loop until main window is destroyed
    #==========================================================================
    def wait(self, text=None) :
        """ wait in main-loop until main window is destroyed.

        **arguments**:

            .. option:: text (string, default=None)

                If text is specified, a button is displayed with the text
                in the button.  Clicking the button releases the application
                from the main event-loop.

        **results**:

            * If no text is displayed, then the application waits for the
              TextWindow instance to somehow be destroyed.  If text was
              specified, then the application waits until the button is
              clicked.

        """
        if self.__toplevel :
            self.__toplevel.deiconify()
        if text and self.__header :
            mbar = self.__Component["mbar"]
            wbut = Button(mbar, text=text, background="gold")
            wbut.pack(side=LEFT)
            wbut["command"] = wbut.destroy
            self.__Component["wbut"] = wbut
            wbut.wait_window()
            if not self.winfo_exists() :
                exit()
        else :
            self.wait_window()
    #==========================================================================
    # METHOD : status
    # PURPOSE : display status message
    #==========================================================================
    def status(self, message) :
        """ display status message.

        **arguments**:

            .. option:: message (string)

                status message to display

        **results**:

           * message is displayed in the status bar of the FrameNotebook

       
        """
        if self.__header :
            stat = self.__Component["stat"]
            stat["text"] = message
            self.update()
    #==========================================================================
    # METHOD : tabs
    # PURPOSE : return list of tabids
    #==========================================================================
    def tabs(self) :
        """ return list of tabids.

        **results**: 

            * list of existing tabids is returned.  A tabid can be used
              to refer to a particular tab/Frame pair.

        """
        return self.__tabids
    #==========================================================================
    # METHOD : new_page
    # PURPOSE : return a new page frame, make new notebook tab
    # NOTES :
    #   * if lift=True, raise tab
    #==========================================================================
    def new_page(self, name, lift=True) :
        """ return a new page frame, make new notebook tab.

        **arguments**:

            .. option:: lift (bool, default=True)

                If lift is True, raise tab/frame after it is created.

        **results**:

            * A new page (tab/frame pair) is created and the handle to the
              associated Tkinter Frame is returned.  This is used as a 
              parent to pack new content in.

        """
        book = self.__Component["book"]
        page_frame = Frame(book, bd=2, relief=SUNKEN)
        tabid  = self.__new_tabid(name)
        self.__tabids.append(tabid)
        self.__TabText[tabid]   = name
        self.__PageFrame[tabid] = page_frame
        self.__TabID_frame[page_frame] = tabid

        if len(self.__tabids) == 1  or  lift :
            def cmd(self=self, tabid=tabid) :
                self.__display_tab(tabid)
            self.after_idle(cmd)
        if not self.__pending :
            def cmd(self=self) :
                self.__refresh()
            self.__pending = self.after_idle(cmd)
        return page_frame
    #==========================================================================
    # METHOD  : lift_tab
    # PURPOSE : display tab/page in the notebook
    #==========================================================================
    def lift_tab(self, tabid):
        """ display tab/page in the notebook.

        **arguments**:

            .. option:: tabid (string)

                A unique tabid associated with a particular page.

        **results**:

            * The page associated with the tabid is raised (made visible).
        
        """
        if tabid in self.__tabids :
            self.__display_tab(tabid)
        else :
            self.fatal("tab %s doesn't exist\n  tabids: %s" % \
              (tabid, self.__tabids))
    #==========================================================================
    # METHOD : current_tab
    # PURPOSE : return current unique tabid
    #==========================================================================
    def current_tab(self) :
        """ return current unique tabid.

        **results**:

            * The current (visible) page tabid is returned.

        """
        return self.__current_tab
    #==========================================================================
    # METHOD : relabel_current_tab
    # PURPOSE : set current tab label
    #==========================================================================
    def relabel_current_tab(self, label) :
        """ set current tab label.

        **arguments**:

            .. option:: label

                text to re-label the current tab

        **results**:

            * The current tab is relabled with label.

        """
        tabid = self.__current_tab
        self.__TabText[tabid] = label
        if not self.__pending :
            def cmd(self=self) :
                self.__refresh()
            self.__pending = self.after_idle(cmd)
    #==========================================================================
    # METHOD : del_page
    # PURPOSE : delete current page
    #==========================================================================
    def del_page(self) :
        """ delete current page.

        **results**:

            * The current page (tab/frame pair) are removed from the 
              notebook.

        """
        book = self.__Component["book"]
        tabid      = self.__current_tab
        page_frame = self.__PageFrame[tabid]
        
        i = self.__tabids.index(tabid)
        self.__tabids.pop(i)
        page_frame.destroy()
        #----------------------------------------------------------------------
        # delicately display underlying tab/frame, refresh tabs afterward
        #----------------------------------------------------------------------
        if i >= len(self.__tabids) :
            i -= 1
        if i >= 0:
            tabid = self.__tabids[i]
            self.__display_tab(tabid)
        else :
            self.__current_tab = None
        self.__refresh()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # FrameNotebook GUI callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : __quit_cmd
    # PURPOSE : destroy window
    #==========================================================================
    def __quit_cmd(self) :
        self.quit()
        wbut = self.__Component["wbut"]
        if wbut :
             wbut.destroy()
        if self["destroy"] :
             self.__del__()
    #==========================================================================
    # METHOD  : __new_tabid
    # PURPOSE : return an unique notebook tab id
    # NOTES   : tabids seem to require an alpha to start
    #==========================================================================
    def __new_tabid(self, name) :
        tabidname  = re.sub(" ", "_", name)
        if not re.search("^[a-zA-Z_]", tabidname) :
            tabidname  = "tabid_%s" % (tabidname)
        tabid = tabidname
        i = 0
        while tabid in self.__tabids :
            tabid = "%s_%d" % (tabidname, i)
            i += 1
            if i > 10000 :
                self.fatal("can't get new tabid")
        return tabid      
    #==========================================================================
    # METHOD  : __display_tab
    # PURPOSE : display tab/page in the notebook
    #==========================================================================
    def __display_tab(self, tabid):
        if tabid in self.__tabids :
            page_frame = self.__PageFrame[tabid]
        else :
            self.fatal("tab %s doesn't exist" % (tabid))

        self.__fix_page_size()
        if not self.__current_tab is None :
            current_page_frame = self.__PageFrame[self.__current_tab]
            if current_page_frame != page_frame :
                current_page_frame.pack_forget()
                page_frame.pack(expand=True, fill=BOTH)
        else :
            page_frame.pack(expand=True, fill=BOTH)
        self.__current_tab = tabid

        normal = self.option_get("tabNormalColor", "Color")
        active = self.option_get("tabActiveColor", "Color")

        tabs = self.__Component["tabs"]
        tabs.itemconfigure("tab",          fill=normal)
        tabs.itemconfigure("tab-" + tabid, fill=active)
        tabs.lift(tabid)
    #==========================================================================
    # METHOD  : __fix_page_size
    # PURPOSE : fix the page size to the maximum in the notebook
    #==========================================================================
    def __fix_page_size(self):
        self.update_idletasks()
        maxw, maxh = 0, 0
        for tabid in self.__tabids :
            page_frame = self.__PageFrame[tabid]
            w = page_frame.winfo_reqwidth()
            h = page_frame.winfo_reqheight()
            maxw=max(maxw, w)
            maxh=max(maxh, h)
        book = self.__Component["book"]
        bd = book.cget("borderwidth")
        maxw += 2*bd
        maxh += 2*bd
        book.configure(width=maxw, height=maxh)
    #==========================================================================
    # METHOD  : __refresh
    # PURPOSE : refresh the notebook after a major change
    #==========================================================================
    def __refresh(self):
        if not "tabs" in self.__Component :
            return
        loc   = self["tab_location"]
        mg    = string.atoi(self.option_get("tabMargin", "Size"))
        color = self.option_get("tabNormalColor", "Color")
        font  = self.option_get("tabFont", "Font")
        tabs  = self.__Component["tabs"]
        book  = self.__Component["book"]
        tabs.delete(ALL)
        tabs.pack_forget()
        book.pack_forget()
        dm = mg*0.5
        if   loc == "top" :
            tabs.pack(side=TOP,    fill=X)
            book.pack(side=BOTTOM, fill=BOTH, expand=True)
            x, y = dm, 0
        elif loc == "right" :
            tabs.pack(side=RIGHT,  fill=Y)
            book.pack(side=LEFT,   fill=BOTH, expand=True)
            x, y = 0, dm
        maxh=0
        maxw=0
        for tabid in self.__tabids :
            if   loc == "top" :
                xt, yt, anchor = x + mg + 2, -dm, SW
            elif loc == "right" :
                xt, yt, anchor = dm, y + mg + 2, NW

            text = self.__TabText[tabid]
            id = tabs.create_text(xt, yt, anchor=anchor, text=text, 
                font=font, tags=tabid)
            bbox = tabs.bbox(id)
            wd = bbox[2] - bbox[0]
            ht = bbox[3] - bbox[1]
            maxw = max(wd, maxw)
            maxh = max(ht, maxh)

            if   loc == "top" :
                dt = ht + mg
                ys = (
                    0, 0,
                    -0.1*dt,    -0.9*dt,    -1.0*dt,
                    -1.0*dt,    -0.9*dt,    -0.1*dt,
                    0, 0, 10, 10
                )
                xs = (
                    0, x,
                    x+dm,       x+dm,       x+mg,
                    x+mg+wd,    x+mg+dm+wd, x+mg+dm+wd,
                    x+mg+mg+wd, 2000, 2000, 0
                )
            elif loc == "right" :
                dt = wd + mg
                ys = (
                    0, y,
                    y+dm,       y+dm,       y+mg,
                    y+mg+ht,    y+mg+dm+ht, y+mg+dm+ht,
                    y+mg+mg+ht, 2000, 2000, 0
                )
                xs = (
                    0, 0,
                    0.1*dt,     0.9*dt,     1.0*dt,
                    1.0*dt,     0.9*dt,     0.1*dt,
                    0, 0, -10, -10
                )
            coords = zip(xs, ys)
            tags = ["tab", tabid, "tab-" + tabid]
               
            tabs.create_polygon(coords, tags=tags, outline=None, fill=color)
            tabs.lift(id)
            def cmd(event, self=self, tabid=tabid) :
                self.__display_tab(tabid)
            tabs.tag_bind(tabid, "<ButtonPress-1>", cmd)
            if   loc == "top" :
                x += wd + 1.2*mg
            elif loc == "right" :
                y += ht + 1.2*mg
        if   loc == "top" :
            height=maxh+2*mg
            tabs.move(ALL, 0, height)
            tabs["width"]  = x
            tabs["height"] = height + 4
        elif loc == "right" :
            width=maxw+2*mg
            tabs.move(ALL, 10, 0)
            tabs["height"] = y
            tabs["width"] = width + 4
        if not self.__current_tab is None :
            self.__display_tab(self.__current_tab)
        elif len(self.__tabids) > 0 :
            self.__display_tab(self.__tabids[0])
        self.__pending = None
