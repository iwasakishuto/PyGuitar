# coding: utf-8

__all__ = [
    "toRED", "toGREEN", "toYELLOW", "toBLUE", "toPURPLE", "toCYAN",
    "toWHITE", "toRETURN", "toACCENT", "toFLASH", "toRED_FLASH",
]

def make_2COLOR_funcs(color="BLUE"):
    code = {
        "BLACK"     : '\033[30m',
        "RED"       : '\033[31m',
        "GREEN"     : '\033[32m',
        "YELLOW"    : '\033[33m',
        "BLUE"      : '\033[34m',
        "PURPLE"    : '\033[35m',
        "CYAN"      : '\033[36m',
        "WHITE"     : '\033[37m',
        "RETURN"    : '\033[07m',    # 反転
        "ACCENT"    : '\033[01m',    # 強調
        "FLASH"     : '\033[05m',    # 点滅
        "RED_FLASH" : '\033[05;41m', # 赤背景+点滅
    }.get(color.upper())
    func = lambda x: f"{code}{x}\033[0m"
    return func

toRED       = make_COLOR_funcs("RED")
toGREEN     = make_COLOR_funcs("GREEN")
toYELLOW    = make_COLOR_funcs("YELLOW")
toBLUE      = make_COLOR_funcs("BLUE")
toPURPLE    = make_COLOR_funcs("PURPLE")
toCYAN      = make_COLOR_funcs("CYAN")
toWHITE     = make_COLOR_funcs("WHITE")
toRETURN    = make_COLOR_funcs("RETURN")    # 反転
toACCENT    = make_COLOR_funcs("ACCENT")    # 強調
toFLASH     = make_COLOR_funcs("FLASH")     # 点滅
toRED_FLASH = make_COLOR_funcs("RED_FLASH") # 赤背景+点滅
