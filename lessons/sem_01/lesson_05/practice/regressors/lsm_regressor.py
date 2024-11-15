from typing import Sequence, Union
from numbers import Real

from regressors.regressor_abc import RegressorABC


class RegressorLSM(RegressorABC):
    _train: list
    _k: Real
    _b: Real

    def fit(self, abscissa: Sequence[Real], ordinates: Sequence[Real]) -> None:
        self._train = list(zip(abscissa, ordinates))
        sum_x = 0
        sum_y = 0
        sum_xy = 0
        sum_x_sqr = 0
        count_of_points = len(self._train)
        for x,y in self._train:
            sum_x += x
            sum_y += y
            sum_xy += x * y
            sum_x_sqr += x**2
        sum_x /= count_of_points
        sum_y /= count_of_points
        sum_x_sqr /= count_of_points
        sum_xy /= count_of_points
        self._k = (sum_xy - sum_x * sum_y) / (sum_x_sqr - sum_x**2)
        self._b = (sum_y - self._k * sum_x)
        pass

    def predict(self, abscissa: Union[Real, Sequence[Real]]) -> list:
        if isinstance(abscissa, list):
            return [self._k * x + self._b for x in abscissa]
        else: return self._k * abscissa + self._b
