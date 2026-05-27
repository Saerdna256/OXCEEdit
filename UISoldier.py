import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import * # pyright: ignore[reportWildcardImportFromLibrary]

from OXCCEHandlers.savedata import savedata
from OXCCEHandlers.bases import base
from OXCCEHandlers.soldier import soldier
from OXCCEHandlers.constants import *

class SoldierWindow(ttk.Toplevel):
    def __init__(self, unit : soldier, root : ttk.Window) -> None:
        # create modal window
        super().__init__(title=unit.name, iconphoto="", resizable=(False, False), topmost=True, transient=root)
        self.wait_visibility()
        self.grab_set()
        self.focus()

        # temp vars to allow canceling out
        self.edited = False # Flags if any edits have been done
        self.id = str(unit.id)
        self.name = unit.name

         # UI Elements definitions
        ##########################################

        header_bar = ttk.Frame(master=self)
        body = ttk.Frame(master=self)

        self.header_text = ttk.Label(master=header_bar, text=f"Soldier {unit.id}: {unit.name}", bootstyle=SUCCESS)

        # UI Elements placement
        ##########################################
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        self.header_text.pack(anchor=CENTER, expand=True, fill=BOTH)

        header_bar.grid(column=1, row=0, sticky=NSEW)

        body.grid(column=1, columnspan=3, row=1, sticky=NSEW)

        # wait for window to close
        self.wait_window(self)
