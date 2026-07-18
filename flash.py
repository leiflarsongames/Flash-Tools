from enum import Enum
from time import sleep

from lum import *
from lum_manual_verify import *

# Please see README.md for disclaimer on use.

DATA_POINT_COUNT:int = 100  # integer on the interval [2, inf)

class Mode(Enum):
    CHECKING_CONTRAST = 1
    CHECKING_FLASH = 2
    VERIFYING_FEATURES = 3

def main():
    running:bool = True
    show_help_dialogue()

    # run program
    while(running):

        mode:Mode|None = None
        while(running and not mode):

            # prompt user for mode
            print("[C] Contrast only")
            print("[F] Flash criteria only")
            print("[V] Verify basic features")
            given:str = input("? ")

            if len(given) > 0:
                if given[0] in ['c', 'C', '1']:
                    mode = Mode.CHECKING_CONTRAST
                elif given[0] in ['f', 'F', '2']:
                    mode = Mode.CHECKING_FLASH
                elif given[0] in ['v', 'V', '3']:
                    mode = Mode.VERIFYING_FEATURES
                elif is_exit_cmd(given):
                    running = False     # escapes program
                elif is_restart_cmd(given):
                    pass                # includes help dialogue, relying on side-effects of check.

        
        while(running and mode):

            # prompt user for colors to compare
            code_1:str = input("color code (C1) = ")
            if (is_restart_cmd(code_1)):
                mode = None
            elif(is_exit_cmd(code_1)):
                running = False

            code_2:str = input("color code (C2) = ")
            if (is_restart_cmd(code_2)):
                mode = None
            elif(is_exit_cmd(code_2)):
                running = False

            if running and mode:
                C1:ColorVector = ColorVector.from_hexcode(code_1)
                C2:ColorVector = ColorVector.from_hexcode(code_2)

                # main behavior
                if mode == Mode.CHECKING_FLASH:
                    complete_flash_checklist(C1, C2)
                elif mode == Mode.CHECKING_CONTRAST:
                    contrast_checklist(C1, C2)
                elif mode == Mode.VERIFYING_FEATURES:
                    verify_feature_routine(C1, C2, DATA_POINT_COUNT)

    print("Terminated by user command.")
    sleep(1)


# NOTE: do not occlude valid hexcode values in the following functions 
# (e.g., including any letter from `a-f` as a shorthand would break legitimate color code inputs)

def is_exit_cmd(cmd:str) -> bool:
    return len(cmd) > 0 and (
            cmd[0].lower() == "q"
            or cmd.lower() in ["quit", "exit"]
            )

def is_restart_cmd(cmd:str) -> bool:
    if (len(cmd) <= 0):
        return False
    if (cmd[0].lower() == "h"):
        show_help_dialogue()
        input("press [Enter] to proceed.")
        return True
    return (cmd[0].lower() == "r")

def show_help_dialogue() -> bool:
    print()
    print("Type \"q\" or \"quit\" to end the program.")
    print("Type \"r\" or \"restart\" to restart the program.")
    print("Type \"h\" or \"help\" to show this dialogue again.")
    print()


main()