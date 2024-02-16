from peewee import AutoField, CharField, IntegerField, TextField
from playhouse.shortcuts import model_to_dict

from db.models import BaseModel


class History(BaseModel):
    id = AutoField()
    role = CharField()
    message = TextField()
    timestamp = IntegerField()
    # xiaomi, github-co-pilot, moonshot, etc
    provider = CharField()

    def to_dict(self):
        return model_to_dict(self)
