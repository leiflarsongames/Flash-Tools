from enum import Enum
from dataclasses import dataclass

# Please see README.md for disclaimer on use.

PRECISION:int = 4
'''precision of final output, in base-10 places.'''

class ColorFormat(Enum):
    sRGB = "sRGB"
    internalForRL = "internal_rl_channel"

@dataclass
class ColorVector:
    '''
    Contains each RGB channel as a float, alongside the format those channels are represented in.

    Should they need to be within the interval [0, 1] at any particular step, call `as_clamped` to get a copy which abides by this restriction.
    '''
    R:float
    G:float
    B:float
    format:ColorFormat

    def as_clamped(self):
        '''
        Returns a copy whose color channels are guaranteed to each be within the interval [0, 1].
        
        Values are clamped to the nearest endpoint if they are not.
        '''
        return ColorVector(
            min(max(self.R, 0.0), 1.0),
            min(max(self.G, 0.0), 1.0),
            min(max(self.B, 0.0), 1.0),
            self.format
        )

    @classmethod
    def from_channels(cls, R:float, G:float, B:float, format:ColorFormat=ColorFormat.sRGB) -> ColorVector:
        return ColorVector(R, G, B, format)

    @classmethod
    def from_hexcode(cls, hexcode:str, format:ColorFormat=ColorFormat.sRGB) -> ColorVector:
        hexcode = hexcode.replace("#","").replace("0x","")
        vec = ColorVector(
            R=_8bitRGB_to_sRGB_channel(int(hexcode[0:2],16)), 
            G=_8bitRGB_to_sRGB_channel(int(hexcode[2:4],16)), 
            B=_8bitRGB_to_sRGB_channel(int(hexcode[4:6],16)),
            format=ColorFormat.sRGB
        )

        # return vec
        if vec.format is ColorFormat.sRGB:
            return vec
        else:
            return vec.as_internal_for_relative_luminance()

    def as_internal_for_relative_luminance(self) -> ColorVector:
        if self.format is ColorFormat.sRGB:
            return ColorVector(
                R=_sRGB_to_internal_rl_channel(self.R),
                G=_sRGB_to_internal_rl_channel(self.G),
                B=_sRGB_to_internal_rl_channel(self.B),
                format=ColorFormat.internalForRL
                )
        else:
            return self

    def get_relative_luminance(self) -> float:
        return relative_luminance(self.R, self.G, self.B)
    
    def __add__(self, other:ColorVector):
        if (type(other) is not ColorVector):
            raise TypeError(f"ColorVector.__add__ ... Cannot add a ColorVector to a value of a different type ... type(self) = {type(self)} and type(other) = {type(other)}.")
        if (self.format != other.format):
            if self.format is ColorFormat.internalForRL:
                other = other.as_internal_for_relative_luminance()
            else:
                raise ValueError(f"ColorVector.__add__ ... cannot add when self.format = {self.format} and other.format = {other.format}.")
            
        return ColorVector(
            self.R + other.R, 
            self.G + other.G, 
            self.B + other.B, 
            self.format
            )

    def __sub__(self, other:ColorVector):
        if (type(other) is not ColorVector):
            raise TypeError(f"ColorVector.__sub__ ... Cannot subtract a value of a different type from a ColorVector ... type(self) = {type(self)} and type(other) = {type(other)}.")
        if (self.format != other.format):
            if self.format is ColorFormat.internalForRL:
                other = other.as_internal_for_relative_luminance()
            else:
                raise ValueError(f"ColorVector.__sub__ ... cannot subtract when self.format = {self.format} and other.format = {other.format}.")
            
        return ColorVector(
            self.R - other.R, 
            self.G - other.G, 
            self.B - other.B, 
            self.format
            )
    
    def __mul__(self, other:float):
        if (type(other) is not float):
            raise TypeError(f"ColorVector.__mul__ ... Cannot multiply ColorVector by a non-float type ... type(other) = {type(other)}.")
        return ColorVector(
            self.R * other,
            self.G * other,
            self.B * other,
            self.format
        )
        



## BEHAVIOR FUNCTIONS

def relative_luminance(R_sRGB:float, G_sRGB:float, B_sRGB:float) -> float:
    '''based on the WCAG 2.2 definition of relative luminance. See https://www.w3.org/TR/WCAG22/#dfn-relative-luminance'''
    if not isinstance(R_sRGB, float):
        raise TypeError(f"relative_luminance ... R_sRGB (1st param, RED) must be a float w/n interval [0,1]. Got type={type(R_sRGB)} instead.")
    if not isinstance(G_sRGB, float):
        raise TypeError(f"relative_luminance ... G_sRGB (2nd param, GREEN) must be a float w/n interval [0,1]. Got type={type(G_sRGB)} instead.")
    if not isinstance(B_sRGB, float):
        raise TypeError(f"relative_luminance ... B_sRGB (3rd param, BLUE) must be a float w/n interval [0,1]. Got type={type(B_sRGB)} instead.")
    
    if R_sRGB < 0 or R_sRGB > 1:
        raise ValueError(f"relative_luminance ... R_sRGB (1st param, RED) must be a float w/n interval [0,1]. Got value={R_sRGB} instead.")
    if G_sRGB < 0 or G_sRGB > 1:
        raise ValueError(f"relative_luminance ... G_sRGB (2nd param, GREEN) must be a float w/n interval [0,1]. Got value={G_sRGB} instead.")
    if B_sRGB < 0 or B_sRGB > 1:
        raise ValueError(f"relative_luminance ... B_sRGB (3rd param, BLUE) must be a float w/n interval [0,1]. Got value={B_sRGB} instead.")
    
    R:float = _sRGB_to_internal_rl_channel(R_sRGB)
    G:float = _sRGB_to_internal_rl_channel(G_sRGB)
    B:float = _sRGB_to_internal_rl_channel(B_sRGB)

    L:float = 0.2126 * R + 0.7152 * G + 0.0722 * B

    return L

def contrast_ratio(L1:float, L2:float) -> float:
    '''
    The WCAG 2.2 contrast ratio.
    '''
    if L1 > L2:
        tmp = L1
        L1 = L2
        L2 = tmp
    # L1 is guaranteed to be no greater than L2.
    return (L2 + 0.05) / (L1 + 0.05)

# CHECKLISTS

def contrast_checklist(C1:ColorVector, C2:ColorVector):
    print(f"Contrast ratio: {round(contrast_ratio(C1.get_relative_luminance(), C2.get_relative_luminance()), PRECISION)}")
    print("TODO: print what standards are actually being met!")

def complete_flash_checklist(C1:ColorVector, C2:ColorVector):
    gen:bool = general_flash_threshold_checklist(C1, C2)
    red:bool = red_flash_checklist(C1, C2)
    if (not gen) or (not red):
        print(f"Result: [FAIL] ... general={_check(gen)}, red={_check(red)}")
    else:
        print(f"Result: [PASS] ... general={_check(gen)}, red={_check(red)}")

def general_flash_threshold_checklist(L1:float|ColorVector, L2:float|ColorVector) -> bool:
    '''
    Returns `False` if not compliant.
    '''
    if type(L1) is ColorVector:
        L1 = L1.get_relative_luminance()
    if type(L2) is ColorVector:
        L2 = L2.get_relative_luminance()
        
    if L1 > L2:
        tmp = L1
        L1 = L2
        L2 = tmp
    # L1 is guaranteed to be no greater than L2.

    print(f"General Flash Threshold ... to pass: one of the following criteria must get {_check(True)}")

    delt_lum:bool = (abs(L1 - L2) >= 0.1)
    '''delta luminance is at least threshold'''
    print(f"{_check(not delt_lum)} relative luminance difference = {round(abs(L1-L2)*100.0, PRECISION)}%  |  ({"IS AT LEAST 10%" if delt_lum else "does not change brightness enough to be of concern. (threshold is 'at least 10%')"})")
    dark_lum:bool = (min(L1,L2) < 0.80)
    '''darkest luminance is strictly below threshold'''
    print(f"{_check(not dark_lum)}      least relative luminance = {round(min(L1,L2)*100.0, PRECISION)}%  |  ({"IS BELOW 80%" if dark_lum else "does not become dark enough to be of concern. (threshold is 'below 80%')"})")
    
    if delt_lum and dark_lum:
        print("[FAIL] General flash threshold failed: both failure criteria were met.")
        return False
    elif delt_lum or dark_lum:
        print("[PASS] General flash threshold passed: only one failure criteria was present.")
        return True
    else:
        print("[PASS] General flash threshold passed: no failure criteria present.")
        return True

def red_flash_checklist(C1:ColorVector, C2:ColorVector) -> bool:
    '''
    returns whether the two colors would NOT be considered a red flash!

    see Note 3 under https://www.w3.org/TR/WCAG20/#general-thresholddef for the specification this tries to implement.
    '''
    ## IMPORTANT NOTE: per WCAG 2.0, this definition's RGBs must use the RGB internal to the "relative luminance" calculation.
    if C1.format is not ColorFormat.internalForRL:
        C1 = C1.as_internal_for_relative_luminance()
    if C2.format is not ColorFormat.internalForRL:
        C2 = C2.as_internal_for_relative_luminance()
    
    # TODO should the R, G, B be scaled by the factors actually used in the Luminance formula?
    
    C1_score:float = _safe_division(C1.R, C1.R + C1.G + C1.B)
    C2_score:float = _safe_division(C2.R, C2.R + C2.G + C2.B)
    if (C1_score < 0.8 and C2_score < 0.8):
        print(f"[PASS] Red flash criteria passed: Neither color is red enough to count as a red flash.  |  (threshold is 'at least 80%', C1_score={C1_score*100.0}%, C2_score={C2_score*100.0}%)")
        return True
    else:
        print(f"       The flash has at least one value that is red enough to fail step (1/2)  |  (threshold is 'at least 80%', C1_score={C1_score*100.0}%, C2_score={C2_score*100.0}%)")
    
    
    C1_weird_score:float = max(0.0, C1.R - C1.G - C1.B) * 320.0
    C2_weird_score:float = max(0.0, C2.R - C2.G - C2.B) * 320.0
    delta_weird_score:float = abs(C1_weird_score - C2_weird_score)
    if (delta_weird_score > 20):
        print(f"[FAIL] Does not comply. The flash fails on step (2/2)'s [delta of (R-G-B)x320 > 20] criteria  |  (threshold was '20 or less', delta was = {delta_weird_score})")
        return False
    else:
        print(f"[PASS] Passed on step (2/2)'s criteria's [delta of (R-G-B)x320 > 20] criteria  |  (threshold was '20 or less', delta was = {delta_weird_score})")
        return True

## HELPER FUNCTIONS

def _check(value:bool):
    return "☑" if value else "☒"

def _8bitRGB_to_sRGB_channel(channel:int) -> float:
    if not isinstance(channel, int):
        raise TypeError(f"_8bitRGB_to_sRGB_channel ... channel must be an integer w/n interval [0, 255]. Got type={type(channel)} instead.")

    if channel < 0 or channel > 255:
        raise ValueError(f"_8bitRGB_to_sRGB_channel ... channel must be an integer w/n interval [0, 255]. Got value={channel} instead.")

    return channel / 255.0


def _sRGB_to_internal_rl_channel(sRGB_value:float) -> float:
    '''used internally by `relative_luminance`.'''
    if sRGB_value <= 0.04045:   # Based on WCAG 2.2 (changed from 0.03928, which would have been used prior to May 2021.)
        return sRGB_value/12.92
    else:
        return pow((sRGB_value+0.055)/1.055, 2.4)

def _safe_division(dividend, divisor) -> float:
    if divisor == 0:
        return 0.0
    else:
        return dividend / float(divisor)

    ## pending a copy of ISO 9241-391:2016 to update to WCAG 2.2 specification! (if anyone wants to cough up 100 Swiss francs for the purpose (~123 USD), let me know.)"
    ## TODO this is crazy important! https://www.w3.org/TR/WCAG22/#dfn-general-flash-and-red-flash-thresholds
    ## TODO this is an associated document: https://www.iso.org/standard/56350.html    