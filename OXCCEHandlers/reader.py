from io import TextIOWrapper

from .constants import *
from .savedata import savedata
from .bases import base
from .soldier import soldier

##########################################################################################
# First part of the actual savefile management:
# Get all the necessary data from the existing savefile
# 
# NOTE: this is NOT part of the savedata class as that class does not represent the
# whole savefile but merely some data extracted from it. In contrast, this and the 
# savefile writer functions act on the actual savefile.
# 
# OVERVIEW:
# 00 - open the file, all reads from now on will happen line by line
# 01 - check if first line start with "name: ", if not, abort
# 02 - create savedata variable, read the line !after! "name: " and store the string as the name of the savedata name
# 03 - continue until the line "funds:"
# 04 - disregard "  - " at the start of the next line, the number following can be saved as funds in the savedata
# 05 - continue to the line "bases:", here the actual work starts; the following will loop until we have no more bases
# 05 a - search for the line beginning with "    name: " or "options:". If options, all bases are accounted for and we are done
# 05 b - Take the following string and save it as the base name
# 05 c - use a counter for the order number and store that as well
# 05 d - search for "    soldiers:" and start the soldier loop on the next line
# 05 e 1  - search for "      - type: STR_SOLDIER" or "    crafts:". If crafts, exit the soldier loop
# 05 e 2  - following line sould start with  "        id: ", save the following number in a temp var
# 05 e 3  - following line should start with "        name: ", save the following name in a temp var
# 05 e 4  - save the temp vars in a new soldier object
# 05 e 5  - continue untile the line "        initialStats:"
# 05 e 6  - the following 10 lines should start with "          ", the stat name, ": ". Check for that, extract the stat name and the following number
# 05 e 7  - use the stat name to save the number as the initial stat in the soldier object
# 05 e 8  - continue untile the line "        currentStats:"
# 05 e 9  - the following 10 lines should start with "          ", the stat name, ": ". Check for that, extract the stat name and the following number
# 05 e 10 - use the stat name to save the number as the current stat in the soldier object
# 05 e 11 - add the soldier object to the base and continue loop
# 05 f - add the base object to the savedata
# 06 - return the savedata object
##########################################################################################

# no need for a class, do this data driven
# the actual save data will be stored and maintained be the main program

#read and return a single soldier
def read_soldier(file_handle : TextIOWrapper) -> soldier:
    # 05 e 2  - following line sould start with  "        id: ", save the following number in a temp var   
    line = file_handle.readline()
    if not line.startswith(SOLDIER_ID_ID):
        raise ValueError("Invalid save file, did not find soldier id!")
    tempID = int(line[len(SOLDIER_ID_ID):])

    # 05 e 3  - following line should start with "        name: ", save the following name in a temp var
    line = file_handle.readline()
    if not line.startswith(SOLDIER_NAME_ID):
        raise ValueError("Invalid save file, did not find soldier name!")
    tempName = line[len(SOLDIER_NAME_ID):].strip()

    # 05 e 4  - save the temp vars in a new soldier object
    newSoldier = soldier(tempID, tempName)

    # 05 e 5  - continue untile the line "        initialStats:"
    while (line != SOLDIER_INITIAL_STATS_ID):
        line = file_handle.readline()
        # a proper save file does not conatin any empty lines, so a empty line means EOF!
        if line == "":
            raise ValueError("Improper savefile, either containing an empty line or no soldier stats!")
        
    # 05 e 6  - the following 10 lines should start with "          ", the stat name, ": ". Check for that, extract the stat name and the following number
    for  _ in range(10):
        line = file_handle.readline()
        if not line.startswith(SOLDIER_STAT_PREFIX):
            raise ValueError("Improper formatted save file, could not read an initial stat!")
        tempString = line[len(SOLDIER_STAT_PREFIX):]
        statStrings = tempString.split(SOLDIER_STAT_SUFFIX)
        statName = statStrings[0].strip()
        statValue = int(statStrings[1].strip())
        # 05 e 7  - use the stat name to save the number as the initial stat in the soldier object
        newSoldier.set_base_stat(statName, statValue)

    # 05 e 8  - continue untile the line "        currentStats:"
    while(line != SOLDIER_CURRENT_STATS_ID):
        line = file_handle.readline()
        if line == "":
            raise ValueError("Improper savefile, either containing an empty line or no current soldier stats!")
        
    # 05 e 9  - the following 10 lines should start with "          ", the stat name, ": ". Check for that, extract the stat name and the following number
    for _ in range(10):
        line = file_handle.readline()
        if not line.startswith(SOLDIER_STAT_PREFIX):
            raise ValueError("Improper formatted save file, could not read a current stat!")
        tempString = line[len(SOLDIER_STAT_PREFIX):]
        statStrings = tempString.split(SOLDIER_STAT_SUFFIX)
        statName = statStrings[0].strip()
        statValue = int(statStrings[1].strip())
        # 05 e 10 - use the stat name to save the number as the current stat in the soldier object
        newSoldier.set_current_stat(statName, statValue)
    
    # Done with this soldier, continue with the base
    return newSoldier

# read and return a single base
def read_base(file_handle : TextIOWrapper, name : str, order : int) -> base:
    # 05 b - Take the following string and save it as the base name    
    # 05 c - use a counter for the order number and store that as well
    new_base = base(order, name)

    # 05 d - search for "    soldiers:" and start the soldier loop on the next line
    line = file_handle.readline()
    while(not line.startswith(SOLDIER_BLOCK_START_ID)):
        line = file_handle.readline()
        if line == "":
            raise ValueError("Improper savefile, either containing an empty line or soldier infos!")
        
    # 05 e 1  - search for "      - type: STR_SOLDIER" or "    crafts:". If crafts, exit the soldier loop
    while(True):
        line = file_handle.readline()
        if(line.startswith(SOLDIER_BLOCK_END_ID)):
            break
        if(line.startswith(SOLDIER_START_ID)):
            new_base.add_soldier_to_base(read_soldier(file_handle))
    
    return new_base

# read the whole savefile and return the savedata object
def read_file(filename : str) -> savedata:
    ## 00 - open the file, all reads from now on will happen line by line
    new_data = None
    with open(filename, 'r') as file_handle:
        # 01 - check if first line start with "name: ", if not, abort
        line = file_handle.readline()
        if not line.startswith(SAVEFILENAME_ID):
            raise ValueError(f"Not a valid savegame: \"{filename}\"")
        
        # 02 - create savedata variable, read the line !after! "name: " and store the string as the name of the savedata name
        new_data = savedata(line[len(SAVEFILENAME_ID):].strip())

        # 03 - continue until the line "funds:"
        while(not line.startswith(FUNDS_ID)):
            line = file_handle.readline()
            if line == "":
                raise ValueError("Improper savefile, either containing an empty line or no funds!")
        
        # 04 - desregard "  - " at the start of the next line, the number following can be saved as funds in the savedata
        line = file_handle.readline()
        funds = int(line[len(FUNDS_PREFIX):])
        new_data.set_credits(funds)

        # 05 - continue to the line "bases:", here the actual work starts; the following will loop until we have no more bases
        while(not line.startswith(BASES_START_ID)):
            line = file_handle.readline()
            if line == "":
                raise ValueError("Improper savefile, either containing an empty line or no bases!")

        # 05 a - search for the line beginning with "    name: " or "options:". If options, all bases are accounted for and we are done
        base_counter = -1
        while(True):
            line = file_handle.readline()
            if line.startswith(BASES_END_ID):
                break 
            if line.startswith(BASE_NAME_ID):
                base_name = line[len(BASE_NAME_ID):]
                base_counter = base_counter + 1
                new_base = read_base(file_handle, base_name, base_counter)
                
                # 05 f - add the base object to the savedata
                new_data.add_base(new_base)
        
        
    # final saveguard
    if not isinstance(new_data, savedata):
        raise ValueError("Could not properly create savedata object")
    
    # 06 - return the savedata object
    return new_data

##########################################################################################
# for testing
def main() -> None:
    data = read_file("testsave.sav")
    print(data.debug_savedata_to_string())    

if __name__ == "__main__":
    main()