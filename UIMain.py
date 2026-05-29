from shutil import copy as sh_copy

import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageDialog
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.icons import Icon
from ttkbootstrap.widgets.tableview import Tableview
from ttkbootstrap.constants import * # pyright: ignore[reportWildcardImportFromLibrary]

from OXCCEHandlers.savedata import savedata
from OXCCEHandlers.bases import base
from OXCCEHandlers.soldier import soldier
from OXCCEHandlers.constants import *
from OXCCEHandlers.reader import read_file
from OXCCEHandlers.writer import write_savefile

from UISoldier import SoldierWindow

class MainWindow(ttk.Window):
    def __init__(self) -> None:
        super().__init__(themename="cyborg", title="OXCEEdit")        
        self.geometry("1280x720")
        self.minsize(width=1280, height=720)

        # custom variables
        self.dataChanged : bool = False    # Any unsaved changes?                
        self.data : savedata| None = None
        self.savefile = ""

        # frames for bases, dynamically constructed and destroyed
        self.frames_for_bases : list[ttk.Frame] = []

        # soldier tables for later updating (after edits)
        self.soldier_tables : list[Tableview] = []

        # String Vars for input monitoring
        self.creditsVar = ttk.StringVar()

        # event handlers
        self.protocol("WM_DELETE_WINDOW", self.custom_exit_handler)
        isCreditsOK = self.register(self.testCredits)

        # UI Elements definitions
        ##########################################
        
        # Frame for top elements        
        self.topleveltoprow = ttk.Labelframe(self, labelanchor=NW, text="Savefile", bootstyle=PRIMARY)
        self.topleveltoprow.columnconfigure(0, weight=0)
        self.topleveltoprow.columnconfigure(1, weight=0)
        self.topleveltoprow.columnconfigure(2, weight=0)
        self.topleveltoprow.columnconfigure(3, weight=0)
        self.topleveltoprow.columnconfigure(4, weight=1)

        # Frame for middle elements
        self.toplevelmiddlerow = ttk.Labelframe(self, labelanchor=NW, text="Soldiers at bases", bootstyle=PRIMARY)
        self.toplevelmiddlerow.rowconfigure(0, weight=0)
        self.toplevelmiddlerow.rowconfigure(1, weight=1)
        self.toplevelmiddlerow.columnconfigure(0, weight=1)

        # Frame for bottom elements
        self.toplevelbottomrow = ttk.Frame(self)
        self.toplevelbottomrow.columnconfigure(0, weight=1)
        self.toplevelbottomrow.columnconfigure(2, weight=1)

        # Top Elements
        self.saveTitleLabel = ttk.Label(self.topleveltoprow, bootstyle=PRIMARY, text="Savedata Name:")
        self.saveTitleInput = ttk.Entry(self.topleveltoprow, bootstyle=PRIMARY, takefocus=False, state=READONLY, width=48)
        self.saveCreditsLabel = ttk.Label(self.topleveltoprow, bootstyle=PRIMARY, text="Credits (edit in place):")
        self.saveCreditsInput = ttk.Entry(self.topleveltoprow, bootstyle=PRIMARY, takefocus=True, state=NORMAL, width=16, 
                                          textvariable=self.creditsVar, validate='all', validatecommand=(isCreditsOK, '%P'))
        self.loadButton = ttk.Button(self.topleveltoprow, text="Load File...", padding=5, command=self.load_file)

        # Middle Elements
        self.instructionsLabel = ttk.Label(self.toplevelmiddlerow, bootstyle=PRIMARY, text="(Double Click on row to edit.)")
        self.baseTabs = ttk.Notebook(self.toplevelmiddlerow, bootstyle=PRIMARY) # One pane per base loaded
        self.baseTabs.rowconfigure(0, weight=1)
        self.baseTabs.columnconfigure(0, weight=1)

        # Dummy base pane for when no data is loaded
        self.dummyPanel = ttk.Frame(self.baseTabs, takefocus=False)
        self.dummyPanel.columnconfigure(0, weight=1)
        self.dummyText = ttk.Label(self.dummyPanel, bootstyle=SECONDARY, text="No data loaded.")

        # Bottom elements
        self.saveButton = ttk.Button(self.toplevelbottomrow, text="Save File", padding=5, command=self.onSaveClick, state=DISABLED)
        self.exitButton = ttk.Button(self.toplevelbottomrow, text="Exit", padding=5, command=self.custom_exit_handler, bootstyle=SUCCESS)
        
        # UI Elements placement
        ##########################################

        # Main window
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Top elements into frame
        self.saveTitleLabel.grid(column=0, row=0, sticky=W, padx =5, pady = 5)
        self.saveTitleInput.grid(column=1, row=0, sticky=W, padx =5, pady = 5)
        self.saveCreditsLabel.grid(column=2, row=0, sticky=W, padx =5, pady = 5)        
        self.saveCreditsInput.grid(column=3, row=0, sticky=W, padx =5, pady = 5)        
        self.loadButton.grid(column=4, row=0, sticky=E, padx=5, pady=5)

        # Middle elements into frame
        self.instructionsLabel.grid(row=0, column=0, sticky="", padx=5, pady=5)

        # Dummy Pane into notebook, notebook into middle frame
        self.dummyText.grid(column=0, row=0, sticky=N, pady=5)
        self.baseTabs.add(self.dummyPanel, text="No data") # Note to self: .forget() to remove a tab from the notebook
        self.baseTabs.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)

        # Bottom elements into frame
        self.saveButton.grid(column=1, row=0, sticky=S, padx=5, pady=5)
        self.exitButton.grid(column=2, row=0, sticky=SE, padx=5, pady=5)

        # Frames into window        
        self.topleveltoprow.grid(column=0, row=0, sticky=NSEW, ipadx=5, ipady=5, padx=5, pady=5)
        self.toplevelmiddlerow.grid(column=0, row=1, sticky=NSEW, ipadx=5, ipady=5, padx=5, pady=5)
        self.toplevelbottomrow.grid(column=0, row=2, sticky=NSEW, ipadx=5, ipady=5, padx=5, pady=5)
    
    # METHODS ###########################################################################################

    def custom_exit_handler(self) -> None:
        if(self.dataChanged):
            dialog = MessageDialog("Unsaved edits, exit anyways?", "Unsaved edits", buttons=["Exit", "Cancel"], parent=self, default="Cancel", icon=Icon.warning)
            dialog.show()            
            if dialog.result != "Exit":
                return
        self.destroy()

    def soldier_double_click(self, event : tk.Event) -> None:
        # Get Data from event, what soldier did we click on?
        item_id = event.widget.focus()
        if not item_id:
            return
        item = event.widget.item(item_id) # pyright: ignore[reportAttributeAccessIssue]
        soldierID = item['values'][0] # First value should be the soldier ID

        # open child window to edit this soldier
        if not self.data:
            return
        unit = self.data.get_soldier_by_id(int(soldierID))
        if not unit:
            return
        
        # display the actual editing popup dialog
        editor = SoldierWindow(unit, self)

        # Process data after dialog has been closed
        if not editor.edited:
            return
        
        self.dataChanged = True
        
        # new row data
        row = [unit.id, unit.name]                

        # edit the data in the soldier object (unit) and the new row data to reflect the data returned from the dialog
        for (key, value) in editor.base_stats.items():
            unit.stats[key][OX_BASE] = int(value.get())
        for (key, value) in editor.current_stats.items():
            unit.stats[key][OX_CURRENT] = int(value.get())
            row.append(int(value.get()))
        
        # Update visual soldier table
        tab_index = self.baseTabs.index("current")
        self.soldier_tables[tab_index-1].view.item(item_id, values=row)
        self.soldier_tables[tab_index-1].load_table_data()

        # unlock save file button
        self.saveButton.config(state=NORMAL)

    def load_file(self) -> None:
        # get the data
        filepath = filedialog.askopenfilename(title="Select OXCE savefile")
        if not filepath:
            return
        try:
            self.data = read_file(str(filepath))
        except ValueError:
            Messagebox.show_error(message="Invalid file format!", title="Error")
            return
        
        # store savefile path for saving
        self.savefile = filepath
        
        # delete old data of bases, if any
        if len(self.frames_for_bases) > 0:
            for frame in self.frames_for_bases:
                self.baseTabs.forget(frame)
                frame.destroy()
            self.frames_for_bases = []
            self.soldier_tables = []
        self.baseTabs.hide(self.dummyPanel) # don't display the "no data" tab as AFAIK any savefile has at least one base

        # display the data
        self.saveTitleInput.config(state=NORMAL)
        self.saveTitleInput.delete(0, END)
        self.saveTitleInput.insert(0, self.data.name)
        self.saveTitleInput.config(state=READONLY)
        
        self.creditsVar.set(str(self.data.get_credits()))        
        
        # monitor for changes
        self.creditsVar.trace_add("write", self.on_credits_changed)

        for base in self.data.bases:
            self.create_base_pane(base)    

        self.dataChanged = False
        self.saveButton.config(state=DISABLED)            
        
    # extracted for readability: creating the frame with the information on soldiers in a single base
    def create_base_pane(self, current_base : base) -> None:
        new_pane = ttk.Frame(self.baseTabs)

        # create soldier table
        # note: only display the current values, as those are more pertinent to gameplay
        headers = ["ID", "name", "TU", "stamina", "health", "bravery", "reactions", "firing", "throwing", "strength", "psi skill", "psi strength"]
        row_data = []
        for soldier in current_base.soldiers:
            row = (
                soldier.id,
                soldier.name,
                soldier.stats[TU][OX_CURRENT],
                soldier.stats[STAMINA][OX_CURRENT],
                soldier.stats[HEALTH][OX_CURRENT],
                soldier.stats[BRAVERY][OX_CURRENT],
                soldier.stats[REACTIONS][OX_CURRENT],
                soldier.stats[FIRING][OX_CURRENT],
                soldier.stats[THROWING][OX_CURRENT],
                soldier.stats[STRENGTH][OX_CURRENT],
                soldier.stats[PSI_SKILL][OX_CURRENT],
                soldier.stats[PSI_STRENGTH][OX_CURRENT],
            )

            row_data.append(row)

        data_table = Tableview(
            master=new_pane,
            coldata=headers,
            rowdata=row_data,
            autofit=True,
            paginated=False,
            searchable=False,
            bootstyle=PRIMARY,
            disable_right_click=True,
            yscrollbar=True,                        
        )

        data_table.view.bind("<Double-1>", self.soldier_double_click)

        # add table and frame to main program
        self.soldier_tables.append(data_table)
        data_table.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        self.frames_for_bases.append(new_pane)
        self.baseTabs.add(new_pane, text=current_base.name)

    def on_credits_changed(self, *args) -> None:
        if self.data != None:
            self.data.set_credits(int(self.creditsVar.get()))
        self.dataChanged = True
        self.saveButton.config(state=NORMAL)

    def testCredits(self, what : str) -> bool:
        try:
            int(what)
        except ValueError:
            return False
        return True
    
    def onSaveClick(self) -> None:
        if self.data == None:
            return
        # create backup
        sh_copy(self.savefile, self.savefile+".bak")
        
        # write new save data
        write_savefile(self.savefile, self.data, self.savefile)

        # all data saved, so revert to the no data changed state
        self.dataChanged = False
        self.saveButton.config(state=DISABLED)

