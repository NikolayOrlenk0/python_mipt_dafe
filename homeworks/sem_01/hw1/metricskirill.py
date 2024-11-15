from uuid import UUID
from typing import Sequence


class PeriodActiveUsers:
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
        self._last_session = {} #Создаём словарь в котором будем хранить пару UUID: кол-во дней с последнего визита

        if accumulation_period < 1: #Проверяем, чтобы accumulation_period был больше 1. Вызываем исключение, если accumulation_period меньше 1
            raise(ValueError(f'bad accumulation_period: {accumulation_period}'))
        
        self._accumulation_period = round(accumulation_period) #Сохраняем период рассчёта метрики

    def add_active_users_for_curr_day(self, users: Sequence[UUID]) -> None:
        """
        Обновляет метрику на основании данных о посещении ресурса для текущего дня.

        Args:
            users: последовательность UUID пользователей, посетивших ресурс
                в данный день.
        """
        for uuid in users:  #Обходим список пользователей, посетивших ресурс в данный день, и обнуляем им счетчик кол-ва дней с последнего посещения или добавляем их в нашу "базу данных"
            self._last_session[uuid] = 0
        buffer = dict(self._last_session) #Копируем наш словарь, т.к. его длина может быть изменена в теле цикла
        for uuid in self._last_session: 
            if self._last_session[uuid] >= self._accumulation_period: #Если пользователь слишком давно не посещал ресур, удаляем его для экономии памяти, иначе увеличиваем его счётчик на один
                buffer.pop(uuid)
            else:
                buffer[uuid] += 1
        self._last_session = dict(buffer) #Сохраняем изменения

    @property
    def unique_users_amount(self) -> int:
        """Число уникальных пользователей за последние accumulation_period дней."""
        return len(self._last_session) #Длина нашего словаря = кол-во пользователей, попавших в метрику

    @property
    def accumulation_period(self) -> int:
        """Период расчета метрики: accumulation_period."""
        return self._accumulation_period #Возвращаем заданный период сбора метрики


#Тесты

#Что если accumulation_period < 1 или вовсе не число
try:
    bad_arg = PeriodActiveUsers(-2)
    bad_arg = PeriodActiveUsers('vehicale')
except Exception:
    print('First test passed')

#Проверка округления accumulation_period
round_test = PeriodActiveUsers(1.3)
assert round_test.accumulation_period == round(1.3)
round_test = PeriodActiveUsers(1.6)
assert round_test.accumulation_period == round(1.6)
print('Second test passed')

#Нормальная работа алгоритма
period = 3
metrica = PeriodActiveUsers(period)
uuid_list = [l for l in 'qwerty1367']

for i in range(10 + period):
    metrica.add_active_users_for_curr_day(uuid_list[i::])
    if i >= period:
        assert metrica.unique_users_amount == 9 + period - i
print('Third test passed')

