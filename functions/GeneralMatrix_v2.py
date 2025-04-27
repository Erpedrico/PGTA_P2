import numpy as np
import math
from typing import List, Dict, Optional, Union
import scipy.linalg

class GeneralMatrix:
    def __init__(self, *args):
        """
        Constructores compatibles:
        1. GeneralMatrix(m, n) - Matriz de ceros mxn
        2. GeneralMatrix(m, n, s) - Matriz mxn llena del valor s
        3. GeneralMatrix(A) - Desde un array 2D de Python
        4. GeneralMatrix(A, m, n) - Desde array 2D con dimensiones específicas
        5. GeneralMatrix(vals, m) - Desde array 1D empaquetado por columnas
        """
        if len(args) == 2:
            # Constructor GeneralMatrix(m, n)
            self.m, self.n = args
            self.A = np.zeros((self.m, self.n))
        elif len(args) == 3 and isinstance(args[2], (int, float)):
            # Constructor GeneralMatrix(m, n, s)
            self.m, self.n, s = args
            self.A = np.full((self.m, self.n), s)
        elif len(args) == 1 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(A)
            A = np.array(args[0])
            self.m, self.n = A.shape
            self.A = A.copy()
        elif len(args) == 3 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(A, m, n)
            self.A = np.array(args[0])
            self.m, self.n = args[1], args[2]
        elif len(args) == 2 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(vals, m)
            vals, m = args
            vals = np.array(vals)
            if len(vals.shape) == 1:
                if m * (len(vals) // m) != len(vals):
                    raise ValueError("Array length must be a multiple of m.")
                self.m = m
                self.n = len(vals) // m
                self.A = vals.reshape(self.m, self.n, order='F')  # Empaquetado por columnas
            else:
                raise ValueError("Invalid input for constructor")
        else:
            raise ValueError("Invalid arguments for constructor")

    @property
    def Array(self) -> np.ndarray:
        """Acceso al array interno"""
        return self.A

    @property 
    def ArrayCopy(self) -> np.ndarray:
        """Copia del array interno"""
        return self.A.copy()

    @property
    def ColumnPackedCopy(self) -> np.ndarray:
        """Copia empaquetada por columnas"""
        return self.A.flatten(order='F')  # 'F' para orden Fortran (columnas)

    @property
    def RowPackedCopy(self) -> np.ndarray:
        """Copia empaquetada por filas"""
        return self.A.flatten(order='C')  # 'C' para orden C (filas)

    @property
    def RowDimension(self) -> int:
        """Número de filas"""
        return self.m

    @property 
    def ColumnDimension(self) -> int:
        """Número de columnas"""
        return self.n

    @staticmethod
    def Create(A: List[List[float]]) -> 'GeneralMatrix':
        """Crea una matriz desde un array 2D"""
        return GeneralMatrix(A)

    def Copy(self) -> 'GeneralMatrix':
        """Copia profunda de la matriz"""
        return GeneralMatrix(self.A.copy())

    def GetElement(self, i: int, j: int) -> float:
        """Obtiene el elemento (i,j)"""
        return self.A[i, j]

    def SetElement(self, i: int, j: int, s: float):
        """Establece el elemento (i,j)"""
        self.A[i, j] = s

    def GetMatrix(self, i0: int, i1: int, j0: int, j1: int) -> 'GeneralMatrix':
        """Obtiene una submatriz"""
        return GeneralMatrix(self.A[i0:i1+1, j0:j1+1].copy())

    def Transpose(self) -> 'GeneralMatrix':
        """Transposición de la matriz"""
        return GeneralMatrix(self.A.T.copy())

    def Norm1(self) -> float:
        """Norma 1 (máxima suma de columnas)"""
        return np.max(np.sum(np.abs(self.A), axis=0))

    def Norm2(self) -> float:
        """Norma 2 (mayor valor singular)"""
        return np.linalg.norm(self.A, 2)

    def NormInf(self) -> float:
        """Norma infinito (máxima suma de filas)"""
        return np.max(np.sum(np.abs(self.A), axis=1))

    def NormF(self) -> float:
        """Norma Frobenius"""
        return np.linalg.norm(self.A, 'fro')

    def UnaryMinus(self) -> 'GeneralMatrix':
        """Matriz negativa"""
        return GeneralMatrix(-self.A)

    def Add(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Suma de matrices"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A + B.A)

    def AddEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Suma in-place"""
        self._check_dimensions(B)
        self.A += B.A
        return self

    def Subtract(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resta de matrices"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A - B.A)

    def SubtractEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resta in-place"""
        self._check_dimensions(B)
        self.A -= B.A
        return self

    def ArrayMultiply(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación elemento a elemento"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A * B.A)

    def ArrayMultiplyEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación elemento a elemento in-place"""
        self._check_dimensions(B)
        self.A *= B.A
        return self

    def Multiply(self, s: float) -> 'GeneralMatrix':
        """Multiplicación por escalar"""
        return GeneralMatrix(self.A * s)

    def MultiplyEquals(self, s: float) -> 'GeneralMatrix':
        """Multiplicación por escalar in-place"""
        self.A *= s
        return self

    def MultiplyMatrix(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación de matrices"""
        if self.n != B.m:
            raise ValueError("Matrix inner dimensions must agree.")
        return GeneralMatrix(np.dot(self.A, B.A))

    def Solve(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resuelve A*X = B"""
        if self.m == self.n:
            # Matriz cuadrada: usar descomposición LU
            return GeneralMatrix(np.linalg.solve(self.A, B.A))
        else:
            # Matriz rectangular: solución por mínimos cuadrados
            return GeneralMatrix(np.linalg.lstsq(self.A, B.A, rcond=None)[0])

    def Inverse(self) -> 'GeneralMatrix':
        """Inversa de la matriz"""
        return GeneralMatrix(np.linalg.inv(self.A))

    def Determinant(self) -> float:
        """Determinante de la matriz"""
        return np.linalg.det(self.A)

    def Rank(self) -> int:
        """Rango de la matriz"""
        return np.linalg.matrix_rank(self.A)

    def Trace(self) -> float:
        """Traza de la matriz"""
        return np.trace(self.A)

    @staticmethod
    def Random(m: int, n: int) -> 'GeneralMatrix':
        """Matriz aleatoria mxn"""
        return GeneralMatrix(np.random.rand(m, n))

    @staticmethod 
    def Identity(m: int, n: int) -> 'GeneralMatrix':
        """Matriz identidad mxn"""
        return GeneralMatrix(np.eye(m, n))

    def _check_dimensions(self, B: 'GeneralMatrix'):
        """Verifica que las dimensiones coincidan"""
        if self.m != B.m or self.n != B.n:
            raise ValueError("Matrix dimensions must agree.")

    # Operadores sobrecargados
    def __add__(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        return self.Add(B)

    def __sub__(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        return self.Subtract(B)

    def __mul__(self, other: Union['GeneralMatrix', float]) -> 'GeneralMatrix':
        if isinstance(other, GeneralMatrix):
            return self.MultiplyMatrix(other)
        elif isinstance(other, (int, float)):
            return self.Multiply(other)
        else:
            raise TypeError("Operand must be GeneralMatrix or scalar")

    def __repr__(self) -> str:
        return f"GeneralMatrix({self.m}x{self.n}):\n{self.A}"

    # Métodos para descomposiciones (simplificados)
    def LUD(self) -> Dict:
        """Descomposición LU"""
        P, L, U = scipy.linalg.lu(self.A)
        return {'P': GeneralMatrix(P), 'L': GeneralMatrix(L), 'U': GeneralMatrix(U)}

    def QRD(self) -> Dict:
        """Descomposición QR"""
        Q, R = np.linalg.qr(self.A)
        return {'Q': GeneralMatrix(Q), 'R': GeneralMatrix(R)}

    def SVD(self) -> Dict:
        """Descomposición en valores singulares"""
        U, s, Vh = np.linalg.svd(self.A)
        return {'U': GeneralMatrix(U), 'S': GeneralMatrix(np.diag(s)), 'V': GeneralMatrix(Vh.T)}

class GeneralMatrix:
    def __init__(self, *args):
        """
        Constructores compatibles:
        1. GeneralMatrix(m, n) - Matriz de ceros mxn
        2. GeneralMatrix(m, n, s) - Matriz mxn llena del valor s
        3. GeneralMatrix(A) - Desde un array 2D de Python
        4. GeneralMatrix(A, m, n) - Desde array 2D con dimensiones específicas
        5. GeneralMatrix(vals, m) - Desde array 1D empaquetado por columnas
        """
        if len(args) == 2:
            # Constructor GeneralMatrix(m, n)
            self.m, self.n = args
            self.A = np.zeros((self.m, self.n))
        elif len(args) == 3 and isinstance(args[2], (int, float)):
            # Constructor GeneralMatrix(m, n, s)
            self.m, self.n, s = args
            self.A = np.full((self.m, self.n), s)
        elif len(args) == 1 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(A)
            A = np.array(args[0])
            self.m, self.n = A.shape
            self.A = A.copy()
        elif len(args) == 3 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(A, m, n)
            self.A = np.array(args[0])
            self.m, self.n = args[1], args[2]
        elif len(args) == 2 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(vals, m)
            vals, m = args
            vals = np.array(vals)
            if len(vals.shape) == 1:
                if m * (len(vals) // m) != len(vals):
                    raise ValueError("Array length must be a multiple of m.")
                self.m = m
                self.n = len(vals) // m
                self.A = vals.reshape(self.m, self.n, order='F')  # Empaquetado por columnas
            else:
                raise ValueError("Invalid input for constructor")
        else:
            raise ValueError("Invalid arguments for constructor")

    @property
    def Array(self) -> np.ndarray:
        """Acceso al array interno"""
        return self.A

    @property 
    def ArrayCopy(self) -> np.ndarray:
        """Copia del array interno"""
        return self.A.copy()

    @property
    def ColumnPackedCopy(self) -> np.ndarray:
        """Copia empaquetada por columnas"""
        return self.A.flatten(order='F')  # 'F' para orden Fortran (columnas)

    @property
    def RowPackedCopy(self) -> np.ndarray:
        """Copia empaquetada por filas"""
        return self.A.flatten(order='C')  # 'C' para orden C (filas)

    @property
    def RowDimension(self) -> int:
        """Número de filas"""
        return self.m

    @property 
    def ColumnDimension(self) -> int:
        """Número de columnas"""
        return self.n

    @staticmethod
    def Create(A: List[List[float]]) -> 'GeneralMatrix':
        """Crea una matriz desde un array 2D"""
        return GeneralMatrix(A)

    def Copy(self) -> 'GeneralMatrix':
        """Copia profunda de la matriz"""
        return GeneralMatrix(self.A.copy())

    def GetElement(self, i: int, j: int) -> float:
        """Obtiene el elemento (i,j)"""
        return self.A[i, j]

    def SetElement(self, i: int, j: int, s: float):
        """Establece el elemento (i,j)"""
        self.A[i, j] = s

    def GetMatrix(self, i0: int, i1: int, j0: int, j1: int) -> 'GeneralMatrix':
        """Obtiene una submatriz"""
        return GeneralMatrix(self.A[i0:i1+1, j0:j1+1].copy())

    def Transpose(self) -> 'GeneralMatrix':
        """Transposición de la matriz"""
        return GeneralMatrix(self.A.T.copy())

    def Norm1(self) -> float:
        """Norma 1 (máxima suma de columnas)"""
        return np.max(np.sum(np.abs(self.A), axis=0))

    def Norm2(self) -> float:
        """Norma 2 (mayor valor singular)"""
        return np.linalg.norm(self.A, 2)

    def NormInf(self) -> float:
        """Norma infinito (máxima suma de filas)"""
        return np.max(np.sum(np.abs(self.A), axis=1))

    def NormF(self) -> float:
        """Norma Frobenius"""
        return np.linalg.norm(self.A, 'fro')

    def UnaryMinus(self) -> 'GeneralMatrix':
        """Matriz negativa"""
        return GeneralMatrix(-self.A)

    def Add(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Suma de matrices"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A + B.A)

    def AddEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Suma in-place"""
        self._check_dimensions(B)
        self.A += B.A
        return self

    def Subtract(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resta de matrices"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A - B.A)

    def SubtractEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resta in-place"""
        self._check_dimensions(B)
        self.A -= B.A
        return self

    def ArrayMultiply(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación elemento a elemento"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A * B.A)

    def ArrayMultiplyEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación elemento a elemento in-place"""
        self._check_dimensions(B)
        self.A *= B.A
        return self

    def Multiply(self, s: float) -> 'GeneralMatrix':
        """Multiplicación por escalar"""
        return GeneralMatrix(self.A * s)

    def MultiplyEquals(self, s: float) -> 'GeneralMatrix':
        """Multiplicación por escalar in-place"""
        self.A *= s
        return self

    def MultiplyMatrix(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación de matrices"""
        if self.n != B.m:
            raise ValueError("Matrix inner dimensions must agree.")
        return GeneralMatrix(np.dot(self.A, B.A))

    def Solve(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resuelve A*X = B"""
        if self.m == self.n:
            # Matriz cuadrada: usar descomposición LU
            return GeneralMatrix(np.linalg.solve(self.A, B.A))
        else:
            # Matriz rectangular: solución por mínimos cuadrados
            return GeneralMatrix(np.linalg.lstsq(self.A, B.A, rcond=None)[0])

    def Inverse(self) -> 'GeneralMatrix':
        """Inversa de la matriz"""
        return GeneralMatrix(np.linalg.inv(self.A))

    def Determinant(self) -> float:
        """Determinante de la matriz"""
        return np.linalg.det(self.A)

    def Rank(self) -> int:
        """Rango de la matriz"""
        return np.linalg.matrix_rank(self.A)

    def Trace(self) -> float:
        """Traza de la matriz"""
        return np.trace(self.A)

    @staticmethod
    def Random(m: int, n: int) -> 'GeneralMatrix':
        """Matriz aleatoria mxn"""
        return GeneralMatrix(np.random.rand(m, n))

    @staticmethod 
    def Identity(m: int, n: int) -> 'GeneralMatrix':
        """Matriz identidad mxn"""
        return GeneralMatrix(np.eye(m, n))

    def _check_dimensions(self, B: 'GeneralMatrix'):
        """Verifica que las dimensiones coincidan"""
        if self.m != B.m or self.n != B.n:
            raise ValueError("Matrix dimensions must agree.")

    # Operadores sobrecargados
    def __add__(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        return self.Add(B)

    def __sub__(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        return self.Subtract(B)

    def __mul__(self, other: Union['GeneralMatrix', float]) -> 'GeneralMatrix':
        if isinstance(other, GeneralMatrix):
            return self.MultiplyMatrix(other)
        elif isinstance(other, (int, float)):
            return self.Multiply(other)
        else:
            raise TypeError("Operand must be GeneralMatrix or scalar")

    def __repr__(self) -> str:
        return f"GeneralMatrix({self.m}x{self.n}):\n{self.A}"

    # Métodos para descomposiciones (simplificados)
    def LUD(self) -> Dict:
        """Descomposición LU"""
        P, L, U = scipy.linalg.lu(self.A)
        return {'P': GeneralMatrix(P), 'L': GeneralMatrix(L), 'U': GeneralMatrix(U)}

    def QRD(self) -> Dict:
        """Descomposición QR"""
        Q, R = np.linalg.qr(self.A)
        return {'Q': GeneralMatrix(Q), 'R': GeneralMatrix(R)}

    def SVD(self) -> Dict:
        """Descomposición en valores singulares"""
        U, s, Vh = np.linalg.svd(self.A)
        return {'U': GeneralMatrix(U), 'S': GeneralMatrix(np.diag(s)), 'V': GeneralMatrix(Vh.T)}

class GeneralMatrix:
    def __init__(self, *args):
        """
        Constructores compatibles:
        1. GeneralMatrix(m, n) - Matriz de ceros mxn
        2. GeneralMatrix(m, n, s) - Matriz mxn llena del valor s
        3. GeneralMatrix(A) - Desde un array 2D de Python
        4. GeneralMatrix(A, m, n) - Desde array 2D con dimensiones específicas
        5. GeneralMatrix(vals, m) - Desde array 1D empaquetado por columnas
        """
        if len(args) == 2:
            # Constructor GeneralMatrix(m, n)
            self.m, self.n = args
            self.A = np.zeros((self.m, self.n))
        elif len(args) == 3 and isinstance(args[2], (int, float)):
            # Constructor GeneralMatrix(m, n, s)
            self.m, self.n, s = args
            self.A = np.full((self.m, self.n), s)
        elif len(args) == 1 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(A)
            A = np.array(args[0])
            self.m, self.n = A.shape
            self.A = A.copy()
        elif len(args) == 3 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(A, m, n)
            self.A = np.array(args[0])
            self.m, self.n = args[1], args[2]
        elif len(args) == 2 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(vals, m)
            vals, m = args
            vals = np.array(vals)
            if len(vals.shape) == 1:
                if m * (len(vals) // m) != len(vals):
                    raise ValueError("Array length must be a multiple of m.")
                self.m = m
                self.n = len(vals) // m
                self.A = vals.reshape(self.m, self.n, order='F')  # Empaquetado por columnas
            else:
                raise ValueError("Invalid input for constructor")
        else:
            raise ValueError("Invalid arguments for constructor")

    @property
    def Array(self) -> np.ndarray:
        """Acceso al array interno"""
        return self.A

    @property 
    def ArrayCopy(self) -> np.ndarray:
        """Copia del array interno"""
        return self.A.copy()

    @property
    def ColumnPackedCopy(self) -> np.ndarray:
        """Copia empaquetada por columnas"""
        return self.A.flatten(order='F')  # 'F' para orden Fortran (columnas)

    @property
    def RowPackedCopy(self) -> np.ndarray:
        """Copia empaquetada por filas"""
        return self.A.flatten(order='C')  # 'C' para orden C (filas)

    @property
    def RowDimension(self) -> int:
        """Número de filas"""
        return self.m

    @property 
    def ColumnDimension(self) -> int:
        """Número de columnas"""
        return self.n

    @staticmethod
    def Create(A: List[List[float]]) -> 'GeneralMatrix':
        """Crea una matriz desde un array 2D"""
        return GeneralMatrix(A)

    def Copy(self) -> 'GeneralMatrix':
        """Copia profunda de la matriz"""
        return GeneralMatrix(self.A.copy())

    def GetElement(self, i: int, j: int) -> float:
        """Obtiene el elemento (i,j)"""
        return self.A[i, j]

    def SetElement(self, i: int, j: int, s: float):
        """Establece el elemento (i,j)"""
        self.A[i, j] = s

    def GetMatrix(self, i0: int, i1: int, j0: int, j1: int) -> 'GeneralMatrix':
        """Obtiene una submatriz"""
        return GeneralMatrix(self.A[i0:i1+1, j0:j1+1].copy())

    def Transpose(self) -> 'GeneralMatrix':
        """Transposición de la matriz"""
        return GeneralMatrix(self.A.T.copy())

    def Norm1(self) -> float:
        """Norma 1 (máxima suma de columnas)"""
        return np.max(np.sum(np.abs(self.A), axis=0))

    def Norm2(self) -> float:
        """Norma 2 (mayor valor singular)"""
        return np.linalg.norm(self.A, 2)

    def NormInf(self) -> float:
        """Norma infinito (máxima suma de filas)"""
        return np.max(np.sum(np.abs(self.A), axis=1))

    def NormF(self) -> float:
        """Norma Frobenius"""
        return np.linalg.norm(self.A, 'fro')

    def UnaryMinus(self) -> 'GeneralMatrix':
        """Matriz negativa"""
        return GeneralMatrix(-self.A)

    def Add(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Suma de matrices"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A + B.A)

    def AddEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Suma in-place"""
        self._check_dimensions(B)
        self.A += B.A
        return self

    def Subtract(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resta de matrices"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A - B.A)

    def SubtractEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resta in-place"""
        self._check_dimensions(B)
        self.A -= B.A
        return self

    def ArrayMultiply(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación elemento a elemento"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A * B.A)

    def ArrayMultiplyEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación elemento a elemento in-place"""
        self._check_dimensions(B)
        self.A *= B.A
        return self

    def Multiply(self, s: float) -> 'GeneralMatrix':
        """Multiplicación por escalar"""
        return GeneralMatrix(self.A * s)

    def MultiplyEquals(self, s: float) -> 'GeneralMatrix':
        """Multiplicación por escalar in-place"""
        self.A *= s
        return self

    def MultiplyMatrix(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación de matrices"""
        if self.n != B.m:
            raise ValueError("Matrix inner dimensions must agree.")
        return GeneralMatrix(np.dot(self.A, B.A))

    def Solve(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resuelve A*X = B"""
        if self.m == self.n:
            # Matriz cuadrada: usar descomposición LU
            return GeneralMatrix(np.linalg.solve(self.A, B.A))
        else:
            # Matriz rectangular: solución por mínimos cuadrados
            return GeneralMatrix(np.linalg.lstsq(self.A, B.A, rcond=None)[0])

    def Inverse(self) -> 'GeneralMatrix':
        """Inversa de la matriz"""
        return GeneralMatrix(np.linalg.inv(self.A))

    def Determinant(self) -> float:
        """Determinante de la matriz"""
        return np.linalg.det(self.A)

    def Rank(self) -> int:
        """Rango de la matriz"""
        return np.linalg.matrix_rank(self.A)

    def Trace(self) -> float:
        """Traza de la matriz"""
        return np.trace(self.A)

    @staticmethod
    def Random(m: int, n: int) -> 'GeneralMatrix':
        """Matriz aleatoria mxn"""
        return GeneralMatrix(np.random.rand(m, n))

    @staticmethod 
    def Identity(m: int, n: int) -> 'GeneralMatrix':
        """Matriz identidad mxn"""
        return GeneralMatrix(np.eye(m, n))

    def _check_dimensions(self, B: 'GeneralMatrix'):
        """Verifica que las dimensiones coincidan"""
        if self.m != B.m or self.n != B.n:
            raise ValueError("Matrix dimensions must agree.")

    # Operadores sobrecargados
    def __add__(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        return self.Add(B)

    def __sub__(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        return self.Subtract(B)

    def __mul__(self, other: Union['GeneralMatrix', float]) -> 'GeneralMatrix':
        if isinstance(other, GeneralMatrix):
            return self.MultiplyMatrix(other)
        elif isinstance(other, (int, float)):
            return self.Multiply(other)
        else:
            raise TypeError("Operand must be GeneralMatrix or scalar")

    def __repr__(self) -> str:
        return f"GeneralMatrix({self.m}x{self.n}):\n{self.A}"

    # Métodos para descomposiciones (simplificados)
    def LUD(self) -> Dict:
        """Descomposición LU"""
        P, L, U = scipy.linalg.lu(self.A)
        return {'P': GeneralMatrix(P), 'L': GeneralMatrix(L), 'U': GeneralMatrix(U)}

    def QRD(self) -> Dict:
        """Descomposición QR"""
        Q, R = np.linalg.qr(self.A)
        return {'Q': GeneralMatrix(Q), 'R': GeneralMatrix(R)}

    def SVD(self) -> Dict:
        """Descomposición en valores singulares"""
        U, s, Vh = np.linalg.svd(self.A)
        return {'U': GeneralMatrix(U), 'S': GeneralMatrix(np.diag(s)), 'V': GeneralMatrix(Vh.T)}

class GeneralMatrix:
    def __init__(self, *args):
        """
        Constructores compatibles:
        1. GeneralMatrix(m, n) - Matriz de ceros mxn
        2. GeneralMatrix(m, n, s) - Matriz mxn llena del valor s
        3. GeneralMatrix(A) - Desde un array 2D de Python
        4. GeneralMatrix(A, m, n) - Desde array 2D con dimensiones específicas
        5. GeneralMatrix(vals, m) - Desde array 1D empaquetado por columnas
        """
        if len(args) == 2:
            # Constructor GeneralMatrix(m, n)
            self.m, self.n = args
            self.A = np.zeros((self.m, self.n))
        elif len(args) == 3 and isinstance(args[2], (int, float)):
            # Constructor GeneralMatrix(m, n, s)
            self.m, self.n, s = args
            self.A = np.full((self.m, self.n), s)
        elif len(args) == 1 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(A)
            A = np.array(args[0])
            self.m, self.n = A.shape
            self.A = A.copy()
        elif len(args) == 3 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(A, m, n)
            self.A = np.array(args[0])
            self.m, self.n = args[1], args[2]
        elif len(args) == 2 and isinstance(args[0], (list, np.ndarray)):
            # Constructor GeneralMatrix(vals, m)
            vals, m = args
            vals = np.array(vals)
            if len(vals.shape) == 1:
                if m * (len(vals) // m) != len(vals):
                    raise ValueError("Array length must be a multiple of m.")
                self.m = m
                self.n = len(vals) // m
                self.A = vals.reshape(self.m, self.n, order='F')  # Empaquetado por columnas
            else:
                raise ValueError("Invalid input for constructor")
        else:
            raise ValueError("Invalid arguments for constructor")

    @property
    def Array(self) -> np.ndarray:
        """Acceso al array interno"""
        return self.A

    @property 
    def ArrayCopy(self) -> np.ndarray:
        """Copia del array interno"""
        return self.A.copy()

    @property
    def ColumnPackedCopy(self) -> np.ndarray:
        """Copia empaquetada por columnas"""
        return self.A.flatten(order='F')  # 'F' para orden Fortran (columnas)

    @property
    def RowPackedCopy(self) -> np.ndarray:
        """Copia empaquetada por filas"""
        return self.A.flatten(order='C')  # 'C' para orden C (filas)

    @property
    def RowDimension(self) -> int:
        """Número de filas"""
        return self.m

    @property 
    def ColumnDimension(self) -> int:
        """Número de columnas"""
        return self.n

    @staticmethod
    def Create(A: List[List[float]]) -> 'GeneralMatrix':
        """Crea una matriz desde un array 2D"""
        return GeneralMatrix(A)

    def Copy(self) -> 'GeneralMatrix':
        """Copia profunda de la matriz"""
        return GeneralMatrix(self.A.copy())

    def GetElement(self, i: int, j: int) -> float:
        """Obtiene el elemento (i,j)"""
        return self.A[i, j]

    def SetElement(self, i: int, j: int, s: float):
        """Establece el elemento (i,j)"""
        self.A[i, j] = s

    def GetMatrix(self, i0: int, i1: int, j0: int, j1: int) -> 'GeneralMatrix':
        """Obtiene una submatriz"""
        return GeneralMatrix(self.A[i0:i1+1, j0:j1+1].copy())

    def Transpose(self) -> 'GeneralMatrix':
        """Transposición de la matriz"""
        return GeneralMatrix(self.A.T.copy())

    def Norm1(self) -> float:
        """Norma 1 (máxima suma de columnas)"""
        return np.max(np.sum(np.abs(self.A), axis=0))

    def Norm2(self) -> float:
        """Norma 2 (mayor valor singular)"""
        return np.linalg.norm(self.A, 2)

    def NormInf(self) -> float:
        """Norma infinito (máxima suma de filas)"""
        return np.max(np.sum(np.abs(self.A), axis=1))

    def NormF(self) -> float:
        """Norma Frobenius"""
        return np.linalg.norm(self.A, 'fro')

    def UnaryMinus(self) -> 'GeneralMatrix':
        """Matriz negativa"""
        return GeneralMatrix(-self.A)

    def Add(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Suma de matrices"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A + B.A)

    def AddEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Suma in-place"""
        self._check_dimensions(B)
        self.A += B.A
        return self

    def Subtract(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resta de matrices"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A - B.A)

    def SubtractEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resta in-place"""
        self._check_dimensions(B)
        self.A -= B.A
        return self

    def ArrayMultiply(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación elemento a elemento"""
        self._check_dimensions(B)
        return GeneralMatrix(self.A * B.A)

    def ArrayMultiplyEquals(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación elemento a elemento in-place"""
        self._check_dimensions(B)
        self.A *= B.A
        return self

    def Multiply(self, s: float) -> 'GeneralMatrix':
        """Multiplicación por escalar"""
        return GeneralMatrix(self.A * s)

    def MultiplyEquals(self, s: float) -> 'GeneralMatrix':
        """Multiplicación por escalar in-place"""
        self.A *= s
        return self

    def MultiplyMatrix(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Multiplicación de matrices"""
        if self.n != B.m:
            raise ValueError("Matrix inner dimensions must agree.")
        return GeneralMatrix(np.dot(self.A, B.A))

    def Solve(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        """Resuelve A*X = B"""
        if self.m == self.n:
            # Matriz cuadrada: usar descomposición LU
            return GeneralMatrix(np.linalg.solve(self.A, B.A))
        else:
            # Matriz rectangular: solución por mínimos cuadrados
            return GeneralMatrix(np.linalg.lstsq(self.A, B.A, rcond=None)[0])

    def Inverse(self) -> 'GeneralMatrix':
        """Inversa de la matriz"""
        return GeneralMatrix(np.linalg.inv(self.A))

    def Determinant(self) -> float:
        """Determinante de la matriz"""
        return np.linalg.det(self.A)

    def Rank(self) -> int:
        """Rango de la matriz"""
        return np.linalg.matrix_rank(self.A)

    def Trace(self) -> float:
        """Traza de la matriz"""
        return np.trace(self.A)

    @staticmethod
    def Random(m: int, n: int) -> 'GeneralMatrix':
        """Matriz aleatoria mxn"""
        return GeneralMatrix(np.random.rand(m, n))

    @staticmethod 
    def Identity(m: int, n: int) -> 'GeneralMatrix':
        """Matriz identidad mxn"""
        return GeneralMatrix(np.eye(m, n))

    def _check_dimensions(self, B: 'GeneralMatrix'):
        """Verifica que las dimensiones coincidan"""
        if self.m != B.m or self.n != B.n:
            raise ValueError("Matrix dimensions must agree.")

    # Operadores sobrecargados
    def __add__(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        return self.Add(B)

    def __sub__(self, B: 'GeneralMatrix') -> 'GeneralMatrix':
        return self.Subtract(B)

    def __mul__(self, other: Union['GeneralMatrix', float]) -> 'GeneralMatrix':
        if isinstance(other, GeneralMatrix):
            return self.MultiplyMatrix(other)
        elif isinstance(other, (int, float)):
            return self.Multiply(other)
        else:
            raise TypeError("Operand must be GeneralMatrix or scalar")

    def __repr__(self) -> str:
        return f"GeneralMatrix({self.m}x{self.n}):\n{self.A}"

    # Métodos para descomposiciones (simplificados)
    def LUD(self) -> Dict:
        """Descomposición LU"""
        P, L, U = scipy.linalg.lu(self.A)
        return {'P': GeneralMatrix(P), 'L': GeneralMatrix(L), 'U': GeneralMatrix(U)}

    def QRD(self) -> Dict:
        """Descomposición QR"""
        Q, R = np.linalg.qr(self.A)
        return {'Q': GeneralMatrix(Q), 'R': GeneralMatrix(R)}

    def SVD(self) -> Dict:
        """Descomposición en valores singulares"""
        U, s, Vh = np.linalg.svd(self.A)
        return {'U': GeneralMatrix(U), 'S': GeneralMatrix(np.diag(s)), 'V': GeneralMatrix(Vh.T)}