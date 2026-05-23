from soldier import soldier

class base:
    def __init__(self, order_number = 0, name = "") -> None:
        self.name = name
        self.order_number = order_number

        # soldiers at the base
        self.soldiers : list[soldier] = []

    def get_soldier_by_id(self, id : int) -> soldier:        
        for soldier in self.soldiers:
            if soldier.id == id:
                return soldier
        raise ValueError(f"No soldier with id {id} at base {self.name}\n”")
    
    def get_num_soldier(self) -> int:
        return len(self.soldiers)
    
    def add_soldier_to_base(self, unit : soldier) -> None:
        self.soldiers.append(unit)
    
    def debug_base_to_string(self) -> str:
        return_value = f"{self.name}\n"
        for unit in self.soldiers:
            return_value += unit.debug_soldier_to_string()
            return_value += "\n"
        return_value += "\n"
        return return_value