from dataclasses import dataclass
from numbers import Number
from math import acos, degrees


@dataclass(order = True)
class Vector2D(object):
    _abscissa: float = 0.0
    _ordinate: float = 0.0

    def __repr__(self):
        return f"Vector2D(abscissa={self._abscissa}, ordinate={self._ordinate})"

    @property
    def abscissa(self) -> float:
        return self._abscissa

    @property
    def ordinate(self) -> float:
        return self._ordinate

    def __bool__(self):
        if self._ordinate == 0 and self._abscissa == 0:
            return False
        else:
            return True

    def __int__  
    def __abs__(self):
        return (self._abscissa**2 + self._ordinate**2)**0.5

    def 

    def __add__(self, other):



    def __mul__(obj1, obj2):
        if isinstance(obj1, Vector2D) and isinstance(obj2, Vector2D):
            raise TypeError
        if isinstance(obj1, Vector2D):
            return Vector2D(obj1._abscissa * obj2, obj1._ordinate * obj2)
        if isinstance(obj2, Vector2D):
            return Vector2D(obj2._abscissa * obj1, obj2._ordinate * obj1)

    def __truediv__(v1, number):
        if isinstance(number, Vector2D):
            raise TypeError
        if number == 0:
            raise ValueError
        return Vector2D(v1._abscissa, v1._ordinate) * (1/number)

    def __sub__(v1, obj):
        if not (isinstance(v1, Vector2D)):
            raise TypeError
        if isinstance(obj, Number):
            return Vector2D(v1._abscissa - obj, v1._ordinate - obj)
        if isinstance(obj, Vector2D):
            return Vector2D(v1._abscissa + obj._abscissa, v1._ordinate + obj._ordinate)

    def __neg__(v1):
        return Vector2D(-v1._abscissa, -v1._ordinate)

    def __matmul__(v1, v2):
        return v1._abscissa*v2._abscissa + v1._ordinate*v2._ordinate

    def get_angle(self, other):
        return degrees(acos((self @ other) / (self.abs()*other.abs())))

    def adjoint(v1):
        return Vector2D(v1._abscissa, -v1._ordinate)


v1 = Vector2D(2.2, 2.1)
v2 = -v1
print(v1, v2, v1@v2)
print(v1+v2, v1-v2)
print(bool(v1))
v3 = Vector2D(0, 0)
print(bool(v3))
v4 = Vector2D(2, 2)
v5 = Vector2D(2, 2)
print(v1.abscissa(), v1.ordinate())