import os

from sympy import *

from simplify import simplifyAnd, simplifyOr

#    __  __                               _             __          __
#   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
#  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
# / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
# \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
#               /____/                        /____/
#


# A function to help get inputs and simply the expression
def helpInput():
    # Print the instructions
    print("\033[0;36m\nAND Gate:\t&\nOR Gate:\t|\nNOT Gate:\t~\nXOR Gate:\t^\nXNOR Gate:\t~^\nNAND Gate:\t~&\nNOR "
          "Gate:\t~|\n")
    # Getting the expression from the user
    expr = input("\033[0;34mEnter the expression: ")
    expr = expr.replace(" ", "")
    # Create the file name as the expression
    fileName = expr + ".sim"
    # Simplify the complex gates ie. XOR gate, XNOR gate, NAND gate, NOR gate
    expr = helpComplexGates(expr)
    # Use the simplify function to simplify the expression
    minExpr = str(simplify(expr))
    minExpr = minExpr.replace(" ", "")
    # Change the working directory to "Circuits"
    os.chdir("Circuits")
    # Initialize the wire count to 0
    wireCount = 0
    # Print the simplified expression
    print("\033[0;31m\nThe simplified expression: y = %s" % minExpr)
    # Print the satisfiable inputs
    print("\033[0;32m\nThe satisfiable values are (X indicates that the variable can hold either 0 or 1): \033[0;33m")
    helpSolutions(minExpr)
    # Return the minimized expression, file name, wire count
    return minExpr, fileName, wireCount


# A function to help simplify the expression
# The simply function of the sympy package reduces the equation so that it consists of only AND, NOT and OR gates
# The generalized simplified expressions are (~a&b&...)|(c&~d&...)|... or (~a|b|...)&(c|~d|...)&...
# or a|(c&~d&...)|... or b&(c|~d|...)&...
def helpSimplify(minExpr, wireCount, fp):
    # If the gate outside the brackets are |, then the gates within the brackets are &
    if minExpr.find(")|") != -1 or minExpr.find("|(") != -1:
        # Simplify the AND gates
        minExpr, wireCount = helpAnd(minExpr, wireCount, fp)
        minExpr = "(" + minExpr + ")"
        # Simplify the OR gates
        minExpr, wireCount = helpOr(minExpr, wireCount, fp)
    # If the gate outside the brackets are &, then the gates within the brackets are |
    elif minExpr.find(")&") != -1 or minExpr.find("&(") != -1:
        # Simplify the OR gates
        minExpr, wireCount = helpOr(minExpr, wireCount, fp)
        minExpr = "(" + minExpr + ")"
        # Simplify the AND gates
        minExpr, wireCount = helpAnd(minExpr, wireCount, fp)
    # If there is only one type of gate ie. |
    elif minExpr.find("|") != -1:
        minExpr = "(" + minExpr + ")"
        # Simplify the OR gates
        minExpr, wireCount = helpOr(minExpr, wireCount, fp)
    # If there is only one type of gate ie. &
    elif minExpr.find("&") != -1:
        minExpr = "(" + minExpr + ")"
        # Simplify the AND gates
        minExpr, wireCount = helpAnd(minExpr, wireCount, fp)
    # Return the minimized expression and the wire count
    return minExpr, wireCount


# Function to help simplify the AND Gates
def helpAnd(exprAnd, wireCount, fp):
    # Simplify the AND gates
    f1m, wireCount1 = simplifyAnd(exprAnd, wireCount, fp)
    # Update the minimized expression and the wire count
    f1m, wireCount = helpGate(f1m, wireCount, wireCount1)
    # Return the minimized expression and wire count
    return f1m, wireCount


# Function to help simplify the OR gates
def helpOr(exprOr, wireCount, fp):
    # Simplify the OR gates
    f1m, wireCount1 = simplifyOr(exprOr, wireCount, fp)
    # Update the minimized expression and the wire count
    f1m, wireCount = helpGate(f1m, wireCount, wireCount1)
    # Return the minimized expression and wire count
    return f1m, wireCount


# A function to help simplify the complex gates
def helpComplexGates(expr):
    # If there is a XNOR gate in the expression
    if expr.find("~^") != -1:
        # Reduce the XNOR gates to basic gates
        expr = helpXnor(expr)
    # If there is a XOR gate in the expression
    if expr.find("^") != -1:
        # Reduce the XOR gates to basic gates
        expr = helpXor(expr)
    # If there is a NAND gate in the expression
    if expr.find("~&") != -1:
        # Reduce the NAND gates to basic gates
        expr = helpNand(expr)
    # If there is a NOR gate in the expression
    if expr.find("~|") != -1:
        # Reduce the NOR gates to basic gates
        expr = helpNor(expr)
    # Return the expression in terms of basic gates
    return expr


# A function to help reduce XOR gates to basic gates
def helpXor(expr):
    # Get the index of the first XOR gates
    # find() returns -1, if the substring is not present
    it = expr.find("^")
    # While there exists a XOR gate, run the loop
    while it != -1:
        # Get the inputs of the XOR gates
        a1, b1 = helpFindAB(expr, it, 1)
        # Replace the XOR gate
        # a^b = ((~a&b)|(a&~b))
        old = a1 + "^" + b1
        rep = "(" + b1 + "&~" + a1 + "|" + a1 + "&~" + b1 + ")"
        expr = expr.replace(old, rep)
        # Get the index of the next XOR gate
        it = expr.find("^")
    # Return the expression
    return expr


# A function to help reduce XNOR gates to basic gates
def helpXnor(expr):
    # Get the index of the first XNOR gates
    # find() returns -1, if the substring is not present
    it = expr.find("~^")
    # While there exists a XNOR gate, run the loop
    while it != -1:
        # Get the inputs of the XNOR gates
        a1, b1 = helpFindAB(expr, it, 2)
        # Replace the XNOR gate
        # a~^b = ((a&b)|(~a&~b))
        old = a1 + "~^" + b1
        rep = "(" + a1 + "&" + b1 + "|~" + a1 + "&~" + b1 + ")"
        expr = expr.replace(old, rep)
        # Get the index of the next XNOR gate
        it = expr.find("~^")
    # Return the expression
    return expr


# A function to help reduce NAND gates to basic gates
def helpNand(expr):
    # Get the index of the first NAND gates
    # find() returns -1, if the substring is not present
    it = expr.find("~&")
    # While there exists a NAND gate, run the loop
    while it != -1:
        # Get the inputs of the NAND gates
        a1, b1 = helpFindAB(expr, it, 2)
        # Replace the NAND gate
        # a~&b = (~a|~b)
        old = a1 + "~&" + b1
        rep = "(~" + a1 + "|~" + b1 + ")"
        expr = expr.replace(old, rep)
        # Get the index of the next NAND gate
        it = expr.find("~&")
    # Return the expression
    return expr


# A function to help reduce NOR gates to basic gates
def helpNor(expr):
    # Get the index of the first NOR gates
    # find() returns -1, if the substring is not present
    it = expr.find("~|")
    # While there exists a NOR gate, run the loop
    while it != -1:
        # Get the inputs of the NOR gates
        a1, b1 = helpFindAB(expr, it, 2)
        # Replace the NOR gate
        # a~|b = (~a&~b)
        old = a1 + "~|" + b1
        rep = "(~" + a1 + "&~" + b1 + ")"
        expr = expr.replace(old, rep)
        # Get the index of the next NOR gate
        it = expr.find("~|")
    # Return the expression
    return expr


# A function to get the two inputs of a given gate
def helpFindAB(expr, it, inc):
    # Initialize empty strings
    a1 = ""
    b1 = ""
    # Go to previous index of the gate
    temp = it - 1
    # Initialize the count of ) brackets
    count = 0
    # If the character is )
    if expr[temp] == ")":
        # Increase the count of brackets
        count += 1
        # Add the bracket to the string
        a1 = ")" + a1
        # While the count of brackets is not zero
        while count != 0:
            # Decrement the index
            temp -= 1
            # If temp under flows
            if temp < 0:
                # Break the loop
                break
            # If the character is )
            if expr[temp] == ")":
                # Increment the count of brackets
                count += 1
            # If the character is (
            if expr[temp] == "(":
                # Decrement the count of brackets
                count -= 1
            # Concat the character to a1
            a1 = expr[temp] + a1
        # If temp is not under flowed
        if temp != 0:
            # If the character is ~
            if expr[temp - 1] == "~":
                # Concat ~ to a1
                a1 = "~" + a1
    # If the character is not )
    else:
        # Run an infinite loop
        while True:
            # If the character is any of |^&)
            if expr[temp] == "^" or expr[temp] == "&" or expr[temp] == "|" or expr[temp] == "(":
                # Break the loop
                break
            # Concat the character to 11
            a1 = expr[temp] + a1
            # Decrement temp
            temp -= 1
            # If temp under flows
            if temp < 0:
                # Break the loop
                break
    # Go to the next index of the gate
    # inc is two for XNOR, NAND, NOR, as its symbol is of length 2
    # inc is one for XOR, as its symbol is of length 1
    temp = it + inc
    # Initialize the count of brackets to 0
    count = 0
    # If the character is ~
    if expr[temp] == "~":
        # Concat ~ to b1
        b1 = b1 + "~"
        # Increment temp
        temp += 1
    # If the character is (
    if expr[temp] == "(":
        # Increment the count
        count += 1
        # Concat ( to b1
        b1 = b1 + expr[temp]
        # While count is not 0
        while count != 0:
            # Increment temp
            temp += 1
            # If temp over flows
            if temp >= len(expr):
                # Break the loop
                break
            # If the character is (
            if expr[temp] == "(":
                # Increment the count of brackets
                count += 1
            # If the character is )
            if expr[temp] == ")":
                # Decrement the count of brackets
                count -= 1
            # Concat the character to b1
            b1 = b1 + expr[temp]
    # If the character is not (
    else:
        # Run a infinite loop
        while True:
            # If the character is in ^&|)
            if expr[temp] == "^" or expr[temp] == "&" or expr[temp] == "|" or expr[temp] == ")":
                # Break the loop
                break
            # If the character is ~
            if expr[temp] == "~":
                # If ~ is a part of XNOR or NAND or NOR gate
                if expr[temp + 1] == "^" or expr[temp + 1] == "&" or expr[temp + 1] == "|" or expr[temp + 1] == ")":
                    # Break the loop
                    break
            # Concat the character to b1
            b1 = b1 + expr[temp]
            # Increment temp
            temp += 1
            # If the temp over flows
            if temp >= len(expr):
                # Break the loop
                break
    # Return the inputs of the gate
    return a1, b1


# A function to get the solution of the expression
def helpSolutions(expr):
    # Get the list of solutions from satisfiable function of sympy
    x = list(satisfiable(expr))
    # Sort the set of variables in the expression
    variables = sorted(helpVariables(expr))
    x = x[0]
    # Find the | in the solution set
    it = x.find("|")
    b1 = ""
    i = 0
    # While | is present in the expression
    while it != -1:
        i += 1
        print(str(i) + ")\t", end="")
        # Find A of the | gate
        a1, b1 = helpFindAB(x, it, 1)
        # Format the solution
        helpSolutionFormat(a1, variables)
        x = x.replace("|", "", 1)
        # Find the next |
        it = x.find("|")
    i += 1
    print(str(i) + ")\t", end="")
    # Format the B of the last gate
    helpSolutionFormat(b1, variables)


# A function to help format the solution
def helpSolutionFormat(expr, variables):
    expr = expr.replace("&", " ")
    expr = expr.replace("(", "")
    expr = expr.replace(")", "")
    # For each variable in the expression
    for it in variables:
        # Find the variable in the solution expression
        y = expr.find(it)
        # If the variable is not found, it can take 0 or 1 as input
        if y == -1:
            print(it + " = X", end="; ")
        # If the variable is found
        else:
            # If the variable follows a ~, it takes 0
            if expr[y - 1] == "~":
                print(it + " = 0", end="; ")
            # If the variable does not follow a ~, it takes 1
            else:
                print(it + " = 1", end="; ")
    print("", end="\n")


# A function to update the expression and wire count
def helpGate(f1m, wireCount, wireCount1):
    wireCount += wireCount1
    f1m = f1m.replace("(", "")
    f1m = f1m.replace(")", "")
    return f1m, wireCount


# A function to get the unique variables in a given expression
def helpVariables(expr):
    # initialize an empty set
    variables = set()
    # For each character in the expression
    for it in expr:
        # If the character is an alphabet
        if it.isalpha():
            # Add to the set
            variables.add(it)
    # Return the variables
    return variables


# A function to rename the output in the sim file
def helpRename(fileName, expr):
    # Open the file in read mode
    with open(fileName, "r") as fp:
        # Read the file
        fileData = fp.read()
    # Change the last wire to y
    fileData = fileData.replace(expr, "y")
    # Open the file in write mode
    with open(fileName, "w") as fp:
        # Write the modified text
        fp.write(fileData)
    print("\033[0;35m\nThe .sim file is saved as '%s' in the directory 'Circuits/'" % fileName)
