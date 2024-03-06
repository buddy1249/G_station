import datetime
from model import *


with db:
    """Удаление данных выборочно по id:"""
    a = int(input('Начало id: '))
    b = int(input('Окончание id: '))
    for i in range(a, b):
        print(i)
        query = Own_transport.delete().where(Own_transport.id == i).execute()


print('DONE')


