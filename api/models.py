from peewee import *

db = SqliteDatabase("myshop.db")


class BaseClass(Model):
    class Meta:
        database = db


class Users(BaseClass):
    email = CharField(max_length=50)
    password = CharField(max_length=60)


class Products(BaseClass):
    name = CharField()
    price = IntegerField()
    description = TextField()
    kategory = CharField()
    city = CharField()
    number = CharField()
    email = CharField()
    date = DateField()
    time = TimeField()
    image = CharField()


db.connect()  # Ma'lumotlar bazasiga ulan!
db.create_tables([Users, Products])  # Jadvallarni yarat!
