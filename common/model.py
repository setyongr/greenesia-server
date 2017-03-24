from mongoengine import *

class User(Document):
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    nama = StringField()
    alamat = StringField()
    tipe = StringField()
    message_token = StringField()
    point = IntField()

class Event(Document):
    nama = StringField()
    deskripsi = StringField()
    tanggal = DateTimeField()
    gambar = StringField()
    alamat = StringField()
    lokasi = PointField(auto_index=False)
    organizer = ReferenceField(User)

    meta = {
        'indexes': [
                [
                    ("location", "2dsphere"), 
                ]
            ]
    }

class TakeEvent(Document):
    user = ReferenceField(User)
    event = ReferenceField(Event)
    status = BooleanField()

class Reward(Document):
    nama = StringField()
    gambar = StringField()
    min_point = IntField()

class TakeReward(Document):
    user = ReferenceField(User)
    reward = ReferenceField(Reward)
    processed = BooleanField()
    