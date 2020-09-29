from simGates import *

#    __  __                               _             __          __
#   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
#  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
# / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
# \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
#               /____/                        /____/
#


def simplifyNot(exprNot, fp):
    varDone = set()
    for it in range(len(exprNot)):
        if exprNot[it] == "~":
            it1 = it + 1
            if exprNot[it1] not in varDone:
                varDone.add(exprNot[it1])
            else:
                continue
            wr = notGate(exprNot[it1])
            fp.write(wr)

    exprNot = exprNot.replace("~", "n")
    return exprNot


def simplifyAnd(exprAnd, wcAnd, fpAnd):
    return simplifyFun(exprAnd, "&", wcAnd, fpAnd)


def simplifyOr(exprOr, wcOr, fpOr):
    return simplifyFun(exprOr, "|", wcOr, fpOr)


def simplifyFun(expr, symbol, wc, fp):
    a1 = ""
    b1 = ""
    it = expr.find(symbol)
    while it != -1:
        temp = it - 1
        while True:
            if expr[temp] == "(" or expr[temp] == symbol:
                break
            a1 = expr[temp] + a1
            temp -= 1
        temp = it + 1
        while True:
            if expr[temp] == ")" or expr[temp] == symbol:
                break
            b1 = b1 + expr[temp]
            temp += 1
        wr = ""
        if symbol == "&":
            wr = andGate(a1, b1, wc)
        elif symbol == "|":
            wr = orGate(a1, b1, wc)
        wc += 2
        rep = a1 + symbol + b1
        out = "n" + str(wc)
        wc += 1
        fp.write(wr)
        expr = expr.replace(rep, out)
        a1 = ""
        b1 = ""
        it = expr.find(symbol)
    return expr, wc
