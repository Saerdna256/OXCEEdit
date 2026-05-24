from constants import TU, STAMINA, HEALTH, BRAVERY, REACTIONS, FIRING, THROWING, STRENGTH, PSI_STRENGTH, PSI_SKILL, BASE, CURRENT

# Helper class to manage individual soldier. Note that reading from the variabels is ok,
# but they are meant to be set through the setter methods to make sure that all variable pairs
# stay in a reasonable range to each other (ie don't have larger base than current value).
#
# User input is expected to already be sanitized and we will accept anything from existing files.

class soldier:
    def __init__(self, id : int = 0, name:str = "") -> None:
        self.id = id
        self.name = name

        self.stats = \
        {
            TU:[0,0],
            STAMINA:[0,0],
            HEALTH:[0,0],
            BRAVERY:[0,0],
            REACTIONS:[0,0],
            FIRING:[0,0],
            THROWING:[0,0],
            STRENGTH:[0,0],
            PSI_SKILL:[0,0],
            PSI_STRENGTH:[0,0]
        }        

    def set_id(self, id : int) -> None:
        self.id = id

    def set_name(self, name:str) -> None:
        self.name = name

    # When setting base or current stats, also check if this leaves the base as smalller or equal
    # to the current stat, othewise also set the other value to always keep base as smaller
    # or equal
    def set_base_stat(self, stat : str, value : int) -> None:
        self.stats[stat][BASE] = value
        if self.stats[stat][BASE] > self.stats[stat][CURRENT]:
            self.stats[stat][CURRENT] = value
    
    def set_current_stat(self, stat : str, value : int) -> None:
        self.stats[stat][CURRENT] = value
        if self.stats[stat][BASE] > self.stats[stat][CURRENT]:
            self.stats[stat][BASE] = value

    # for debugging
    def debug_soldier_to_string(self) -> str:
        return_value = ""

        return_value += f"{self.name} (ID: {self.id}):\n"
        lines = self.stats.keys()
        for line in lines:
            return_value += f"{line}: {self.stats[line][BASE]} / {self.stats[line][CURRENT]}\n"        
        return_value += "\n"

        return return_value
