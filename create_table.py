import datetime
from model import *

"""  Создание таблиц (объектов) в базе данных"""

with db:
    
    db.create_tables([Own_transport, Commercial_transport])

print('DONE')
