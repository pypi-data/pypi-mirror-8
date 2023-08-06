################################################################################
# CLASS    : SelectionDialog
# PURPOSE  : generic selection dialog
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:24:40 2013
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
from decida.DialogBase import DialogBase
from Tkinter import *
import string
class SelectionDialog(DialogBase):
    """ generic selection dialog.

        **synopsis**:

        *SelectionDialog* is a generic dialog for incorporating 
        a panel of check-boxes, radio-switch boxes, and entry boxes.

        *SelectionDialog* is used to create the *XYplotx* settings and 
        annotation dialogs.

        **constructor arguments**:

            .. option:: parent (Tkinter handle) (optional, default=None)

                handle of frame or other widget to pack plot in.
                if this is not specified, top-level is created.

            .. option:: guispecs (list) (optional, default=None)

                gui-specs

            .. option:: title (string) (optional, default="")

                title to be placed on dialog window

        **gui-specs**:

            .. option:: list of category specs:

                * check: ["check", <category title>, <check button specs>]

                * radio: ["radio", <category title>, <key>, <default value>,
                                                     <radio button specs>]

                * entry: ["entry", <category title>, <entry  specs>]

            .. option:: check button specs:

                * [<key>, <button label>, <default value>]

            .. option:: radio button specs:

                * [       <button label>, <button value> ]

            .. option:: entry specs:

                * [<key>, <entry  label>, <default value>]

        **results**:

            * key array returned

            * if accept button is pressed, changed results are returned in key array

            * if cancel button is pressed, default results are returned in key array

            * key array ["ACCEPT"] is True if accept was pressed else False

            * key array ["KEYS"] is list of keys in order of appearance in guispecs

        **example**::

            guispecs = [
               ["check", "Checkbox Selections", [
                   ["CHECK_KEY0", "select check 0", True],
                   ["CHECK_KEY1", "select check 1", True],
                   ["CHECK_KEY2", "select check 2", False],
               ]],
               ["radio", "Radiobox Selections", "RADIO_KEY", "RADIO_VAL0", [
                   ["select radio 0", "RADIO_VAL0"],
                   ["select radio 1", "RADIO_VAL1"],
                   ["select radio 2", "RADIO_VAL2"],
               ]],
               ["entry", "Entry Selections", [
                   ["ENTRY_KEY0", "entry 0", 1.2],
                   ["ENTRY_KEY1", "entry 1", 2.2],
                   ["ENTRY_KEY2", "entry 2", 2.3],
               ]],
            ]
            sd = SelectionDialog(title="Selection Dialog", guispecs=guispecs)
            V = sd.go()

    **public methods**:

    """
    #=========================================================================
    # METHOD : __init__
    # PURPOSE : constructor
    #=========================================================================
    def __init__(self, parent=None, guispecs=None, title=""):
        self.__guispecs = guispecs
        DialogBase.__init__(self, parent=parent, title=title, bitmap="question")
        self._gui()
    #=========================================================================
    # METHOD: _gui_middle
    #=========================================================================
    def _gui_middle(self):
        top      = self._Component["top"]
        bf       = self._Component["but_frame"]
        f_table  = self._Component["table"]
        guispecs = self.__guispecs
        #---------------------------------------------------------------------
        # middle entries
        #---------------------------------------------------------------------
        self._all_keys   = []
        self._check_keys = []
        self._radio_keys = []
        self._entry_keys = []
        self._check_val  = {}
        self._radio_val  = {}
        self._entry_val  = {}
        self._check_var  = {}
        self._radio_var  = {}
        self._entry_win  = {}
        start = True
        for spec in guispecs :
            type  = spec[0]
            blurb = spec[1]
            spec_f = Frame(f_table, relief=FLAT, bd=3)
            spec_f.pack(side=TOP, expand=True, fill=BOTH)
            if blurb and blurb != "" :
                spec_m = Label(spec_f, relief=GROOVE, bd=3, bg="cadet blue",
                    text=blurb, anchor=W)
                spec_m.pack(side=TOP, expand=True, fill=BOTH)
            if type == "radio" :
                radio_var = StringVar()
                radio_key = spec[2]
                radio_val = spec[3]
                items     = spec[4]
                self._all_keys.append(radio_key)
                self._radio_keys.append(radio_key)
                self._radio_var[radio_key] = radio_var
                self._radio_val[radio_key] = radio_val
                self._radio_var[radio_key].set(radio_val)
            else :
                items     = spec[2]
            for item in items :
                witem = Frame(spec_f, relief=FLAT, bd=3)
                witem.pack(side=TOP, fill=X, expand=True)
                if   type == "check" :
                    key   = item[0]
                    label = item[1]
                    value = item[2]
                    w = Checkbutton(witem, text=label, anchor=W, width=50)
                    w.pack(side=LEFT, fill=X, expand=True)
                    self._all_keys.append(key)
                    self._check_keys.append(key)
                    self._check_var[key] = IntVar()
                    self._check_var[key].set(value)
                    self._check_val[key] = value
                    w["variable"] = self._check_var[key]
                elif type == "radio" :
                    label = item[0]
                    value = item[1]
                    w = Radiobutton(witem, text=label, anchor=W, width=50)
                    w.pack(side=LEFT, fill=X, expand=True)
                    w["variable"] = radio_var
                    w["value"]    = value
                elif type == "entry" :
                    key   = item[0]
                    label = item[1]
                    value = item[2]
                    w = Label(witem, text=label)
                    w.pack(side=LEFT, fill=X, expand=True)
                    w = Entry(witem, bd=2, relief=SUNKEN, width=40)
                    w.pack(side=RIGHT, fill=BOTH, expand=False)
                    self._all_keys.append(key)
                    self._entry_keys.append(key)
                    self._entry_win[key] = w
                    self._entry_val[key] = value
                    self._entry_win[key].delete(0, END)
                    self._entry_win[key].insert(0, value)
                w.bind("<MouseWheel>", self._mouse_wheel)
                w.bind("<Button-4>",   self._mouse_wheel)
                w.bind("<Button-5>",   self._mouse_wheel)
                w.bind("<Prior>",      self._page_key)
                w.bind("<Next>",       self._page_key)
                w.bind("<Home>",       self._page_key)
                w.bind("<End>",        self._page_key)
        #---------------------------------------------------------------------
        # accept and cancel buttons
        #---------------------------------------------------------------------
        bf_cancel = Frame(bf, bd=2, relief=SUNKEN)
        bf_cancel.pack(side=LEFT, expand=True, padx=3, pady=2)
        bf_cancel_button = Button(bf_cancel, text="cancel",
            command=self.__cancel)
        bf_cancel_button.pack(anchor="c", expand=True, padx=3, pady=2)
        bf_accept = Frame(bf, bd=2, relief=SUNKEN)
        bf_accept.pack(side=LEFT, expand=True, padx=3, pady=2)
        bf_accept_button = Button(bf_accept, text="accept",
            command=self.__accept)
        bf_accept_button.pack(anchor="c", expand=True, padx=3, pady=2)
        self._Component["cancel"] = bf_cancel_button
        self._Component["accept"] = bf_accept_button
        #---------------------------------------------------------------------
        # key bindings
        #---------------------------------------------------------------------
        def cancel_cmd(event, self=self) :
            self.__cancel()
        def accept_cmd(event, self=self) :
            self.__accept()
        top.bind("<Control-Key-q>",      cancel_cmd)
        top.bind("<Control-Key-s>",      accept_cmd)
        top.bind("<Return>",             accept_cmd)
        top.protocol('WM_DELETE_WINDOW', self.__cancel)
    #=========================================================================
    # METHOD: __cancel
    # PURPOSE: cancel button call-back
    #=========================================================================
    def __cancel(self):
        self._return_results = {}
        self._return_results["ACCEPT"] = False
        self._return_results["KEYS"]   = self._all_keys
        for key in self._entry_keys :
            val = self._entry_val[key]
            self._return_results[key] = val
        for key in self._check_keys :
            val = self._check_val[key]
            self._return_results[key] = val
        for key in self._radio_keys :
            val = self._radio_val[key]
            self._return_results[key] = val
        top = self._Component["top"]
        top.quit()
    #=========================================================================
    # METHOD: __accept
    # PURPOSE: accept button call-back
    #=========================================================================
    def __accept(self):
        self._return_results = {}
        self._return_results["ACCEPT"] = True
        self._return_results["KEYS"]   = self._all_keys
        for key in self._entry_keys :
            win = self._entry_win[key]
            vdf = self._entry_val[key]
            val = win.get()
            val = string.strip(val)
            if   type(vdf) is float :
                val = string.atof(val)
            elif type(vdf) is int :
                val = string.atoi(val)
            self._return_results[key] =  val
        for key in self._check_keys :
            var = self._check_var[key]
            val = var.get()
            val = True if val == 1 else False
            self._return_results[key] =  val
        for key in self._radio_keys :
            var = self._radio_var[key]
            val = var.get()
            self._return_results[key] =  val
        top = self._Component["top"]
        top.quit()
