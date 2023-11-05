def colored(seq):
    bcolors = {
        "A": "\033[92m",
        "C": "\033[94m",
        "G": "\033[93m",
        "T": "\033[91m",
        "U": "\033[91m",
        "reset": "\033[0;0m"
    }
    tmpstr = ""
    for nuc in seq:
        if nuc in bcolors:
            tmpstr += bcolors[nuc] + nuc
        else:
            tmpstr += bcolors["reset"] + nuc
    return tmpstr + "\033[0;0m"