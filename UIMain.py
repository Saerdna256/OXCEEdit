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
        self.dataChanged : bool = True    # Any unsaved changes?
        self.savefile_path : str = "" # Path to current savefile

        # event handlers
        self.protocol("WM_DELETE_WINDOW", self.custom_exit_handler)

        # UI layout
        """ For reference:
        Top Level has three element, displayed top to bottom over the full width. Top and bottom are only as high as needed with the center expending as screenspace allows 
        1) Savefile title, path to savefile and Load File button. Neither the titel nor the path can be edited (directly)
        2) Table of the soldiers in a tabbed view, every tab is a base
        3) Funds (can be edited directly) leftbound, Save button in the center, Exit button rightbound 
        """


    def custom_exit_handler(self) -> None:
        if(self.dataChanged):
            dialog = MessageDialog("Unsaved edits, exit anyways?", "Unsaved edits", buttons=["Exit", "Cancel"], parent=self, default="Cancel", icon=Icon.warning)
            dialog.show()            
            if dialog.result != "Exit":
                return
        self.destroy()

    def custom_exit(self) -> None:
        self.destroy()
    

#####################################################################
## DEBUG to quickly test this window alone:

def main() -> None:
    root = MainWindow()
    root.mainloop()

if __name__ == "__main__":
    main()
