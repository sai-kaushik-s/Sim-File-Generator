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
    # Gets the minimized expression, file name and initial wire count
    minExpr, fileName, wireCount = helpInput()

    # Open the file
    # If the file does not exist, create a new file
    fp = open(fileName, "w")

    # Simplify the NOT gates in the expression
    minExpr = simplifyNot(minExpr, fp)
    # Simplify the AND and OR gates in the expression
    minExpr, wireCount = helpSimplify(minExpr, wireCount, fp)

    # Close the file
    fp.close()

    # Rename the final output variable
    helpRename(fileName, minExpr)
