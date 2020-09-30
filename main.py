from helperFunctions import *
from simplify import *

#    __  __                               _             __          __
#   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
#  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
# / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
# \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
#               /____/                        /____/
#


# Main driver function
if __name__ == '__main__':
    # Gets the minimized expression
    minExpr, fileName, wireCount = helpInput()

    fp = open(fileName, "w")

    minExpr = simplifyNot(minExpr, fp)
    minExpr, wireCount = helpSimplify(minExpr, wireCount, fp)

    fp.close()

    helpRename(fileName, minExpr)
