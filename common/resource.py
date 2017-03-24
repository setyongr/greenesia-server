import ast
from flask_mongorest.views import ResourceView
from flask_mongorest.resources import Resource
from flask_mongorest import operators as ops
from common import model, schema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_refresh_token, create_access_token, get_jwt_identity

class SphereFilter(ops.Operator):
    op = 'geo_within_sphere'
    def prepare_queryset_kwargs(self, field, value, negate):
        if negate:
            return {'__'.join(filter(None, [field, 'not', self.op])): value}
        else:
            val = ast.literal_eval(value)
            val[1] = val[1] / 6378.1
            return {'__'.join(filter(None, [field, self.op])): val}

class EventResource(Resource):
    document = model.Event
    schema = schema.Event
    filters = {
        'lokasi': [SphereFilter]
    }

class UserResource(Resource):
    document = model.User
    schema = schema.User
    def create_object(self, data=None, save=True, parent_resources=None):
        data = data or self.data
        data['password'] = generate_password_hash(data['password'])

        return super(UserResource, self).create_object(data, save, parent_resources)

class TakeEventResource(Resource):
    document = model.TakeEvent
    schema = schema.TakeEvent
    related_resources = {
        "event": EventResource,
        "user": UserResource
    }
    filters = {
        'event': [ops.Exact],
        'user': [ops.Exact]
    }
    def get_objects(self, **kwargs):
        self.params['user'] = get_jwt_identity()
        return super(TakeEventResource, self).get_objects(**kwargs)

    def create_object(self, data=None, save=True, parent_resources=None):
        data = data or self.data
        data['user'] = model.User.objects(id=get_jwt_identity())[0]

        return super(TakeEventResource, self).create_object(data, save, parent_resources)


class RewardResource(Resource):
    document = model.Reward
    schema = schema.Reward


class TakeRewardResource(Resource):
    document = model.TakeReward
    schema = schema.TakeReward
    related_resources = {
        "reward": RewardResource,
        "user": UserResource
    }
    filters = {
        'reward': [ops.Exact],
        'user': [ops.Exact]
    }

    def get_objects(self, **kwargs):
        self.params['user'] = get_jwt_identity()
        return super(TakeRewardResource, self).get_objects(**kwargs)

    def create_object(self, data=None, save=True, parent_resources=None):
        data = data or self.data
        data['user'] = model.User.objects(id=get_jwt_identity())[0]

        return super(TakeRewardResource, self).create_object(data, save, parent_resources)


class OrganizedEventResource(Resource):


    document = model.Event
    schema = schema.Event
    filters = {
        'lokasi': [SphereFilter],
        'organizer': [ops.Exact]
    }

    def get_objects(self, **kwargs):
        self.params['organizer'] = get_jwt_identity()
        return super(OrganizedEventResource, self).get_objects(**kwargs)
  
class MyProfileResource(Resource):
    document = model.User
    schema = schema.User

        
class AttendantResource(Resource):
    document = model.TakeEvent
    schema = schema.TakeEvent
    related_resources = {
        "event": EventResource,
        "user": UserResource
    }
    filters = {
        'event': [ops.Exact],
        'user': [ops.Exact]
    }

    # def update_object(self, obj, data=None, save=True, parent_resources=None):
    #     data = data or self.data
    #     # data['status'] = True
    #     # print(data)
    #     return super(AttendantResource, self).update_object(data, save, parent_resources)