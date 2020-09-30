from simGates import *

#    __  __                               _             __          __
#   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
#  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
# / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
# \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
#               /____/                        /____/
#
#


# A function to add the NOT gate entries to the sim file and reduce the NOT gates
def simplifyNot(exprNot, fp):
    # Initialize a set for variables added
    varDone = set()
    # For each index of exprNot
    for it in range(len(exprNot)):
        # If ~ is found
        if exprNot[it] == "~":
            it1 = it + 1
            # If the character is not in the variables added
            if exprNot[it1] not in varDone:
                # Add to the set
                varDone.add(exprNot[it1])
            # If the character is in the variables added
            else:
                # Continue the loop
                continue
            # Get the entry of exprNot[it] in the sim file
            wr = notGate(exprNot[it1])
            # Write the entry in the file
            fp.write(wr)
    # Replace the ~ with n
    exprNot = exprNot.replace("~", "n")
    # Return the modified expression
    return exprNot


# A function to add the AND gate entries to the sim file and reduce the AND gates
def simplifyAnd(exprAnd, wcAnd, fpAnd):
    # Return the modified expression
    return simplifyFun(exprAnd, "&", wcAnd, fpAnd)


# A function to add the OR gate entries to the sim file and reduce the OR gates
def simplifyOr(exprOr, wcOr, fpOr):
    # Return the modified expression
    return simplifyFun(exprOr, "|", wcOr, fpOr)


# A function to simplify the AND and OR gates
def simplifyFun(expr, symbol, wc, fp):
    # Initialize empty strings
    a1 = ""
    b1 = ""
    # Get the index of the first symbol
    it = expr.find(symbol)
    # While the symbol exists in the expression
    while it != -1:
        # Go to the previous index of the symbol
        temp = it - 1
        # Run an infinite loop
        while True:
            # If the character is the symbol or (
            if expr[temp] == "(" or expr[temp] == symbol:
                # Break the loop
                break
            # Concat the character to a1
            a1 = expr[temp] + a1
            # Decrement temp
            temp -= 1
            # If temp under flows
            if temp < 0:
                # Break the loop
                break
        # Go to the next index of the symbol
        temp = it + 1
        # Run an infinite loop
        while True:
            # If the character is the symbol or )
            if expr[temp] == ")" or expr[temp] == symbol:
                # Break the loop
                break
            # Concat the character to b1
            b1 = b1 + expr[temp]
            # Decrement temp
            temp += 1
            # If temp over flows
            if temp >= len(expr):
                # Break the loop
                break
        wr = ""
        # If the symbol is &
        if symbol == "&":
            # Get the sim file entry for AND gate
            wr = andGate(a1, b1, wc)
        # If the symbol is |
        elif symbol == "|":
            # Get the sim file entry for OR gate
            wr = orGate(a1, b1, wc)
        wc += 2
        # Replace a1 & b1 or a1 | b1 with its new output
        rep = a1 + symbol + b1
        out = "n" + str(wc)
        wc += 1
        # Write the entry in the file
        fp.write(wr)
        expr = expr.replace(rep, out)
        # Reset the strings
        a1 = ""
        b1 = ""
        # Get the index of the next symbol
        it = expr.find(symbol)
    # Return the minimized expression and the wire count
    return expr, wc
