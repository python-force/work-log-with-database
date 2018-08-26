import datetime
from peewee import *

db = SqliteDatabase('catalogue.db')


class Employee(Model):
    pub_date = DateTimeField(default=datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d'))
    name = CharField(max_length=50)
    task_name = CharField(max_length=50)
    time_spent = IntegerField()
    notes = TextField()

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Employee], safe=True)
