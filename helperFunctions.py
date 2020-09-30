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


def helpInput():
    print("\033[0;36m\nAND Gate:\t&\nOR Gate:\t|\nNOT Gate:\t~\nXOR Gate:\t^\nXNOR Gate:\t~^\nNAND Gate:\t~&\nNOR "
          "Gate:\t~|\n")
    expr = input("\033[0;34mEnter the expression: ")
    expr = expr.replace(" ", "")
    fileName = expr + ".sim"
    expr = helpComplexGates(expr)
    minExpr = str(simplify(expr))
    minExpr = minExpr.replace(" ", "")
    os.chdir("Circuits")
    wireCount = 0
    print("\033[0;31m\nThe simplified expression: y = %s" % minExpr)
    print("\033[0;32m\nThe satisfiable values are (X indicates that the variable can hold either 0 or 1): \033[0;33m")
    helpSolutions(minExpr)
    return minExpr, fileName, wireCount


def helpSimplify(minExpr, wireCount, fp):
    if minExpr.find(")|") != -1 or minExpr.find("|(") != -1:
        minExpr, wireCount = helpAnd(minExpr, wireCount, fp)
        minExpr = "(" + minExpr + ")"
        minExpr, wireCount = helpOr(minExpr, wireCount, fp)
    elif minExpr.find(")&") != -1 or minExpr.find("&(") != -1:
        minExpr, wireCount = helpOr(minExpr, wireCount, fp)
        minExpr = "(" + minExpr + ")"
        minExpr, wireCount = helpAnd(minExpr, wireCount, fp)
    elif minExpr.find("|") != -1:
        minExpr = "(" + minExpr + ")"
        minExpr, wireCount = helpOr(minExpr, wireCount, fp)
    elif minExpr.find("&") != -1:
        minExpr = "(" + minExpr + ")"
        minExpr, wireCount = helpAnd(minExpr, wireCount, fp)
    return minExpr, wireCount


def helpAnd(exprAnd, wireCount, fp):
    f1m, wireCount1 = simplifyAnd(exprAnd, wireCount, fp)
    f1m, wireCount = helpGate(f1m, wireCount, wireCount1)
    return f1m, wireCount


def helpOr(exprOr, wireCount, fp):
    f1m, wireCount1 = simplifyOr(exprOr, wireCount, fp)
    f1m, wireCount = helpGate(f1m, wireCount, wireCount1)
    return f1m, wireCount


def helpComplexGates(expr):
    if expr.find("~^") != -1:
        expr = helpXnor(expr)
    if expr.find("^") != -1:
        expr = helpXor(expr)
    if expr.find("~&") != -1:
        expr = helpNand(expr)
    if expr.find("~|") != -1:
        expr = helpNor(expr)
    return expr


def helpXor(expr):
    it = expr.find("^")
    while it != -1:
        a1, b1 = helpFindAB(expr, it, 1)
        old = a1 + "^" + b1
        rep = "(" + b1 + "&~" + a1 + "|" + a1 + "&~" + b1 + ")"
        expr = expr.replace(old, rep)
        it = expr.find("^")
    return expr


def helpXnor(expr):
    it = expr.find("~^")
    while it != -1:
        a1, b1 = helpFindAB(expr, it, 2)
        old = a1 + "~^" + b1
        rep = "(" + a1 + "&" + b1 + "|~" + a1 + "&~" + b1 + ")"
        expr = expr.replace(old, rep)
        it = expr.find("~^")
    return expr


def helpNand(expr):
    it = expr.find("~&")
    while it != -1:
        a1, b1 = helpFindAB(expr, it, 2)
        old = a1 + "~&" + b1
        rep = "(~" + a1 + "|~" + b1 + ")"
        expr = expr.replace(old, rep)
        it = expr.find("~&")
    return expr


def helpNor(expr):
    it = expr.find("~|")
    while it != -1:
        a1, b1 = helpFindAB(expr, it, 2)
        old = a1 + "~|" + b1
        rep = "(~" + a1 + "&~" + b1 + ")"
        expr = expr.replace(old, rep)
        it = expr.find("~|")
    return expr


def helpFindAB(expr, it, inc):
    temp = it - 1
    a1 = ""
    count = 0
    if expr[temp] == ")":
        count += 1
        a1 = ")" + a1
        while count != 0:
            temp -= 1
            if temp < 0:
                break
            if expr[temp] == ")":
                count += 1
            if expr[temp] == "(":
                count -= 1
            a1 = expr[temp] + a1
        if temp != 0:
            if expr[temp - 1] == "~":
                a1 = "~" + a1
    else:
        while True:
            if expr[temp] == "^" or expr[temp] == "&" or expr[temp] == "|" or expr[temp] == "(":
                break
            a1 = expr[temp] + a1
            temp -= 1
            if temp < 0:
                break
    temp = it + inc
    b1 = ""
    count = 0
    if expr[temp] == "~":
        b1 = b1 + "~"
        temp += 1
    if expr[temp] == "(":
        count += 1
        b1 = b1 + expr[temp]
        while count != 0:
            temp += 1
            if temp >= len(expr):
                break
            if expr[temp] == "(":
                count += 1
            if expr[temp] == ")":
                count -= 1
            b1 = b1 + expr[temp]
    else:
        while True:
            if expr[temp] == "^" or expr[temp] == "&" or expr[temp] == "|" or expr[temp] == ")":
                break
            if expr[temp] == "~":
                if expr[temp + 1] == "^" or expr[temp + 1] == "&" or expr[temp + 1] == "|" or expr[temp + 1] == ")":
                    break
            b1 = b1 + expr[temp]
            temp += 1
            if temp >= len(expr):
                break
    return a1, b1


def helpSolutions(expr):
    x = list(satisfiable(expr))
    variables = sorted(helpVariables(expr))
    x = x[0]
    it = x.find("|")
    b1 = ""
    i = 0
    while it != -1:
        i += 1
        print(str(i) + ")\t", end="")
        a1, b1 = helpFindAB(x, it, 1)
        helpSolutionFormat(a1, variables)
        x = x.replace("|", "", 1)
        it = x.find("|")
    i += 1
    print(str(i) + ")\t", end="")
    helpSolutionFormat(b1, variables)


def helpSolutionFormat(expr, variables):
    expr = expr.replace("&", " ")
    expr = expr.replace("(", "")
    expr = expr.replace(")", "")
    for it in variables:
        y = expr.find(it)
        if y == -1:
            print(it + " = X", end="; ")
        else:
            if expr[y - 1] == "~":
                print(it + " = 0", end="; ")
            else:
                print(it + " = 1", end="; ")
    print("", end="\n")


def helpGate(f1m, wireCount, wireCount1):
    wireCount += wireCount1
    f1m = f1m.replace("(", "")
    f1m = f1m.replace(")", "")
    return f1m, wireCount


def helpVariables(expr):
    variables = set()
    for it in expr:
        if it.isalpha():
            variables.add(it)
    return variables


def helpRename(fileName, expr):
    with open(fileName, "r") as fp:
        fileData = fp.read()
    fileData = fileData.replace(expr, "y")
    with open(fileName, "w") as fp:
        fp.write(fileData)
    print("\033[0;35m\nThe .sim file is saved as '%s' in the directory 'Circuits/'" % fileName)
