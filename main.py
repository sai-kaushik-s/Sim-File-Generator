from helperFunctions import *
from simplify import *

if __name__ == '__main__':
    minExpr, fileName, wireCount = helpInput()

    fp = open(fileName, "w")

    minExpr = simplifyNot(minExpr, fp)
    minExpr, wireCount = helpSimplify(minExpr, wireCount, fp)

    fp.close()

    helpRename(fileName, minExpr)