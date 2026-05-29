from io import TextIOWrapper

from .constants import *
from .savedata import savedata
# from .bases import base
# from .soldier import soldier

# no need for a class, do this data driven
# the actual save data will be maintained and provided be the main program
# process is analog to the reader function, see comment in reader.py
# but this time save lines we discarded in the reader and build the lines we were
# reading ourselves.

# There is virtually no error checking in this file since all input comes from already
# checked and therefore trusted sources inside the main program, unless the savefile
# has been modified and corrputed since reading it in the last time. In that case, screw
# the user.

def write_soldier(file_handle : TextIOWrapper, data : savedata) -> str:        
    # which soldier are we processing?
    line_buffer = file_handle.readline()
    soldier_id = int(line_buffer[len(SOLDIER_ID_ID):])
    current_soldier = data.get_soldier_by_id(soldier_id)
    if not current_soldier:
        raise ValueError("Something went from fetching a soldier for writing")
    
    # Construct the id and name lines
    soldier_string = SOLDIER_ID_ID + str(current_soldier.id) + "\n"
    file_handle.readline() # to progress the input line past the soldier name
    soldier_string = soldier_string + SOLDIER_NAME_ID + current_soldier.name + "\n"

    # progress to initial stats
    while(line_buffer != SOLDIER_INITIAL_STATS_ID):
        line_buffer = file_handle.readline()
        soldier_string = soldier_string + line_buffer
    
    # SOLDIER_INITIAL_STATS_ID was last written, next 10 lines are the initial stats
    # but in wring order in memory for some reason
    for _ in range(10):
        line_buffer = file_handle.readline() 
        stat = line_buffer.split(SOLDIER_STAT_SUFFIX)[0].strip()
        soldier_string = (soldier_string + SOLDIER_STAT_PREFIX + stat + SOLDIER_STAT_SUFFIX
                           + str(current_soldier.stats[stat][OX_BASE]) + "\n")    

    # progress to current stats
    while(line_buffer != SOLDIER_CURRENT_STATS_ID):
        line_buffer = file_handle.readline()
        soldier_string = soldier_string + line_buffer
        
    # SOLDIER_CURRENT_STATS_ID was last written, next 10 lines are the current stats
    # but in wring order in memory for some reason
    for _ in range(10):
        line_buffer = file_handle.readline() 
        stat = line_buffer.split(SOLDIER_STAT_SUFFIX)[0].strip()
        soldier_string = (soldier_string + SOLDIER_STAT_PREFIX + stat + SOLDIER_STAT_SUFFIX
                           + str(current_soldier.stats[stat][OX_CURRENT]) + "\n") 

    # the rest of the soldier should be processed by write_base while it's looking for the 
    # next base / end of bases
    
    return soldier_string

def write_base(file_handle: TextIOWrapper, data : savedata, name : str) -> str:
    # we get name of the base from the caller
    # this is only here and not in write_savefile because in my mind it belongs together
    # but we already read the line
    base_string = BASE_NAME_ID + name + "\n"

    # Copy everything until the soldier block starts
    line_buffer = file_handle.readline()
    while (not line_buffer.startswith(SOLDIER_BLOCK_START_ID)):
        base_string = base_string + line_buffer
        line_buffer = file_handle.readline()
    # SOLDIER_BLOCK_START_ID line also needs to be copied
    base_string = base_string + line_buffer

    # Check each line for 
    # "      - type: STR_SOLDIER" : pass over the the read_soldier_function
    # "    crafts:" all soldiers accounted for, rest of the base will be handled by read_savefile
    #               while it's looking for the next base or the end of the bases section
    while(True):
        line_buffer = file_handle.readline()
        if(line_buffer.startswith(SOLDIER_BLOCK_END_ID)):
            base_string = base_string + line_buffer
            break
        if(line_buffer.startswith(SOLDIER_START_ID)):
            base_string = base_string + line_buffer
            base_string = base_string + write_soldier(file_handle, data)
            continue
        base_string = base_string + line_buffer
        

    return base_string

def write_savefile(filename_input : str, data : savedata, filename_output : str) -> bool:
    so_far = "" # build the savefile into this
    line_buffer = ""
    with open(filename_input, 'r') as file_handle:
        # Copy over data until we hit the "funds" line
        while(not line_buffer.startswith(FUNDS_ID)):
            line_buffer = file_handle.readline()
            so_far = so_far + line_buffer

        # We habe written the "funds" line, the next line needs to be constructed and the input discarded
        file_handle.readline()
        so_far = so_far + FUNDS_PREFIX + str(data.get_credits()) + "\n"

        # Copy over data until and including "bases:"
        while(not line_buffer.startswith(BASES_START_ID)):
            line_buffer = file_handle.readline()
            so_far = so_far + line_buffer

        # new bases beginn with the BASE_START_ID, end of the bases block with BASE_END_ID
        # look for these, construct a base or continue onwards
        # we can then actually contine until EOF
        while(True):
            line_buffer = file_handle.readline()
            if line_buffer.startswith(BASE_NAME_ID):
                # create new base
                base_name = line_buffer[len(BASE_NAME_ID):].strip()
                so_far = so_far + write_base(file_handle, data, base_name)
                continue
            if line_buffer.startswith(BASES_END_ID):
                so_far = so_far + line_buffer
                break
            so_far = so_far + line_buffer

        # seperate loop to avoid unnecessary if-evaluations
        while(line_buffer != ""):
            line_buffer = file_handle.readline()
            so_far = so_far +  line_buffer

    # write out the result
    try:
        with open(filename_output, "w") as out:
            out.write(so_far)
    except Exception:
        # Only way this should fail is if we don't hace write permissions for the file,
        # notify the user from the main program
        return False
    
    return True
