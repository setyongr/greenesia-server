import os
import datetime
from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest
from flask_mongorest.views import ResourceView
from flask_mongorest.resources import Resource
from flask_mongorest import operators as ops
from flask_mongorest import methods
from flask_mongorest.authentication import AuthenticationBase

from flask_jwt_extended import JWTManager, jwt_required, create_refresh_token, create_access_token, get_jwt_identity, jwt_refresh_token_required

from common.resource import *
from common import model
from werkzeug.security import generate_password_hash, check_password_hash
from admin import admin as admin_blueprint

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static'
app.secret_key = 'super_duper_secret_key'
app.config.update(
    MONGODB_HOST = 'ds117830.mlab.com',
    MONGODB_PORT = 17830,
    MONGODB_DB = 'greenesia',
    MONGODB_USERNAME = 'greenesia',
    MONGODB_PASSWORD = 'secret',
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(weeks=30) #FIX ME: Our client hasn't implement refresh token, remove this
)

jwt = JWTManager(app)

db = MongoEngine(app)
api = MongoRest(app)

app.register_blueprint(admin_blueprint, url_prefix='/admin')

class ApiKeyAuthentication(AuthenticationBase):
    @jwt_required
    def authorized(self):
        return True

@app.route('/login/', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    for user in model.User.objects(email=email):
        if check_password_hash(user.password, password):
            ret = {
                'access_token': create_access_token(identity=str(user.id)),
                'refresh_token': create_refresh_token(identity=str(user.id))
            }
            return jsonify(ret), 200

    return jsonify({'msg': 'Bad request'}), 400
    
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
        'refresh_token': create_refresh_token(identity=current_user)        
    }
    return jsonify(ret), 200


@api.register(name='user', url='/user/')
class UserView(ResourceView):
    # authentication_methods = [ApiKeyAuthentication]
    resource = UserResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

@api.register(name='event', url='/event/')
class EventView(ResourceView):
    authentication_methods = [ApiKeyAuthentication]
    resource = EventResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

@api.register(name='takeevent', url='/take_event/')
class TakeEventView(ResourceView):
    authentication_methods = [ApiKeyAuthentication]
    resource = TakeEventResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]


@api.register(name='reward', url='/reward/')
class RewardView(ResourceView):
    authentication_methods = [ApiKeyAuthentication]
    resource = RewardResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]


@api.register(name='takereward', url='/take_reward/')
class TakeRewardView(ResourceView):
    authentication_methods = [ApiKeyAuthentication]
    resource = TakeRewardResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

@api.register(name='my', url="/my/")
class MyProfileView(ResourceView):
    authentication_methods = [ApiKeyAuthentication]
    resource = MyProfileResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]
    
    def get(self, **kwargs):
        kwargs['pk'] = get_jwt_identity()
        return super(MyProfileView, self).get(**kwargs)

@api.register(name='organizer', url="/organizer/event/")
class OrganizerEventView(ResourceView):
    authentication_methods = [ApiKeyAuthentication]
    resource = OrganizedEventResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]

@api.register(name='attendant', url="/organizer/attendant/")
class AttendantView(ResourceView):
    authentication_methods = [ApiKeyAuthentication]
    resource = AttendantResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List, methods.Delete]


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
