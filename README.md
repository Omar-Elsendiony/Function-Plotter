# Function-Plotter


# Functionality
## The desktop application is aimed to plot a function in 2-D plane with only one independent variable 'x'

### The *operators* that can be operated upon are (from the highest precedence to the lowest):
* exponentiation(^)
* multiplication(*)
* division(/)
* addition(+)
* subtraction(-)

**Note: The following does not circumvent using paranthesis to change precedence,the equation parsing adheres to the ordinary precedence rules**
#### The plotter ensures that the following:
* user input is valid and the input resembles a valid function
* The input boundaries are real numbers and the lower bound is less than upper bound

# Prerequisites
First install the requiried dependencies using the following commands:
* pip install pyside2
* pip install pytest
* pip install pytestqt


# How to run it
The main GUI is in the file named 'main' (That is where the program starts) , run the file and the GUI will open up
The logic behind parsing the equation is in the file named 'utility'

## How to run automated tests
The automated tests which utilize 'pytest' library are in the file 'test_main' , to run it type:
pytest <relative directory name> <test file name (optional)>:: <function name(optional)>


First, define the boundaries of the equation using xMin and xMax


You can alternate between previously entered equations just by clicking on the labels! This provides ease of access to the history of at most 4 previous equations

