import math
import random as rd
import matplotlib.pyplot as plt

from QElephant.Matrix import *

## Classes

class MuBit:
    def __init__(self, n: int=2) -> None:
        """a set of entangled QuBits

        Args:
            n (int, optional): number of entangled QuBits. Must be at least 2. Defaults to 2.
        """
        if type(n) is not int:
            raise TypeError(f"number of state must be an intergers, not {type(n)}")
        if not n >= 2:
            raise ValueError("a MuBit must have at least two entangled QuBit")

        self.__n = n
        self.__state: list[complex] = [0]*(2**self.__n)
        self.__state[0] = 1
        self.__callBack = None
    
    def __emit(self, gate: str, target: int, neighbor: list[int]=[]) -> None:
        if self.__callBack is not None:
            self.__callBack(gate, target, neighbor)
    
    def __str__(self) -> str:
        def next(N: str) -> str:
            if N == "":
                return ""
            if N[-1] == "0":
                return N[:-1]+"1"
            else:
                return (next(N[:-1]))+"0"
        
        txt = ""
        N = "0"*self.__n
        for i in range(2**self.__n):
            txt += f"{round(self.__state[i], 3)} |{N}>\n"
            N = next(N)
        return txt
    
    def __set(self, i: int, value: int) -> None:
        """Set the nth QuBit into value"""
        if type(i) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(i)}")
        if i > self.__n:
            raise IndexError("MuBit index out of range")
        if not value in {0, 1}:
            raise ValueError(f"QuBit state must be 0 or 1, not {value}")
        
        if self.__getProb(i) != value: # when prob==1 and we want prob==0. Value is in {0, 1}
            l = []
            a, d = 1-value, value
            for k in range(i, self.__n-1):
                self.__SWITCH(k)
            j = 0
            while j < 2**self.__n:
                x1, x2 = self.__state[j], self.__state[j+1]
                l.append(a*x1)
                l.append(d*x2)
                j += 2
            self.__state = l
            for k in range(self.__n-2, i-1, -1):
                self.__SWITCH(k)

            norm = math.sqrt(sum([abs(x)**2 for x in self.__state]))
            self.__state = [x/norm for x in self.__state]
        else:
            self.__apply(Matrix.X(), i)
    
    def __iter__(self):
        return iter([IQuBit(i, self) for i in range(self.__n)])
    
    def __getitem__(self, item: int) -> "QuBit":
        if type(item) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(item)}")
        if item > self.__n:
            raise IndexError("MuBit index out of range")
        item = item%self.__n

        return IQuBit(item, self)

    def __apply(self, matrix: Matrix, i: int) -> None:
        if type(i) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(i)}")
        if i > self.__n:
            raise IndexError("MuBit index out of range")
        if type(matrix) is not Matrix:
            raise TypeError(f"can only manipulate MuBit with Matrix, not {type(matrix)}")
        i = i%self.__n

        l = []
        m = matrix._Matrix__m
        a, b, c, d = m[0][0], m[0][1], m[1][0], m[1][1]
        for k in range(i, self.__n-1):
            self.__SWITCH(k)
        j = 0
        while j < 2**self.__n:
            x1, x2 = self.__state[j], self.__state[j+1]
            l.append(a*x1+b*x2)
            l.append(c*x1+d*x2)
            j += 2
        self.__state = l
        for k in range(self.__n-2, i-1, -1):
            self.__SWITCH(k)
    
    def __mapply(self, matrix: Matrix, i: int) -> None:
        """Can only apply controlled gates"""
        if type(i) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(i)}")
        if i >= self.__n:
            raise IndexError("MuBit index out of range")
        if type(matrix) is not Matrix:
            raise TypeError(f"can only manipulate MuBit with Matrix, not {type(matrix)}")
        i = i%self.__n

        m = matrix._Matrix__m
        a, b, c, d = m[2][2], m[2][3], m[3][2], m[3][3]
        j = 0
        while j < 2**self.__n:
            x3, x4 = self.__state[j+2], self.__state[j+3]
            self.__state[j+2] = a*x3+b*x4
            self.__state[j+3] = c*x3+d*x4
            j += 4
    
    def __getProb(self, i: int) -> float:
        """Probs for i to be zero"""
        if type(i) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(i)}")
        if i > self.__n:
            raise IndexError("MuBit index out of range")
        i = i%self.__n

        prob = 0
        pas = 2**(self.__n-i-1)
        j = 0
        while j < 2**self.__n:
            prob += sum([abs(x)**2 for x in self.__state[j:j+pas]])
            j += 2*pas
        
        return prob
    
    def __SWITCH(self, i: int) -> None:
        if type(i) is not int:
            raise TypeError(f"MuBit indices must be integers, not {type(i)}")
        if i >= self.__n:
            raise IndexError("MuBit index out of range")
        i = i%self.__n

        lng = 2**(self.__n-i)
        a = lng//4
        b = lng//2
        c = 3*lng//4
        K = 0
        for k in range(2**(i)):
            A = K+a
            B = K+b
            C = K+c
            self.__state[A:B], self.__state[B:C] = self.__state[B:C], self.__state[A:B]
            K += lng
    
    def __SWAP(self, n1: int, n2: int) -> None:
        """exchange the place between the two targeted QuBit

        Args:
            n1 (int): index of the first QuBit
            n2 (int): index of the second QuBit
            emit (bool): 
        """
        if type(n1) is not int:
            TypeError(f"MuBit indices must be intergers, not {type(n1)}")
        if type(n2) is not int:
            TypeError(f"MuBit indices must be intergers, not {type(n2)}")
        if n1 > self.__n or n2 > self.__n:
            raise ValueError("Mubit index out of range")
        n1 = n1%self.__n
        n2 = n2%self.__n

        if n1 != n2:
            nmin = min(n1, n2)
            nmax = max(n1, n2)
            for i in range(nmin, nmax):
                self.__SWITCH(i)
            for i in range(nmax-2, nmin-1, -1):
                self.__SWITCH(i)
    
    def get_size(self) -> int:
        """returns the number of entangled QuBits
        """
        return self.__n
            
    def draw(self, show_state=False) -> None:
        """draw in a histogram the probability of each state in the order from |0...0> to |1...1>

        Args:
            show_state (bool, optional): if True, shows the name of each state in the histogram. Defaults to False.
        """
        def next(N: str) -> str:
            if N == "":
                return ""
            if N[-1] == "0":
                return N[:-1]+"1"
            else:
                return (next(N[:-1]))+"0"
        
        xlabels = []
        lab = "0"*self.__n
        for i in range(2**self.__n):
            xlabels.append(lab)
            lab = next(lab)

        X = [n for n in range(2**self.__n)]
        Y = [abs(self.__state[int(k)])**2 for k in X]
        plt.hist(X+[2**self.__n], weights=Y+[0], bins=2**self.__n)
        if show_state:
            plt.xticks([x+0.5 for x in X], [f"|{xlab}>" for xlab in xlabels])
        else:
            plt.xticks([0, 2**self.__n-1], ["", ""])
        plt.show()

    def observe(self) -> list[int]:
        """fixe all the QuBit in one state according their probabilities

        Returns:
            list[int]: the list of the fixed state of the QuBits 
        """
        r = rd.random()
        s = 0
        state = 0
        for prob in self.__state:
            s += abs(prob)**2
            if r < s:
                break
            state += 1
        if state == 2**self.__n:
            state -= 1
        self.state = [0]*(2**self.__n)
        self.state[state] = 1

        l = []
        for i in range(self.__n):
            l.insert(0, state%2)
            state -= state%2
            state //= 2

        self.__emit("Mobserve", 0, range(self.get_size()))
        return l
    
    def reset(self) -> None:
        """reset the state to |0...0>
        """
        self.__state = [0]*2**self.__n
        self.__state[0] = 1
        self.__emit("M-|0>", 0, range(self.get_size()))
    
    @staticmethod
    def intricateThem(*args: "QuBit") -> "MuBit":
        """creates a situation where all the given QuBit are now entangled

        Returns:
            MuBit: a copy of the given QuBits, but entangled
        """
        for q in args:
            if type(q) is IQuBit:
                raise TypeError("cannot intricate QuBit that are already entangled")
            if type(q) is not QuBit:
                raise TypeError(f"cannot intricate QuBit and {type(q)}")
        if len(args) < 2:
            raise ValueError("cannot intricate less than two QuBits")

        S = Matrix([[1]])
        for q in args:
            S *= Matrix([q._QuBit__state])

        mq = MuBit(len(args))
        mq._MuBit__state = S._Matrix__m[0]
        return mq
    
class QuBit:
    def __init__(self, alpha: complex=1, beta: complex=0):
        """a single QuBit

        Args:
            alpha (complex, optional): complex coefficient for the state |0>. Defaults to 1.
            beta (complex, optional): complex coefficient for the state |1>. Defaults to 0.
        """
        if type(alpha) not in {int, float, complex}:
            raise TypeError(f"QuBit state must be int, float or complex, not {type(alpha)}")
        if type(beta) not in {int, float, complex}:
            raise TypeError(f"QuBit state must be int, float or complex, not {type(alpha)}")
        if abs(alpha)**2 + abs(beta)**2 != 1:
            raise ValueError(f"the initial state must be normalized. Here, |alpha|**2+|beta|**2={abs(alpha)**2 + abs(beta)**2}")
        
        self.__state = [alpha, beta]
        self.__entangled = False
    
    def __str__(self) -> str:
        return f"{round(self.__state[0], 3)} |0> + {round(self.__state[1], 3)} |1>"
    
    def __apply(self, matrix: Matrix) -> None:
        if type(matrix) is not Matrix:
            raise TypeError(f"can only manipulate QuBit with Matrix, not {type(matrix)}")

        self.__state = matrix._Matrix__apply(self.__state)
    
    def is_entangled(self) -> bool:
        """tells if the corresponding QuBit is entangled

        Returns:
            bool: True if this is the case, or else False
        """
        return self.__entangled
    
    def observe(self) -> list[int]:
        """set the state to |0> or |1> according its probabilities

        Returns:
            int: the new state of the QuBit
        """
        r = rd.random()
        if r < abs(self.__state[0])**2:
            self.__state = [1, 0]
            return 0
        self.__state = [0, 1]
        return 1
    
    def reset(self) -> None:
        """reset the state to |0>
        """
        self.__state = [1, 0]

class IQuBit(QuBit):
    def __init__(self, n: int, mb: MuBit) -> None:
        if type(n) is not int:
            raise TypeError(f"MuBit indices must be interger, not {type(n)}")
        if n > mb._MuBit__n:
            raise ValueError(f"MuBit index out of range")
        if type(mb) is not MuBit:
            raise TypeError(f"an intricate QuBit should be associated with a MuBit, not a {type(mb)}")
        n = n%mb._MuBit__n

        super().__init__()
        self.__n = n
        self.__muBit = mb
        self.__entangled = True
    
    def __str__(self) -> str:
        p = self.__muBit._MuBit__getProb(self.__n)
        return str(QuBit(math.sqrt(p), math.sqrt(1-p)))
    
    def __apply(self, matrix: Matrix) -> None:
        if type(matrix) is not Matrix:
            raise TypeError(f"can only manipulate QuBit with Matrix, not {type(matrix)}")

        self.__muBit._MuBit__apply(matrix, self.__n)
    
    def is_entangled(self) -> bool:
        """tells if the corresponding QuBit is entangled

        Returns:
            bool: True if this is the case, or else False
        """
        return self.__entangled
    
    def get_Mubit(self) -> tuple[MuBit, int]:
        """returns the MuBit in wich the MuBit is stocked

        Returns:
            tuple[MuBit, int]: the corresponding MuBit and its place among all the QuBits contained in the same MuBit
        """
        return (self.__muBit, self.__n)
    
    def observe(self) -> int:
        """set the state to |0> or |1> according its probabilities

        Returns:
            int: the new state of the QuBit
        """
        r = rd.random()
        self.__muBit._MuBit__emit("obs", self.__n, [])
        if r < self.__muBit._MuBit__getProb(self.__n):
            self.__muBit._MuBit__set(self.__n, 0)
            return 0
        self.__muBit._MuBit__set(self.__n, 1)
        return 1
    
    def reset(self) -> None:
        """reset the state to |0>
        """
        self.__muBit._MuBit__set(self.__n, 0)
        self.__muBit._MuBit__emit("|0>", self.__n, [])





## Fonctions

def H(q: (QuBit | MuBit)) -> None:
    """apply the gate H to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
    """
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.H())
        q._IQuBit__muBit._MuBit__emit("H", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.H())
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.H())
        q._MuBit__emit("M-H", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def X(q: (QuBit | MuBit)) -> None:
    """apply the gate X to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
    """
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.X())
        q._IQuBit__muBit._MuBit__emit("X", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.X())
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.X())
        q._MuBit__emit("MX", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def SQRTX(q: (QuBit | MuBit)) -> None:
    """apply the gate corresponding of the square root of the X-gate to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
    """
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.SQRTX())
        q._IQuBit__muBit._MuBit__emit("√¬", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.SQRTX())
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.SQRTX())
        q._MuBit__emit("M-√¬", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def Y(q: (QuBit | MuBit)) -> None:
    """apply the gate Y to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
    """
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Y())
        q._IQuBit__muBit._MuBit__emit("Y", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.Y())
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.Y())
        q._MuBit__emit("M-Y", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def Z(q: (QuBit | MuBit)) -> None:
    """apply the gate Z to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
    """
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Z())
        q._IQuBit__muBit._MuBit__emit("Z", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.Z())
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.Z())
        q._MuBit__emit("M-Z", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def S(q: (QuBit | MuBit)) -> None:
    """apply the gate S to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
    """
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.S())
        q._IQuBit__muBit._MuBit__emit("S", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.S())
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.S())
        q._MuBit__emit("M-S", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def T(q: (QuBit | MuBit)) -> None:
    """apply the gate T to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
    """
    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.T())
        q._IQuBit__muBit._MuBit__emit("T", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.T())
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.T())
        q._MuBit__emit("M-T", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def Rx(q: (QuBit | MuBit), phi: float) -> None:
    """apply a rotation around the x-axis to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
        phi (float): the angle or the rotation
    """
    if type(phi) not in {int, float}:
        raise TypeError(f"an angle must be integer or float, not {type(phi)}")

    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Rx(phi))
        q._IQuBit__muBit._MuBit__emit("Rx", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.Rx(phi))
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.Rx(phi))
        q._MuBit__emit("M-Rx", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def Ry(q: (QuBit | MuBit), phi: float) -> None:
    """apply a rotation around the y-axis to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
        phi (float): the angle or the rotation
    """
    if type(phi) not in {int, float}:
        raise TypeError(f"an angle must be integer or float, not {type(phi)}")

    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Ry(phi))
        q._IQuBit__muBit._MuBit__emit("Ry", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.Ry(phi))
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.Ry(phi))
        q._MuBit__emit("M-Ry", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def Rz(q: (QuBit | MuBit), phi: float) -> None:
    """apply a rotation around the z-axis to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
        phi (float): the angle or the rotation
    """
    if type(phi) not in {int, float}:
        raise TypeError(f"an angle must be integer or float, not {type(phi)}")

    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.Rz(phi))
        q._IQuBit__muBit._MuBit__emit("Rz", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.Rz(phi))
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.Rz(phi))
        q._MuBit__emit("M-Rz", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")

def R1(q: (QuBit | MuBit), phi: float) -> None:
    """apply the gate R1(phi) to the QuBit or all the QuBit of a MuBit

    Args:
        q (QuBit  |  MuBit): the target
        phi (float): the angle or the rotation
    """
    if type(phi) not in {int, float}:
        raise TypeError(f"an angle must be integer or float, not {type(phi)}")

    if type(q) == IQuBit:
        q._IQuBit__apply(Matrix.R1(phi))
        q._IQuBit__muBit._MuBit__emit("R1", q._IQuBit__n, [])
    elif type(q) == QuBit:
        q._QuBit__apply(Matrix.R1(phi))
    elif type(q) == MuBit:
        for i in range(q.get_size()):
            q[i]._IQuBit__apply(Matrix.R1(phi))
        q._MuBit__emit("M-R1", 0, range(q._MuBit__n))
    else:
        raise TypeError(f"a QuBit or a MuBit was expected, but a {type(q)} was given")
    
def Bell(q: MuBit, n1: int, n2: int, phase: str="phi+") -> None:
    """set the state of the two QuBits to:
    - |00> + |11> if phase = 'phi+'
    - |00> - |11> if phase = 'phi-'
    - |01> + |10> if phase = 'psi+'
    - |01> - |10> if phase = 'psi-'

    Args:
        q (MuBit): the MuBit containing the targeted QuBits
        n1 (int): index of the first QuBit
        n2 (int): index of the second QuBit
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(n1) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n1)}")
    if type(n2) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n2)}")
    if n1 >= q._MuBit__n or n2 >= q._MuBit__n:
        raise ValueError("Mubit index out of range")
    if type(phase) is not str:
        raise TypeError(f"expected a str for a phase, not {type(phase)}")
    if phase not in {"phi+", "phi-", "psi+", "psi-"}:
        raise ValueError("phase must be a value among 'phi+', 'phi-', 'psi+', 'psi-'")
    

    n = q._MuBit__n
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)
    q._MuBit__set(n-2, 0)
    q._MuBit__set(n-1, 0)
    q._MuBit__apply(Matrix.H(), n-2)
    q._MuBit__mapply(Matrix.CX(), n-2)

    if phase[-1] == '-':
        q._MuBit__apply(Matrix.Z(), n-1)
    if phase[1] == "s":
        q._MuBit__apply(Matrix.X(), n-1)
    
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)

    match phase:
        case "phi+":
            q._MuBit__emit("Φ⁺", n1, [n2])
        case "phi-":
            q._MuBit__emit("Φ⁻", n1, [n2])
        case "psi+":
            q._MuBit__emit("Ψ⁺", n1, [n2])
        case "psi-":
            q._MuBit__emit("Ψ⁻", n1, [n2])

def Dicke(q: MuBit, k: int) -> None:
    """set the state to |1,K>|0,n-k>

    Args:
        q (MuBit): the targeted QuBits
        k (int): number of 1. If out of range, set k to 0 or n
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(k) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(k)}")
    k = min(k, q._MuBit__n)
    k = max(0, k)

    state = [0]*(q._MuBit__n-k) + [1]*k
    i = 0
    for j in range(len(state)):
        i += state[j]*2**j
    
    q._MuBit__state = [0]*2**q._MuBit__n
    q._MuBit__state[i] = 1

    q._MuBit__emit(f"M-|D({q._MuBit__n}, {k})>", 0, range(q._MuBit__n))

def Wigner(q: MuBit, a: complex) -> None:
    """set the state given a complexe formula

    Args:
        q (MuBit): the targeted QuBits
        a (complex): complexe ratio of the serie
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(a) not in {int, float, complex}:
            raise TypeError(f"QuBit state must be int, float or complex, not {type(a)}")
    
    state = [a**k/math.sqrt(math.factorial(k)) for k in range(2**q._MuBit__n)]
    norm = sum(abs(x)**2 for x in state)
    q._MuBit__state = [x/norm for x in state]

    q._MuBit__emit("M-W(α)", 0, range(q._MuBit__n))

def Cat(q: MuBit, a: complex, parity: int=0) -> None:
    """set the state given a complexe formula

    Args:
        q (MuBit): the targeted QuBits
        a (complex): complexe ratio of the serie
        parity (int, optional): give the parity of the chossen terms. Defaults to 0.
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if parity not in {0, 1}:
            raise ValueError(f"parity must be 0 or 1, not {parity}")
    if type(a) not in {int, float, complex}:
            raise TypeError(f"QuBit state must be int, float or complex, not {type(a)}")
    
    state = [((k+1+parity)%2)*a**k/math.sqrt(math.factorial(k)) for k in range(2**q._MuBit__n)]
    norm = sum(abs(x)**2 for x in state)
    q._MuBit__state = [x/norm for x in state]

    if parity==0:
        q._MuBit__emit("M-Catₑ(α)", 0, range(q._MuBit__n))
    else:
        q._MuBit__emit("M-Cat₀(α)", 0, range(q._MuBit__n))

# def 

def CX(q: MuBit, n1: int, n2: int) -> None:
    """apply the controlled gate X to the two given QuBits

    Args:
        q (MuBit): the MuBit containing the targeted QuBits
        n1 (int): index of the controller QuBit
        n2 (int): index of the controlled QuBit
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(n1) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n1)}")
    if type(n2) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n2)}")
    if n1 >= q._MuBit__n or n2 >= q._MuBit__n:
        raise ValueError("Mubit index out of range")
    n1 = n1%q._MuBit__n
    n2 = n2%q._MuBit__n
    if n1==n2:
        raise ValueError("the CNOT gate must be applied on two differents QuBits")

    n = q._MuBit__n
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)
    q._MuBit__mapply(Matrix.CX(), n-2)
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)
    q._MuBit__emit("CX", n1, [n2])

def CY(q: MuBit, n1: int, n2: int) -> None:
    """apply the controlled gate Y to the two given QuBits

    Args:
        q (MuBit): the MuBit containing the targeted QuBits
        n1 (int): index of the controller QuBit
        n2 (int): index of the controlled QuBit
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(n1) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n1)}")
    if type(n2) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n2)}")
    if n1 > q._MuBit__n or n2 > q._MuBit__n:
        raise ValueError("Mubit index out of range")
    n1 = n1%q._MuBit__n
    n2 = n2%q._MuBit__n
    if n1==n2:
        raise ValueError("the CNOT gate must be applied on two differents QuBits")

    n = q._MuBit__n
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)
    q._MuBit__mapply(Matrix.CY(), n-2)
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)
    q._MuBit__emit("Y", n1, [n2])

def CZ(q: MuBit, n1: int, n2: int) -> None:
    """apply the controlled gate Z to the two given QuBits

    Args:
        q (MuBit): the MuBit containing the targeted QuBits
        n1 (int): index of the controller QuBit
        n2 (int): index of the controlled QuBit
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(n1) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n1)}")
    if type(n2) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n2)}")
    if n1 > q._MuBit__n or n2 > q._MuBit__n:
        raise ValueError("Mubit index out of range")
    n1 = n1%q._MuBit__n
    n2 = n2%q._MuBit__n
    if n1==n2:
        raise ValueError("the CNOT gate must be applied on two differents QuBits")

    n = q._MuBit__n
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)
    q._MuBit__mapply(Matrix.CZ(), n-2)
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)
    q._MuBit__emit("Z", n1, [n2])

def SWAP(q: MuBit, n1: int, n2: int) -> None:
    """exchange the place between the two given QuBits

    Args:
        q (MuBit): the MuBit containing the targeted QuBits
        n1 (int): index of the controller QuBit
        n2 (int): index of the controlled QuBit
    """
    if type(q) is not MuBit:
        TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(n1) is not int:
        TypeError(f"MuBit indices must be intergers, not {type(n1)}")
    if type(n2) is not int:
        TypeError(f"MuBit indices must be intergers, not {type(n2)}")
    if n1 > q._MuBit__n or n2 > q._MuBit__n:
        raise ValueError("Mubit index out of range")
    n1 = n1%q._MuBit__n
    n2 = n2%q._MuBit__n

    if n1 != n2:
        nmin = min(n1, n2)
        nmax = max(n1, n2)
        for i in range(nmin, nmax):
            q._MuBit__SWITCH(i)
        for i in range(nmax-2, nmin-1, -1):
            q._MuBit__SWITCH(i)
    
    q._MuBit__emit("SWAP", n1, [n2])

def Cu(q: MuBit, u: list[list[complex]], n1: int, n2: int) -> None:
    """apply the controlled gate u

    Args:
        q (MuBit): the MuBit containing the targeted QuBit
        u (list[list[complex]]): matrix representation of the gate u
        n1 (int): index of the controller QuBit
        n2 (int): index of the controlled QuBit
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    if type(n1) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n1)}")
    if type(n2) is not int:
        raise TypeError(f"MuBit indices must be intergers, not {type(n2)}")
    if n1 > q._MuBit__n or n2 > q._MuBit__n:
        raise ValueError("Mubit index out of range")
    n1 = n1%q._MuBit__n
    n2 = n2%q._MuBit__n
    if n1==n2:
        raise ValueError("the Cu gate must be applied on two differents QuBits")
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

    n = q._MuBit__n
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)
    q._MuBit__mapply(Matrix.Cu(u), n-2)
    q._MuBit__SWAP(n-2, n1)
    q._MuBit__SWAP(n-1, n2)
    q._MuBit__emit("U", n1, [n2])

def GHZ(q: MuBit):
    """set the state to |0...0> + |1...1>

    Args:
        q (MuBit): the targeted QuBit
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    
    q._MuBit__state = [1/math.sqrt(2)] + [0]*(2**q.get_size()-2) + [1/math.sqrt(2)]

    q._MuBit__emit("M-GHZ", 0, range(q.get_size()))

def W(q: MuBit) -> None:
    """set the state to |10...0> + |010...0> +...+ |0...01>

    Args:
        q (MuBit): the targeted QuBit
    """
    if type(q) is not MuBit:
        raise TypeError(f"a MuBit was expected, but a {type(q)} was given")
    
    q._MuBit__state = [0]*(2**q.get_size())
    for k in range(q.get_size()):
        q._MuBit__state[2**k] = 1/math.sqrt(q.get_size())

    q._MuBit__emit("M-W", 0, range(q.get_size()))