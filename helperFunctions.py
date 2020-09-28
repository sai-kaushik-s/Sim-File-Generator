import os

from sympy import *

from simplify import simplifyAnd, simplifyOr


def helpInput():
    print("AND Gate:\t&\nOR Gate:\t|\nNOT Gate:\t~\nXOR Gate:\t^\nXNOR Gate:\t~^\nNAND Gate:\t~&\nNOR Gate:\t~|\n")
    expr = input("Enter the expression: ")
    expr = expr.replace(" ", "")
    fileName = expr + ".sim"
    expr = helpComplexGates(expr)
    minExpr = str(simplify(expr))
    minExpr = minExpr.replace(" ", "")
    os.chdir("Circuits")
    wireCount = 0
    print("The simplified expression: y = %s" % minExpr)
    print("The .sim file is saved as '%s' in the directory 'Circuits/'" % fileName)
    print('The satisfiable values are: ')
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
    while temp > -1:
        if expr[temp] == ")":
            count += 1
        if expr[temp] == "(":
            count -= 1
            if count <= 0:
                break
        if count == 0:
            if expr[temp] == "^" or expr[temp] == "&" or expr[temp] == "|":
                break
        a1 = expr[temp] + a1
        temp -= 1
    if a1.find(")") != -1:
        a1 = "(" + a1
    temp = it + inc
    b1 = ""
    count = 0
    while temp < len(expr):
        if expr[temp] == "(":
            count += 1
        if expr[temp] == ")":
            count -= 1
            if count <= 0:
                break
        if expr[temp] == "~":
            if expr[temp + 1] == "^" or expr[temp + 1] == "&" or expr[temp + 1] == "|" or expr[temp + 1] == ")":
                break
        if count == 0:
            if expr[temp] == "^" or expr[temp] == "&" or expr[temp] == "|":
                break
        b1 = b1 + expr[temp]
        temp += 1
    if b1.find("(") != -1:
        b1 = b1 + ")"
    return a1, b1


def helpSolutions(expr):
    x = list(satisfiable(expr))
    x = x[0]
    it = x.find("|")
    b1 = ""
    while it != -1:
        a1, b1 = helpFindAB(x, it, 1)
        print(a1)
        x = x.replace("|", "", 1)
        it = x.find("|")
    print(b1)


def helpGate(f1m, wireCount, wireCount1):
    wireCount += wireCount1
    f1m = f1m.replace("(", "")
    f1m = f1m.replace(")", "")
    return f1m, wireCount


def helpRename(fileName, expr):
    with open(fileName, "r") as fp:
        fileData = fp.read()
    fileData = fileData.replace(expr, "y")
    with open(fileName, "w") as fp:
        fp.write(fileData)
