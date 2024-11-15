from uuid import UUID
import metrics


pau = PeriodActiveUsers(accumulation_period=1)
pau.add_active_users_for_curr_day(
    [
        UUID("2509a9eb-2422-4b83-8911-f780eea815bb"),
        UUID("f52fc9b2-2ff2-4419-9f07-22267946b46e"),
    ],
)
assert pau.unique_users_amount == 2


pau = PeriodActiveUsers(accumulation_period=3)
pau.add_active_users_for_curr_day(
    [
        UUID("52d6f353-4dd3-421b-b1c4-c35d2ae9ad66"),
        UUID("3f06aef7-bf3a-41f8-b571-3453a3b27aa9"),
        UUID("b6595baa-a23a-4e22-8656-079f84c7c3a4"),
        UUID("52d6f353-4dd3-421b-b1c4-c35d2ae9ad66"),
        UUID("52d6f353-4dd3-421b-b1c4-c35d2ae9ad66"),
        UUID("b6595baa-a23a-4e22-8656-079f84c7c3a4"),
    ],
)
assert pau.unique_users_amount == 3


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


print(time.time())
metrica10000 = PeriodActiveUsers(10000)
uuid_list10000 = [[]]
uuid_list10000 = [[0]*10000 for i in range(100)]
print(time.time())
for i in range (100):
    for j in range(10000):
        uuid_list10000[i][j]= uuid.uuid4()
print(time.time())
time_start = time.time()
for i in range (100):
    metrica10000.add_active_users_for_curr_day(uuid_list10000[i]) 
    print(time.time())
time_end = time.time()
print(time_end - time_start)
print(metrica10000.unique_users_amount)
