import mongoengine
from mongoengine import Document, StringField, IntField

mongoengine.connect("event", host="mongodb://localhost:27017/event")


class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)

    meta = {"collection": "Users"}


class Faculty(Document):
    name = StringField(required=True)
    roll_no = StringField(required=True, unique=True)
    designation = StringField(required=True)
    image = StringField(required=True)

    meta = {"collection": "Faculty"}


class Student(Document):
    name = StringField(required=True)
    roll_no = StringField(required=True, unique=True)
    image = StringField(required=True)

    meta = {"collection": "Students"}


class TimeTable(Document):
    year = IntField(required=True)
    image = StringField(required=True)

    meta = {"collection": "TimeTable"}


class Notes(Document):
    year = IntField(required=True)
    subject_code = StringField(required=True)
    notes = StringField(required=True)

    meta = {"collection": "Notes"}


class Achievement(Document):
    Event_name = StringField(required=True)
    level = StringField(required=True)
    organization = StringField(required=True)
    member = IntField(required=True)
    date = StringField(required=True)
    Overall = StringField(required=True)
    event_image = StringField(required=True)
    participation_image = StringField(required=True)

    meta = {"collection": "Achievements"}


class Event(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    date = StringField(required=True)
    image = StringField(required=True)
    meta = {"collection": "Events"}


class Work(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    deadline = StringField(required=True)
    year = IntField(required=True)
    meta = {"collection": "Works"}
