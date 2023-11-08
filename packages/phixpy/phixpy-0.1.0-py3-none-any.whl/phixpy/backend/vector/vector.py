import phixpy.backend.math_funcs_utils.math_funcs as math_funcs#can be imported independently
import phixpy.backend.math_funcs_utils.uid  as uid # a phixpy module for generating random IDs
import phixpy.backend.compressor.compressor as compressor# a phixpy script for compressing and decompressing phixpy objects
from numpy import asarray # for converting into ndarrays, in 'to_numpy' function
#global precision value, for defining how much precise value user need
# Example
# GLOBAL_PRECISION_VAL = '2f' would return a value with just 2 decimals at max
# while '3f' would return 3 decimals at mat
GLOBAL_PRECISION_VAL = '3f'



#############REMOVED################
#from vector_plot import VectorPlot#
####################################

########VERSION DETAILS########
#name = phixpy.core_engine     #
#type = vector & math engine  #
#build = unstable             #
#condition = unfinished       #
#version = 0.1                #
###############################

details = """
########VERSION DETAILS########
#name = phixpy.core_engine  #
#type = vector & math engine  #
#build = unstable             #
#condition = unfinished       #
#version = 0.0.1              #
# C: Rijul Dhungana           #
###############################

"""


###################phixpy'S CORE MODULE##############################
# This module handles the phixpy objects like vector, scalar, matrix#
# author: Rijul Dhungana                                           #
####################################################################



#############################VECTOR OBJECT########################################
# 'vector' is a phixpy object thant carries all the properties a vector carries   #
# 'vector' can be used for both mathematical physics' caluculation               #
# It's generally not recommended for image data and other computer related stuff #
# for images 'tensor' can be used ['tensor' is not available for now]            #
# 'tensor' is planned to be added in the near future                             #
##################################################################################  
class vector:
    """
    vector: A phixpy object thant carries all the properties that a vector carries
            vector can be used for doing physics involving vectors

    Initialization: Initializing a vector object requires no compulsory arguments.
    
    Arguments:
    array : Takes python lists or np.array as an argument, it is the actual array that
            contains the vector
    unit  : Can be used to specify the unit of vector. e.g: 'force', 'velocity'
    mutable : specify whether vector is changable or not; True for yes and False for no
    dtype : specify the datatype of vector; int, float, complex, unit

    Example:

    #initializing a vector 'a'
    >>> a = vector([1,2,3])
    >>> print(a)
    [out] vector([1,2,3]) 

    """
    def __init__(self, array=None, unit=None, mutable=True, dtype=float):    
        self.dtype = dtype
        self.array = array
        self.uid = uid.generate_uuid(7,7)
        if self.array is not None:
            self.dimension = len(self.array)
        else:
            self.dimension = 0
        self.unit = unit
        self.str_mul = True
        self.list_like_repr = False
        self.__index = 0
        self.mutable = mutable
        self.rank = NotImplemented
        self.__post_init__()

    #after initialization
    def __post_init__(self):
        if self.dimension > 0:
            #changing dtype
            for i in range(len(self.array)):
                self.array[i] = self.__change_dtype(self.array[i], self.dtype)
        else:
            pass

    #private method to change dtype
    def __change_dtype(self, value, dtype):
        self.dtype = dtype
        if value is not None:
            return dtype(value)
        else:
            return None  # or handle the case where value is None differently
    
    #reprisentation print
    def __repr__(self):
        if self.dimension == 0:
            return f"phixpy.vector()"
        if self.list_like_repr:
            return f"{self.array}"
        else:
            return f"phixpy.vector({self.array})"
            

    def __len__(self):
        return len(self.array)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            output = []
            for i in range(self.dimension):
                output.append(self.array[i] + other)
        elif isinstance(other, vector):
            if other.dimension != self.dimension:
                raise ValueError("Dimensions didn't match")
            output = []
            for i in range(self.dimension):
                output.append(self.array[i] + other.array[i])

        return vector(output, dtype=float)

    def __radd__(self, scalar):
        return self+scalar

    def __rmul__(self, scalar):
        return self*scalar

    def __rsub__(self, scalar):
        return - (self-scalar)





    def __sub__(self, other):
        if isinstance(other, (int, float)):
            output = []
            for i in range(self.dimension):
                output.append(self.array[i] - other)
        elif isinstance(other, vector):
            if other.dimension != self.dimension:
                raise ValueError("Dimensions didn't match")
            output = []
            for i in range(self.dimension):
                output.append(self.array[i] - other.array[i])

        return vector(output, dtype=float)


  
    def __mul__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError("Dimensions didn't match")
            else:
                output = []
                for i in range(self.dimension):
                    output.append(self.array[i] * other.array[i])
                return vector(output)
        except AttributeError:
            if type(other) != str:    
                output = []
                for i in range(self.dimension):
                    output.append(self.array[i] * other)
                return vector(output)
            else:
                if self.str_mul:   
                    print("Warning: you're multiplying 'vector' with 'str' this will work by just repeating the string the n times\nn is the number at the ith index in the 'vector'.")
                    output = []
                    for i in range(self.dimension+1):
                        output.append(self.array[i] * other)
                    return vector(output)
                else:
                    raise ValueError("cannot multiply 'vector' with 'str'\n set 'self.str_mul' to True to make it possible")


     
    def __matmul__(self, other):
        if self.dimension != other.dimension:
            raise ValueError("Dimensions didn't matched")
        else:
           output = 0
           for i in range(self.dimension):
               output += self.array[i]*other.array[i]
           return output

    def __truediv__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError("Dimensions didn't match")
            else:
                output = []
                for i in range(self.dimension):
                    output.append(self.array[i] / other.array[i])
                return vector(output, dtype=float)
        except AttributeError: 
            output = []
            for i in range(self.dimension):
                output.append(self.array[i] / other)
            return vector(output, dtype=float)

    def __floordiv__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError("Dimensions didn't match")
            else:
                output = []
                for i in range(self.dimension):
                    output.append(self.array[i] // other.array[i])
                return vector(output, dtype=float)
        except AttributeError: 
            output = []
            for i in range(self.dimension):
                output.append(self.array[i] // other)
            return vector(output, dtype=float)

    def append(self, value):
        if self.dimension > 0:
            self.array.append(value)

        else:
            self.array = value
            self.dimension = 1


    def __mod__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError("Dimensions didn't match")
            else:
                output = []
                for i in range(self.dimension):
                    output.append(self.array[i] % other.array[i])
                return vector(output, dtype=int)
        except AttributeError: 
            output = []
            for i in range(self.dimension):
                output.append(self.array[i] % other)
            return vector(output, dtype=int)

    def __divmod__(self, other):
        try:
            if self.dimension != other.dimension:
                raise ValueError("Dimensions didn't match")
            else:
                output = []
                for i in range(self.dimension):
                    o = divmod(self.array[i], other.array[i])
                    op = vector([o[0], o[1]], dtype=int)
                    op.list_like_repr = True
                    print(op)
                    output.append(op)
                return output

        except AttributeError: 
            output = []
            for i in range(self.dimension):
                    o = divmod(self.array[i], other)
                    op = vector([o[0], o[1]], dtype=int)
                    op.list_like_repr = True
                    print(op)
                    output.append(op)
            return output
    
    def __iter__(self):
        return self


    def __next__(self):
        if self.__index < len(self):
            result = self.array[self.__index]
            self.__index += 1
            return result
        else:
            raise StopIteration

    def __list__(self):
        return self.array

    def __getitem__(self, idx):
        return  self.array[idx]

    def __setitem__(self, idx, value):
        if self.mutable:
            self.array[idx] = value 
        else:
            raise ValueError("'vector' is unmutable")

    def __neg__(self):
        output = []
        for i in self.array:
            output.append(-i)
        return vector(output)

    def change_dtype(self, dtype):
        self.dtype = dtype
        self.__post_init__()

    def id(self):
        return self.uid


    def assign(self, idx, value):
        if type(idx) != int and type(value) != int:
            if len(idx) == len(value):
                if len(idx) <= self.dimension:
                    for i in range(len(idx)+1):
                        self[idx[i]] = value[i]
                else:
                    raise ValueError("Out of range")
            else:
                raise ValueError("Out of range")
        else: 
            self[idx] = value
            
    def get_items(self, idx):
        if type(idx) != int:
            if len(idx) == len(value):
                if len(idx) <= self.dimension:
                    output = vector()
                    for i in range(len(idx)):
                        output.append(self[idx[i]])
                    return vector(output)
                else:
                    raise ValueError("Out of range")
            else:
                raise ValueError("Out of range")
        else: 
            return vector(self[idx])

    def __gt__(self, other):
        return len(self) > len(other)

    def __eq__(self, other):
        return self.array == other.array

    def sum(self):
        return sum(self.array)

    def sin(self, in_degrees=True, precision=GLOBAL_PRECISION_VAL):
        output = []
        for i in self.array:
            output.append(math_funcs.sin(i, in_degrees=in_degrees, precision=precision))
        return vector(output, dtype=float)

    def cos(self, in_degrees=True, precision=GLOBAL_PRECISION_VAL):
        output = []
        for i in self.array:
            output.append(math_funcs.cos(i, in_degrees=in_degrees, precision=precision))
        return vector(output, dtype=float)

    def tan(self, in_degrees=True, precision=GLOBAL_PRECISION_VAL):
        output = []
        for i in self.array:
            output.append(math_funcs.tan(i, in_degrees=in_degrees, precision=precision))
        return vector(output, dtype=float)

    def cosec(self, in_degrees=True, precision=GLOBAL_PRECISION_VAL):
        output = []
        for i in self.array:
            output.append(math_funcs.cosec(i, in_degrees=in_degrees, precision=precision))
        return vector(output, dtype=float)

    def cot(self, in_degrees=True, precision=GLOBAL_PRECISION_VAL):
        output = []
        for i in self.array:
            output.append(math_funcs.cot(i, in_degrees=in_degrees, precision=precision))
        return vector(output, dtype=float)

    def sec(self, in_degrees=True, precision=GLOBAL_PRECISION_VAL):
        output = []
        for i in self.array:
            output.append(math_funcs.sec(i, in_degrees=in_degrees, precision=precision))
        return vector(output, dtype=float)

    def visualize(self, c='b', lims='auto', title='auto', tail='origin'):
        print("FUNCTION REMOVED: 'visualize' has been removed from the core of phixpy\nuse 'VectorPlot' from 'vector_plot' instead")

    def map(self, fn, **kwargs):
        output = []
        for i in self:
            output.append(fn(i, **kwargs))
        return vector(output, dtype=float)

    def pow(self, power):
        return self.map(math_funcs.pow, power=power)

    def root(self, root):
        return self.map(math_funcs.root, root=root)

    def sqrt(self):
        return self.map(math_funcs.sqrt)

    def cbrt(self):
        return self.map(math_funcs.cbrt)

    def sqr(self):
        return self.map(math_funcs.sqr)

    def cube(self):
        return self.map(math_funcs.cube)

    def degrees2rad(self):
        return self.map(math_funcs.degrees2rad)

    def rad2degrees(self):
        return self.map(math_funcs.rad2degrees)
    
    def __fmt(self, x, f='3f'):
        return f"{(x):.{f}}"

    def avg(self):
        return self.sum() / self.dimension

    def format(self, fmt='3f'):
        return self.map(self.__fmt)

    def __format__(self, fmt_specifier):
        if fmt_specifier == 'sum':
            return str(self.sum())

        elif fmt_specifier == 'avg':
            return str(self.avg())

        elif fmt_specifier == 'arr':
            return str(self.array)

        elif fmt_specifier == 'arr_open':
            return " ".join(map(str, self.array))

        elif fmt_specifier == 'arr_open_fmted':
            return ":\n" + " \n".join(map(str, self.array)) + "\n"

        elif fmt_specifier == 'sin':
            return " ".join(map(str, self.sin().array))

    def __pow__(self, pow):
        return self.pow(pow)

    def dot(self, other):
        return self@other

    def multiply(self, other):
        return self*other

    def fill(dimension, val):
        output = []
        for i in range(dimension):
            output.append(val)
        return vector(output)

    def zeros(dimension):
        return vector.fill(val=0, dimension=dimension)
    
    def ones(dimension):
        return vector.fill(val=1, dimension=dimension)

    def random(dimension, random_state=None, dtype=int, val_range=(1,100)):
        import random
        if random_state is not None:
            output = []
            random.seed(random_state)
            if dtype == int:
                for i in range(dimension):
                    r = random.randint(*val_range)
                    output.append(r)
                return vector(output)

            elif dtype == float:
                from random import uniform
                for i in range(dimension):
                    r = random.uniform(*val_range)
                    output.append(r)
                return vector(output, dtype=float)
        else:
            output = []
            if dtype == int:
                for i in range(dimension):
                    r = random.randint(*val_range)
                    output.append(r)
                return vector(output)

            elif dtype == float:
                from random import uniform
                for i in range(dimension):
                    r = random.uniform(*val_range)
                    output.append(r)
                return vector(output, dtype=float)
            

    def add(self, other):
        return self+other

    def sub(self, other):
        return self-other

    def divide(self, other):
        return self/other

    def mod(self, other):
        return self%other

    def compress_and_save(self, filename):
        compressor.compress_and_save(self, filename)

    def load(filename):
        return compressor.load_and_decompress(filename)

    def to_numpy(self):
        return asarray(self.array)

    def sin_inv(self, in_degrees=True, precision=GLOBAL_PRECISION_VAL):
        return self.map(math_funcs.sin_inv, in_degrees=in_degrees, precision=precision)

    def magnitude(self):
        return math_funcs.sqrt((self**2).sum())

    def angle_betn(self, other, in_degrees=True):
        if isinstance(other, vector):
            if self.dimension == other.dimension:
                dot = vector.dot(self, other)
                magnitude_self = self.magnitude()
                magnitude_other = other.magnitude()
                ratio = dot/(magnitude_self*magnitude_other)
                return math_funcs.cos_inv(ratio, in_degrees=in_degrees) 
            else:
                raise ValueError("Dimension of vectors did'nt match")
        else:
            raise ValueError("Unsupported Data type")

    def is_orthogonal(self, other):
        return True if self.dot(other) == 0 else False

    def filter(self, fn):
        output = []
        for x in self.array:
            if fn(x):
                output.append(x)

        return vector(output)

    def get_evens(self):
        def even(x):
            if x % 2 == 0:
                return True 
        return self.filter(even)

    def get_odds(self):
        def odd(x):
            if x % 2 == 1:
                return True
        return self.filter(odd)

   # def to_unit(self):
      #  return Unit(self)

    def vec2string(self):
        if self.dimension == 0:
            self.__str_repr = f"phixpy.vector(->None)"
        if self.list_like_repr:
            self.__str_repr = f"{self.array}" 
        else:
            self.__str_repr = f"phixpy.vector({self.array})"
        return self.__str_repr
        

