from cleancat import *
from common import model

class User(Schema):
    email = Email(required=True)
    password = String(required=True)
    nama = String(required=True)
    alamat = String(required=True)
    tipe = String(required=True)
    message_token = String(required=False)
    point = Integer()

class Event(Schema):
    nama = String(required=True)
    deskripsi = String(required=True)
    tanggal = DateTime(required=True)
    gambar = String(required=True)
    alamat = String(required=True)
    lokasi = List(Field(), required=True)
    organizer = MongoReference(model.User, required=False)

class TakeEvent(Schema):
    user = MongoReference(model.User, required=False)
    event = MongoReference(model.Event)
    status = Bool()

class Reward(Schema):
    nama = String()
    gambar = String()
    min_point = Integer()

class TakeReward(Schema):
    user = MongoReference(model.User, required=False)
    reward = MongoReference(model.Reward)
    processed = Bool()