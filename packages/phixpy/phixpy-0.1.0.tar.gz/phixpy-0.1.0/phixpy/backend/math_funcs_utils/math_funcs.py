import math
import copy
from tabulate import tabulate
import os
import random
default_unit_in_degrees = True

t_uses = [
    ['S.N', 'FUNCTIONS', 'USE'],
    ['1', 'sin', 'get the sin value for the given theta'],
    ['2', 'cos', 'get the cos value for the given theta'],
    ['3', 'tan', 'get the tan value for the given theta'],
    ['4', 'cosec', 'get the cosec value for the given theta'],
    ['5', 'sec', 'get the sec value for the given theta'],
    ['6', 'cot', 'get the cot value for the given theta'],
    ['7', 'degrees2rad', 'convert the given in_degreesree value into radians'],
    ['8', 'rad2degrees', 'convert the given radians into in_degreesrees']
]

e_uses = [
    ['S.N', 'FUNCTIONS', 'USE'],
    ['1', 'pow', "raise the power of 'x' by 'pow'"],
    ['2', 'root', "find the root of number"],
    ['3', 'sqrt', 'find the square-root of number'],
    ['4', 'cbrt', 'find the cube-root of number'],
    ['5', 'sqr', 'find the square of number'],
    ['6', 'cube', 'find the cube of number'],
] 


author = 'rijuL dhungana'
__doc__ = f"""
A module that handles trignometric & indices' fuctions: based on 'math' module, a pre-built math module in python

C: @rijuL dhungana
------------------------------------------------------------------------------------------------------------------

USAGE:
------------------------------------------------------------------------------------------------------------------

I) Trigonometric Functions
{tabulate(t_uses, tablefmt='grid')}
__________________________________________________________________________________________________________________
__________________________________________________________________________________________________________________

II) Indices & Exponents
{tabulate(e_uses, tablefmt='grid')}


AUTHOR: @rijul dhungana
#FREE-TO-USE
"""

def doc():
    print(__doc__)

def q():
    quit()

def clr():
    os.system("clear")

def sin(x, in_degrees=default_unit_in_degrees, precision='2f'):
    if in_degrees:
      return float(f"{math.sin(math.radians(x)):.{precision}}")
    else:
        return float(f"{math.sin(x):.{precision}}")

def cos(x, in_degrees=default_unit_in_degrees, precision='2f'):
    if in_degrees:
      return float(f"{math.cos(math.radians(x)):.{precision}}")
    else:
        return float(f"{math.cos(x):.{precision}}")

def tan(x, in_degrees=default_unit_in_degrees, precision='2f'):
    if in_degrees:
      return float(f"{math.tan(math.radians(x)):.{precision}}")
    else:
        return float(f"{math.tan(x):.{precision}}")

def cot(x, in_degrees=default_unit_in_degrees, precision='2f'):
    try:
        return 1/tan(x, in_degrees=in_degrees, precision=precision)
    except ZeroDivisionError:
        return math.nan
def cosec(x, in_degrees=default_unit_in_degrees, precision='2f'):
    try:
        return 1/sin(x, in_degrees=in_degrees, precision=precision)
    except ZeroDivisionError:
        return math.nan

def sec(x, in_degrees=default_unit_in_degrees, precision='2f'):
    try:
        return 1/ cos(x, in_degrees=in_degrees, precision=precision)
    except ZeroDivisionError:
        return math.nan
        
def pow(x, power):
    return x**power

def root(x, root):
    return x**(1/root)

def sqrt(x):
    return root(x, 2)

def cbrt(x):
    return root(x, 3)

def sqr(x):
    return pow(x, 2)

def cube(x):
    return pow(x, 3)

def degrees2rad(x):
    return math.radians(x)

def rad2degrees(x):
    return math.degrees(x)

def sin_inv(x, in_degrees=True):
    if in_degrees:
        return math.degrees(math.asin(x)) 
    else:
        return math.asin(x)

def cos_inv(x, in_degrees=True):
    if in_degrees:
        return math.degrees(math.acos(x)) 
    else:
        return math.acos(x)

def tan_inv(x, in_degrees=True):
    if in_degrees:
        return math.degrees(math.atan(x)) 
    else:
        return math.atan(x)





def scale(matrix, scale_vec, axis):
    mat = copy.deepcopy(matrix)
    invalid_axes = ['none', 'None', 'False', None, False]

    if axis in invalid_axes:
        return scale_vec * mat

    for i in range(len(scale_vec)):
        if axis == 1:
            mat[:, i] = matrix[:, i] * scale_vec[i]
        elif axis == 0:
            mat[i, :] = matrix[i, :] * scale_vec[i]
        else:
            print("Unknown axis")
            return False

    return mat



  

def howto(fn):
    r = random.randint(1, 360)
    fmt= f"""
Provides usage instructions for a given mathematical function.

Args:
    fn (function): The mathematical function for which usage instructions are needed.

Design of {fn.__name__}: {fn.__name__}(x, in_degrees)

Example:

To use the '{fn.__name__}' function:
>>> {fn.__name__}(30)  # Input angle in degrees -> 30
>>> {fn(30)}

Note: The '{fn.__name__}' function assumes the angle is in degrees. If not, specify radians:
>>> {fn.__name__}(30, in degrees=False)
>>> {fn(30, in_degrees=False)}

Try Running {fn.__name__}({r}) it should give {fn(r)} [assuming the angle is in degrees]

"""
    return(fmt)

############EXAMPLE###############
#print(sin(30, precision='5f'))
#print(cos(30, precision='5f'))
#print(sin(30, precision='5f'))
#print(tan(30, precision='5f'))
#print(cosec(30, precision='5f'))
#print(cot(30, precision='5f'))
#print(sec(30, precision='5f'))
##################################


