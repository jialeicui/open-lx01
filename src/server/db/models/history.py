from peewee import AutoField, CharField, IntegerField, TextField

from db.models import BaseModel


class History(BaseModel):
    id = AutoField()
    role = CharField()
    message = TextField()
    timestamp = IntegerField()
    # xiaomi, github-co-pilot, moonshot, etc
    provider = CharField()
