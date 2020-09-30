#    __  __                               _             __          __
#   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
#  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
# / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
# \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
#               /____/                        /____/
#


# A function that gets the sim file entry for a NOT gate
def notGate(va):
    # Entry for a NOT gate
    x1 = "p in vdd nin 2 4\nn in nin gnd 2 4\n\n"
    # Change the inputs to specified variable
    y1 = x1.replace("in", va)
    # Return the modified entry
    return y1


# A function that gets the sim file entry for a AND gate
def andGate(in1, in2, w1):
    # Entry for a AND gate
    xa = "p in1 vdd wire2 2 4\np in2 vdd wire2 2 4\nn in1 wire2 wire1 2 4\nn in2 wire1 gnd 2 4\n\np wire2 vdd out 2 " \
         "4\nn wire2 gnd out 2 4\n\n"
    # Change the inputs to specified variable
    ya = replaceInp(xa, in1, in2, w1)
    # Return the modified entry
    return ya


# A function that gets the sim file entry for a OR gate
def orGate(in1, in2, w1):
    # Entry for a OR gate
    xo = "p in1 vdd wire1 2 4\np in2 wire1 wire2 2 4\nn in1 wire2 gnd 2 4\nn in2 wire2 gnd 2 4\n\np wire2 vdd out 2 " \
         "4\nn wire2 gnd out 2 4\n\n"
    # Change the inputs to specified variable
    yo = replaceInp(xo, in1, in2, w1)
    # Return the modified entry
    return yo


# A function to modify the inputs to specified variables
def replaceInp(x, in1, in2, w1):
    y = x.replace("in1", in1)
    y = y.replace("in2", in2)
    n1 = "n" + str(w1)
    y = y.replace("wire1", n1)
    n2 = "n" + str(w1 + 1)
    y = y.replace("wire2", n2)
    ou = "n" + str(w1 + 2)
    y = y.replace("out", ou)
    # Return the modified entry
    return y
