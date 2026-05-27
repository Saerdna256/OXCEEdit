from .bases import base
from .soldier import soldier

# Helper class to manage the parts of the savedata we might want to edit. Redaing and setting the name memeber 
# directly is ok, other access to the member variabels should in this case be completly done by the
#  accessors to make sure the data stays in the right format,
#
# User input is expected to already be sanitized and we will accept anything from existing files.


class savedata:
    def __init__(self, name = "") -> None:
        self.name = name
        self.credits : float = 0.0
        self.bases : list[base] = []

    def get_num_bases(self)-> int:
        if self.bases == []:
            return 0
        return len(self.bases)
    
    def set_credits(self, value : int) -> None:
        self.credits = float(value)

    def get_credits(self) -> int:
        return int(self.credits)
    
    def add_base(self, value: base) -> None:
        if (value == None) or (not isinstance(value, base)):
            raise ValueError(f"{value} is not a valid base")
        self.bases.append(value)

    def get_base_at_index(self, index : int) -> base:
        if (index < 0 ) or (index > len(self.bases)-1):
            raise ValueError(f"Invalid Index for base: {index}")
        return self.bases[index]
    
    def get_all_bases(self) -> list[base] | None:
        if self.bases == []:
            return None
        return self.bases
    
    def get_soldier_by_id(self, id : int) -> soldier | None:
        for base in self.bases:
            try:
                temp = base.get_soldier_by_id(id)
            except ValueError:
                continue
            return temp
        return None
    
    def debug_savedata_to_string(self) -> str:
        return_value = f"{self.name}\n"
        return_value += f"Cedits: {int(self.credits)}\n\n"
        return_value += "List of bases:\n"
        return_value += "--------------\n"
        for current in self.bases:
            return_value += current.debug_base_to_string()
        return return_value        
        