from uuid import UUID, uuid4
from typing import Sequence
import time


class PeriodActiveUsers:
    _uniq_users: dict[UUID, int]
    _accumulation_period: int
    _current_day: int

    def __init__(self, accumulation_period: int) -> None:
        """
        Инициализирует объект для подсчета числа уникальных пользователей.

        Args:
            accumulation_period: период времени, для которого необходимо подсчитать
                число уникальных пользователей.

        Raises:
            TypeError, если accumulation_period не может быть округлено и использовано
                для получения целого числа.
            ValueError, если после округления accumulation_period - число, меньшее 1.
        """
        self._accumulation_period = round(accumulation_period)
        if self._accumulation_period < 1:
            raise ValueError
        self._uniq_users = {}
        self._current_day = 0
        pass

    def add_active_users_for_curr_day(self, users: Sequence[UUID]) -> None:
        """
        Обновляет метрику на основании данных о посещении ресурса для текущего дня.

        Args:
            users: последовательность UUID пользователей, посетивших ресурс
                в данный день.
        """
        for uuid in users:
            self._uniq_users[uuid] = self._current_day
        self._current_day += 1
        pass


    @property
    def unique_users_amount(self) -> int:
        """Число уникальных пользователей за последние accumulation_period дней."""
        accumulation_period = self._current_day - self.accumulation_period
        for uuid in list(self._uniq_users):
            if self._uniq_users[uuid] < accumulation_period:
                del (self._uniq_users[uuid])
        return len(self._uniq_users)
        pass

    @property
    def accumulation_period(self) -> int:
        """Период расчета метрики: accumulation_period."""
        return self._accumulation_period
        pass
metrica10000 = PeriodActiveUsers(50)
uuid_list10000 = [[0]*10000 for i in range(100)]
print(time.time())
for i in range (100):
    for j in range(10000):
        uuid_list10000[i][j] = uuid4()
print(time.time())
time_start = time.time()
for i in range (100):
    metrica10000.add_active_users_for_curr_day(uuid_list10000[i]) 
    print(time.time())
time_end = time.time()
print(time_end - time_start)
time_s = time.time()
print(metrica10000.unique_users_amount)
time_e = time.time()
print(time_e - time_s)

time_s2 = time.time()


time_e2 = time.time()

print(time_e2 - time_s2)
print(len(metrica10000._uniq_users))
