MAX_WIDTH:int  = 341
MAX_HEIGHT:int = 256

PRECISION:int = 4

# Please see README.md for disclaimer on use.

def fov_routine(max_width:int=MAX_WIDTH, max_height:int=MAX_HEIGHT):
    print("Your resolution should be set to 1024 x 768 for this test.")
    print("Get the object's actual CSS pixel size using inspect element (or failing that, use the planimeter extension to estimate it).")
    print("Copy the dimensions into the terminal below.")
    print()
    print(f"We are to see what proportion of a {max_width} x {max_height} area your selection will take up.")
    if MAX_WIDTH != max_width or MAX_HEIGHT != max_height:
        print()
        print(f"IMPORTANT: max_width and max_height have been changed to [{max_width} x {max_height}] ... specification suggests [{MAX_WIDTH} x {MAX_HEIGHT}] as safe!")
        print(f"[PROCEED ONLY IF YOU KNOW WHAT YOU'RE DOING!]")
    print()
    while(True):
        width:float  = _prompt_for_dim(" width = ")
        height:float = _prompt_for_dim("height = ")

        print()
        print(f"got input = [{width} x {height}] in CSS pixels")

        # FOV checklist
        width = min(max_width, width)
        height = min(max_height, height)
        print(f"(clamped to [{width} x {height}] in CSS pixels)")
        print()
        proportion_of_area:float = width * height / float(max_width * max_height)
        print(f"Takes up {round(proportion_of_area*100.0, PRECISION)}% of the nominal 10 degree viewing angle.")
        if proportion_of_area >= 0.25:
            print("[CAUTION] is at least 25% threshold! Failure on color criteria will indicate a violation of the \"2.3.1 Three Flashes\" criteria. Please proceed with a color check on this element.")
        else:
            print("[PASS] does NOT cross 25% threshold!")    

def _prompt_for_dim(text:str) -> float:
    dim:int|None = None
    while dim is None:
        given:str = input(text)
        try:
            dim = float(given)
            if dim <= 0:
                print(f"Dimension must be a strictly positive value, not \"{given}\".")
                dim = None
        except :
            print(f"\"{given}\" is not convertible to a valid value.")
    return dim

fov_routine()