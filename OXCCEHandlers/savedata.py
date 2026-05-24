from bases import base

class savedata:
    def __init__(self, name = "") -> None:
        self.name = name
        self.credits : float = 0.0
        self.bases : list[base] = []

    def get_num_bases (self)-> int:
        if self.bases == []:
            return 0
        return len(self.bases)
    
    def debug_savedata_to_string(self) -> str:
        return_value = f"{self.name}\n"
        return_value += f"Cedits: {int(self.credits)}\n"
        return_value += "Öist of bases:"
        for current in self.bases:
            return_value += current.debug_base_to_string()
        return return_value        
        