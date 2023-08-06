#!/usr/bin/env python
import user, decida, decida.test
from decida.FrameNotebook import FrameNotebook
from decida.TextWindow import TextWindow
from decida.XYplotx import XYplotx
from decida.Data import Data
import Tkinter 

fn = FrameNotebook(tab_location="top", destroy=False)
    
f1 = fn.new_page("Page 1")
b1 = Tkinter.Button(f1, text="Change Tab Location")
e1 = Tkinter.Entry(f1)
b1.pack()
e1.pack()

def cmd(self=fn):
    tl = self["tab_location"]
    if   tl == "top" :
        self["tab_location"] = "right"
    elif tl == "right" :
        self["tab_location"] = "top"
b1["command"] = cmd

f2 = fn.new_page("Page_2")
b2 = Tkinter.Button(f2, text="Destroy Page 1", command=lambda:f1.destroy())
b3 = Tkinter.Button(f2, text="Beep",   command=lambda:Tkinter._default_root.bell())
b2.pack()
b3.pack()

tw = TextWindow(fn.new_page("text"))

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "LTspice_ac_ascii.raw")
XYplotx(fn.new_page("plot"), command=[d, "frequency DB(V(vout1)) PH(V(vout1))"], title="AC analysis", xaxis="log", ymin=-60.0, ymax=0.0, wait=False)

fn.status("waiting to add new page")
fn.wait("CONTINUE 1")
fn.status("")

tw = TextWindow(fn.new_page("text 1"))

fn.status("waiting to delete 1 page")
fn.wait("CONTINUE 2a")
fn.status("")
fn.del_page()

fn.status("waiting to delete 3 pages")
fn.wait("CONTINUE 2b")
fn.status("")
fn.del_page()
fn.del_page()
fn.del_page()

fn.status("waiting to delete last page")
fn.wait("CONTINUE 3")
fn.status("")
fn.del_page()

fn.wait("EXIT")
