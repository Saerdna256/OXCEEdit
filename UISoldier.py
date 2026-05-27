# import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import * # pyright: ignore[reportWildcardImportFromLibrary]

from OXCCEHandlers.soldier import soldier
from OXCCEHandlers.constants import *

class SoldierWindow(ttk.Toplevel):
    def __init__(self, unit : soldier, root : ttk.Window) -> None:
        # create modal window
        super().__init__(title=unit.name, iconphoto="", resizable=(False, False), topmost=True, transient=root)
        self.wait_visibility()
        self.grab_set()
        self.focus()

        isOK = self.register(self.testOK)

        # temp vars to allow canceling out
        ##########################################
        self.edited = False # Flags if any edits have been done
        self.base_stats = {
            TU: ttk.StringVar(value=str(unit.stats[TU][OX_BASE])),
            STAMINA: ttk.StringVar(value=str(unit.stats[STAMINA][OX_BASE])),
            HEALTH: ttk.StringVar(value=str(unit.stats[HEALTH][OX_BASE])),
            BRAVERY: ttk.StringVar(value=str(unit.stats[BRAVERY][OX_BASE])),
            REACTIONS: ttk.StringVar(value=str(unit.stats[REACTIONS][OX_BASE])),
            FIRING: ttk.StringVar(value=str(unit.stats[FIRING][OX_BASE])),
            THROWING: ttk.StringVar(value=str(unit.stats[THROWING][OX_BASE])),
            STRENGTH: ttk.StringVar(value=str(unit.stats[STRENGTH][OX_BASE])),
            PSI_SKILL: ttk.StringVar(value=str(unit.stats[PSI_SKILL][OX_BASE])),
            PSI_STRENGTH: ttk.StringVar(value=str(unit.stats[PSI_STRENGTH][OX_BASE]))
        }

        self.current_stats = {
            TU: ttk.StringVar(value=str(unit.stats[TU][OX_CURRENT])),
            STAMINA: ttk.StringVar(value=str(unit.stats[STAMINA][OX_CURRENT])),
            HEALTH: ttk.StringVar(value=str(unit.stats[HEALTH][OX_CURRENT])),
            BRAVERY: ttk.StringVar(value=str(unit.stats[BRAVERY][OX_CURRENT])),
            REACTIONS: ttk.StringVar(value=str(unit.stats[REACTIONS][OX_CURRENT])),
            FIRING: ttk.StringVar(value=str(unit.stats[FIRING][OX_CURRENT])),
            THROWING: ttk.StringVar(value=str(unit.stats[THROWING][OX_CURRENT])),
            STRENGTH: ttk.StringVar(value=str(unit.stats[STRENGTH][OX_CURRENT])),
            PSI_SKILL: ttk.StringVar(value=str(unit.stats[PSI_SKILL][OX_CURRENT])),
            PSI_STRENGTH: ttk.StringVar(value=str(unit.stats[PSI_STRENGTH][OX_CURRENT]))
        }
        
         # UI Elements definitions
        ##########################################

        self.header_bar = ttk.Frame(master=self)
        self.body = ttk.Frame(master=self)

        self.header_text = ttk.Label(master=self.header_bar, text=f"Soldier {unit.id}: {unit.name}", bootstyle=SUCCESS)

        self.base_label = ttk.Label(master=self.body, text="base")
        self.current_label = ttk.Label(master=self.body, text="current")

        self.tu_label = ttk.Label(master=self.body, text="tu")
        self.stamina_label = ttk.Label(master=self.body, text="stamina")
        self.health_label = ttk.Label(master=self.body, text="health")
        self.bravery_label = ttk.Label(master=self.body, text="bravery")
        self.reactions_label = ttk.Label(master=self.body, text="reactions")
        self.firing_label = ttk.Label(master=self.body, text="firing")
        self.throwing_label = ttk.Label(master=self.body, text="throwing")
        self.strength_label = ttk.Label(master=self.body, text="strength")
        self.psi_skill_label = ttk.Label(master=self.body, text="psi skill")
        self.psy_strength_label = ttk.Label(master=self.body, text="psi strength")

        self.base_tu_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[TU])
        self.base_stamina_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[STAMINA])
        self.base_health_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[HEALTH])
        self.base_bravery_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[BRAVERY])
        self.base_reactions_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[REACTIONS])
        self.base_firing_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[FIRING])
        self.base_throwing_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[THROWING])
        self.base_strength_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[STRENGTH])
        self.base_psi_skill_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[PSI_SKILL])
        self.base_psy_strength_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.base_stats[PSI_STRENGTH])

        self.current_tu_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[TU])
        self.current_stamina_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[STAMINA])
        self.current_health_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[HEALTH])
        self.current_bravery_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[BRAVERY])
        self.current_reactions_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[REACTIONS])
        self.current_firing_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[FIRING])
        self.current_throwing_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[THROWING])
        self.current_strength_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[STRENGTH])
        self.current_psi_skill_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[PSI_SKILL])
        self.current_psy_strength_entry = ttk.Entry(master=self.body, width=3, validate='all', validatecommand=(isOK, '%P'), textvariable=self.current_stats[PSI_STRENGTH])



        # UI Elements placement
        ##########################################
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        self.header_text.pack(anchor=CENTER, expand=True, fill=BOTH)

        self.base_label.grid(row=0, column=1, sticky=NSEW)
        ttk.Separator(self.body, orient=VERTICAL).grid(row=0, rowspan=11, column=2, sticky=NS)
        self.current_label.grid(row=0, column=3, sticky=NSEW)

        self.tu_label.grid(row=1, column=0, sticky=E)
        self.stamina_label.grid(row=2, column=0, sticky=E)
        self.health_label.grid(row=3, column=0, sticky=E)
        self.bravery_label.grid(row=4, column=0, sticky=E)
        self.reactions_label.grid(row=5, column=0, sticky=E)
        self.firing_label.grid(row=6, column=0, sticky=E)
        self.throwing_label.grid(row=7, column=0, sticky=E)
        self.strength_label.grid(row=8, column=0, sticky=E)
        self.psi_skill_label.grid(row=9, column=0, sticky=E)
        self.psy_strength_label.grid(row=10, column=0, sticky=E)

        self.base_tu_entry.grid(row=1, column=1, sticky=E)
        self.base_stamina_entry.grid(row=2, column=1, sticky=E)
        self.base_health_entry.grid(row=3, column=1, sticky=E)
        self.base_bravery_entry.grid(row=4, column=1, sticky=E)
        self.base_reactions_entry.grid(row=5, column=1, sticky=E)
        self.base_firing_entry.grid(row=6, column=1, sticky=E)
        self.base_throwing_entry.grid(row=7, column=1, sticky=E)
        self.base_strength_entry.grid(row=8, column=1, sticky=E)
        self.base_psi_skill_entry.grid(row=9, column=1, sticky=E)
        self.base_psy_strength_entry.grid(row=10, column=1, sticky=E)

        self.current_tu_entry.grid(row=1, column=3, sticky=W)
        self.current_stamina_entry.grid(row=2, column=3, sticky=W)
        self.current_health_entry.grid(row=3, column=3, sticky=W)
        self.current_bravery_entry.grid(row=4, column=3, sticky=W)
        self.current_reactions_entry.grid(row=5, column=3, sticky=W)
        self.current_firing_entry.grid(row=6, column=3, sticky=W)
        self.current_throwing_entry.grid(row=7, column=3, sticky=W)
        self.current_strength_entry.grid(row=8, column=3, sticky=W)
        self.current_psi_skill_entry.grid(row=9, column=3, sticky=W)
        self.current_psy_strength_entry.grid(row=10, column=3, sticky=W)

        self.header_bar.grid(column=1, row=0, sticky=NSEW)

        self.body.grid(column=1, columnspan=3, row=1, sticky=NSEW)
        
        # wait for window to close
        self.wait_window(self)
    
    def testOK(self, what : str) -> bool:
        try:
            value = int(what)
        except ValueError:
            return False
        if value > 256:
            return False
        if value < 0:
            return False
        return True
