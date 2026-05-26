import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageDialog
from ttkbootstrap.icons import Icon
from ttkbootstrap.constants import * # pyright: ignore[reportWildcardImportFromLibrary]



class MainWindow(ttk.Window):
    def __init__(self) -> None:
        super().__init__(themename="cyborg", title="OXCEEdit")        
        self.geometry("1280x720")

        # custom variables
        self.dataChanged : bool = False    # Any unsaved changes?
        self.savefile_path : str = "" # Path to current savefile
        self.savedataName : str = "Dummy"

        # event handlers
        self.protocol("WM_DELETE_WINDOW", self.custom_exit_handler)

        # UI Elements definitions
        ##########################################
        """ For reference:
        Top Level has three element, displayed top to bottom over the full width. Top and bottom are only as high as needed with the center expending as screenspace allows 
        1) Savefile title, path to savefile and Load File button. Neither the titel nor the path can be edited (directly)
        2) Table of the soldiers in a tabbed view, every tab is a base. Double-clicking a soldier opens the edit soldier dialog.
        3) Funds (can be edited directly) leftbound, Save button in the center, Exit button rightbound 
        
        """
        # Frame for top elements        
        topleveltoprow = ttk.Labelframe(self, labelanchor=NW, text="Savefile", bootstyle=PRIMARY)
        topleveltoprow.columnconfigure(0, weight=0)
        topleveltoprow.columnconfigure(1, weight=0)
        topleveltoprow.columnconfigure(2, weight=1)

        # Top Elements
        saveTitleInput = ttk.Entry(topleveltoprow, bootstyle=PRIMARY, textvariable=self.savedataName, takefocus=False, state=READONLY, width=64)
        saveTitleLabel = ttk.Label(topleveltoprow, bootstyle=PRIMARY, text="Savedata Name: ")
        loadButton = ttk.Button(topleveltoprow, text="Load File...", padding=5)
        
        # UI Elements placement
        ##########################################
        # Main window
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Top Elements into frame
        saveTitleLabel.grid(column=0, row=0, sticky=W, padx =5, pady = 5)
        saveTitleInput.grid(column=1, row=0, sticky=W, padx =5, pady = 5)        
        loadButton.grid(column=2, row=0, sticky=E, padx=5, pady=5)

        # Frames into window        
        topleveltoprow.grid(column=0, row=0, sticky=NSEW, ipadx=5, ipady=5, padx=5, pady=5)


    def custom_exit_handler(self) -> None:
        if(self.dataChanged):
            dialog = MessageDialog("Unsaved edits, exit anyways?", "Unsaved edits", buttons=["Exit", "Cancel"], parent=self, default="Cancel", icon=Icon.warning)
            dialog.show()            
            if dialog.result != "Exit":
                return
        self.destroy()        

#####################################################################
## DEBUG to quickly test this window alone:

def main() -> None:
    root = MainWindow()
    root.mainloop()

if __name__ == "__main__":
    main()
