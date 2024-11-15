from typing import Sequence, Union
from numbers import Real

from regressors.regressor_abc import RegressorABC


class NonparametricRegressor(RegressorABC):
    _k: int
    train: list
    def __init__(self, k: int):
        self._k = k
        self.train = []
    def fit(self, abscissa: Sequence[Real], ordinates: Sequence[Real]) -> None:
        self.train = list(zip(abscissa, ordinates))

    def predict(self, abscissa: Union[Real, Sequence[Real]]) -> list:
        if isinstance(abscissa, Real):
            return self._predict(abscissa)
        return [self._predict(x) for x in abscissa]

    def _predict(self, x: Real):

        ro = [(abs(x - xi), yi) for xi, yi in self.train]
        ro.sort()

        h = ro[self._k][0]
        K = [self._K(roi / h) for roi, _ in ro]

        y = sum(ro[i][1] * K[i] for i in range(len(ro)))
        y /= sum(K)
        return y

    @staticmethod
    def _K(x):
        if abs(x) <= 1:
            return 3/4 * (1 - x ** 2)
        return 0