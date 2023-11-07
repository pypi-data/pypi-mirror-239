import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from QElephant.QuBit import *

class Circuit:
    def __init__(self, n: int):
        self.__instr = []
        self.__n = n
        self.__mubit = MuBit(self.__n)
        self.__mubit._MuBit__callBack = self.__recv
    
    def __recv(self, gate: str, target: int, neighbor: list[int]):
        self.__instr.append((gate, target, neighbor))
    
    def __rect(self, q_i: int, i: int, txt: str, size: int) -> None:
        rec = Rectangle((q_i-0.25, i-0.25), 0.5, 0.5, fill=False)
        if len(txt) >= 4:
            plt.text(q_i, i, txt, size=min(int(40/size), int(40/self.__n)), ha='center', va='center')
        else:
            plt.text(q_i, i, txt, size=min(int(70/size), int(70/self.__n)), ha='center', va='center')
        plt.gca().add_patch(rec)
    
    def __line(self, A, B) -> None:
        plt.plot([A[0], B[0]], [A[1], B[1]], color='Black')
    
    def __circle(self, x: float, y: float, radius: float, fill=True) -> None:
        circ = Circle((x, y), radius, fill=fill, color='Black')
        plt.gca().add_patch(circ)
    
    def __cross(self, x: float, y: float):
        self.__line((x-0.25, y-0.25), (x+0.25, y+0.25))
        self.__line((x-0.25, y+0.25), (x+0.25, y-0.25))

    def get_MuBit(self) -> MuBit:
        """returns the MuBit of the Circuit
        """
        return self.__mubit
    
    def get_size(self) -> int:
        """returns the number of entangled QuBit in the Circuit"""
        return self.__n
    
    def draw(self) -> None:
        """draw and display a representation of the Circuit
        """
        n = len(self.__instr)
        plt.yticks(range(self.__n), [f"QuBit {i}" for i in range(self.__n)])
        plt.xticks(range(1, n+1), [f"Step {i+1}" for i in range(n)])

        i = 0
        while i < n:
            txt, index, neigbhor = self.__instr[i]
            for q_i in range(self.__n):
                self.__line((i+0.5, q_i), (i+0.75, q_i))
                self.__line((i+1.25, q_i), (i+1.5, q_i))

                if q_i == index:
                    match txt:
                        case "X":
                            self.__circle(i+1, q_i, 0.25, False)
                            self.__line((i+0.75, q_i), (i+1.25, q_i))
                            self.__line((i+1, q_i-0.25), (i+1, q_i+0.25))
                        case "SWAP":
                            self.__line((i+0.75, q_i), (i+1.25, q_i))
                            self.__cross(i+1, q_i)
                            self.__cross(i+1, neigbhor[0])
                            self.__line((i+1, q_i), (i+1, neigbhor[0]))
                        case "CX":
                            self.__circle(i+1, q_i, 0.25, False)
                            self.__line((i+0.75, q_i), (i+1.25, q_i))
                            self.__line((i+1, q_i-0.25), (i+1, q_i+0.25))
                            self.__circle(i+1, neigbhor[0], 0.05)
                            self.__line((i+1, q_i), (i+1, neigbhor[0]))
                        case "obs":
                            self.__circle(i+1, q_i, 0.25, False)
                            self.__circle(i+1, q_i, 0.05)
                        case "Φ⁺" | "Φ⁻" | "Ψ⁺" | "Ψ⁻":
                            self.__rect(i+1, q_i, txt, n)
                            if neigbhor[0] > q_i:
                                self.__line((i+1, q_i+0.25), (i+1, neigbhor[0]-0.25))
                            elif neigbhor[0] < q_i:
                                self.__line((i+1, q_i-0.25), (i+1, neigbhor[0]+0.25))
                            else:
                                raise ValueError("Cannot apply gate twice on the same QuBit")
                        case "Mobserve":
                            self.__circle(i+1, q_i, 0.25, False)
                            self.__circle(i+1, q_i, 0.05)
                            for k in range(1, self.__n):
                                self.__line((i+1, k-0.75), (i+1, k-0.25))
                        case "MX":
                            self.__circle(i+1, q_i, 0.25, False)
                            self.__line((i+0.75, q_i), (i+1.25, q_i))
                            self.__line((i+1, q_i-0.25), (i+1, q_i+0.25))
                            for k in range(1, self.__n):
                                self.__line((i+1, k-1), (i+1, k))
                        case _:
                            if txt[:2] == "M-":
                                self.__rect(i+1, q_i, txt[2:], n)
                                for k in range(1, self.__n):
                                    self.__line((i+1, k-0.75), (i+1, k-0.25))
                            else:
                                self.__rect(i+1, q_i, txt, n)
                                for neig in neigbhor:
                                    self.__circle(i+1, neig, 0.05)
                                    if neig > q_i:
                                        self.__line((i+1, q_i+0.25), (i+1, neig))
                                    elif neig < q_i:
                                        self.__line((i+1, q_i-0.25), (i+1, neig))
                                    else:
                                        raise ValueError("Cannot apply gate twice on the same QuBit")
                elif q_i in neigbhor:
                    match txt:
                        case "Φ⁺" | "Φ⁻" | "Ψ⁺" | "Ψ⁻":
                            self.__rect(i+1, q_i, txt, n)
                        case "Mobserve":
                            self.__circle(i+1, q_i, 0.25, False)
                            self.__circle(i+1, q_i, 0.05)
                        case "MX":
                            self.__circle(i+1, q_i, 0.25, False)
                            self.__line((i+0.75, q_i), (i+1.25, q_i))
                            self.__line((i+1, q_i-0.25), (i+1, q_i+0.25))
                        case _:
                            if txt[:2] == "M-":
                                self.__rect(i+1, q_i, txt[2:], n)
                            else:
                                self.__line((i+0.75, q_i), (i+1.25, q_i))
                else:
                    self.__line((i+0.75, q_i), (i+1.25, q_i))
            i += 1
        plt.show()
    
if __name__=="__main__":
    c = Circuit(3, [("CS", 0, [1]), ("CX", 2, [0]), ("TX", 1, [0, 2])])
    print(c.get_size())
    c.draw()