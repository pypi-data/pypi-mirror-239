import math
import numpy as np

I = complex(0, 1)

class Matrix:
    def __init__(self, l: list[list[complex]]=[]) -> None:
            if type(l) is not list:
                raise ValueError(f"l was expected to be list[list[complex]], no {type(l)}")
            for u_ in l:
                if type(u_) is not list:
                    raise ValueError(f"l was expected to be list[list[complex]]. A {type(u_)} has been found")
            for l_ in l:
                for x in l_:
                    if type(x) not in {int, float, complex}:
                        raise ValueError(f"l was expected to be list[list[complex]]. A {type(x)} has been found")
            
            self.__m = l
            if l == []:
                  self.__m = [[0, 0], [0, 0]]
            self.__size = (len(self.__m), len(self.__m[0]))
    
    def __mul__(self, __value: "Matrix") -> "Matrix":
        if type(__value) is not Matrix:
            raise ValueError(f"cannot multiply Matrix with {type(__value)}")
        
        l = np.kron(self.__m, __value._Matrix__m).tolist()
        
        return Matrix(l)
    
    def __apply(self, x: list[complex]) -> list[complex]:
        if type(x) is not list:
            raise TypeError(f"can apply a Matrix to a list[complex, not to a {type(x)}]")
        for y in x:
            if type(y) not in {int, float, complex}:
                TypeError(f"can apply a Matrix to a ")
        if not self.__size[1] == len(x):
            raise ValueError(f"the vector was expectedd to be of size {self.__size[1]}, but is of size {len(x)}")

        y: list[complex] = np.dot(self.__m, x).tolist()
        return y
    
    def __str__(self) -> str:
        return str(self.__m)
    
    def to_list(self) -> list[list[complex]]:
        """convert the Matrix into a list representation"""  
        return self._Matrix__m.copy()

    @staticmethod
    def I() -> "Matrix":
        return Matrix([
            [1, 0],
            [0, 1]
        ])
    
    @staticmethod
    def H() -> "Matrix":
        s = 1/math.sqrt(2)
        return Matrix([
            [s, s],
            [s, -s]
        ])

    @staticmethod
    def X() -> "Matrix":
        return Matrix([
            [0, 1],
            [1, 0]
        ])
    
    @staticmethod
    def SQRTX() -> "Matrix":
        return Matrix([
            [(1+I)/2, (1-I)/2],
            [(1-I)/2, (1+I)/2]
        ])

    @staticmethod
    def Y() -> "Matrix":
        return Matrix([
            [0, -I],
            [I, 0]
        ])

    @staticmethod
    def Z() -> "Matrix":
        return Matrix([
            [1, 0],
            [0, -1]
        ])
    
    @staticmethod
    def S() -> "Matrix":
        return Matrix([
            [1, 0],
            [0, I]
        ])

    @staticmethod
    def T() -> "Matrix":
        s = math.e**(I*math.pi/4)
        return Matrix([
            [1, 0],
            [0, s]
        ])
    
    @staticmethod
    def Rx(phi: float) -> "Matrix":
        if type(phi) not in {int, float}:
            TypeError(f"an angle must be integer or float, not {type(phi)}")

        c = math.cos(phi/2)
        s = math.sin(phi/2)
        return Matrix([
            [c, -I*s],
            [-I*s, c]
        ])
    
    @staticmethod
    def Ry(phi: float) -> "Matrix":
        if type(phi) not in {int, float}:
            TypeError(f"an angle must be integer or float, not {type(phi)}")

        c = math.cos(phi/2)
        s = math.sin(phi/2)
        return Matrix([
            [c, -s],
            [s, c]
        ])
    
    @staticmethod
    def Rz(phi: float) -> "Matrix":
        if type(phi) not in {int, float}:
            TypeError(f"an angle must be integer or float, not {type(phi)}")

        s = math.e**(I*phi/2)
        return Matrix([
            [1/s, 0],
            [0, s]
        ])
    
    @staticmethod
    def R1(phi: float) -> "Matrix":
        if type(phi) not in {int, float}:
            TypeError(f"an angle must be integer or float, not {type(phi)}")
            
        s = math.e**(I*phi)
        return Matrix([
            [1, 0],
            [0, s]
        ])

    @staticmethod
    def CX() -> "Matrix":
        return Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ])
    
    @staticmethod
    def CY() -> "Matrix":
        return Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, -I],
            [0, 0, I, 0]
        ])
    
    @staticmethod
    def CZ() -> "Matrix":
        return Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, -1]
        ])
    
    @staticmethod
    def SWAP() -> "Matrix":
        return Matrix([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])
    
    @staticmethod
    def Cu(u: list[list[complex]]) -> "Matrix":
        if type(u) is not list:
            raise ValueError(f"u was expected to be list[list[complex]], not {type(u)}")
        for u_ in u:
            if type(u_) is not list:
                raise ValueError(f"u was expected to be list[list[complex]]. A {type(u_)} has been found")
        for l in u:
            for x in l:
                if type(x) not in {int, float, complex}:
                    raise ValueError(f"u was expected to be list[list[complex]]. A {type(x)} has been found")
        if len(u) != 2 or len(u[0]) != 2:
            if len(u) == 0:
                raise ValueError(f"the size of the matrix was expected to be (2, 2). A matrix of size (0, .) has been given")
            raise ValueError(f"the size of the matrix was expected to be (2, 2). A matrix of size ({len(u)}, {u[0]}) has been given")

        l = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, u[0][0], u[0][1]],
            [0, 0, u[1][0], u[1][1]]
        ]

        return Matrix(l)

if __name__=="__main__":
    m1 = Matrix([[1]])
    m2 = Matrix([[1, 1], [0, 1]])

    print(m1*m2)