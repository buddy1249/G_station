from peewee import *
import datetime

# Set DataBase


db = SqliteDatabase('database02_2024.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Own_transport(BaseModel):
    date = CharField()
    name = CharField()
    waybill = CharField()
    driver = CharField()
    amount = FloatField()
    column = CharField()
    note = CharField()

    class Meta():
        db_table = 'own'       


class Commercial_transport(BaseModel):
    date = CharField()
    name = CharField()
    amount = FloatField()
    money = FloatField()
    note = CharField()


    class Meta():
        db_table = 'commercial'
        
        

        
        
