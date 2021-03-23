from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.person import Person, PersonList
from resources.recognition import Recognition


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = "dummySecretKey" #add secret key

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth endpoint for authenticate users

api.add_resource(Recognition, '/api/recognition')
api.add_resource(PersonList, '/api/persons')
api.add_resource(Person, '/api/person/<string:name>')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
