from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from werkzeug.datastructures import FileStorage
import os
import json
import face_recognition
from models.person import PersonModel


class Person(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image',
                        type=FileStorage,
                        location='files',
                        required=True,
                        help="person image required"
                        )

    @jwt_required()
    def get(self, name):
        person = PersonModel.find_person_by_name(name)
        return {'face encodings': person.face_encodings} if person else {'message': f'No Person found with name {name}'}, 404

    @jwt_required()
    def post(self, name):
        old_person = PersonModel.find_person_by_name(name)
        if old_person:
            return {'message': f'Person with same name {name} already exists'}, 400

        data = Person.parser.parse_args()

        image_file = data['image']
        if image_file:
            filename = f"{name}.jpg"
            image_file.save(os.path.join('static', filename))

            image = face_recognition.load_image_file(
                os.path.join('static', filename))
            face_encodings = face_recognition.face_encodings(image)

            if len(face_encodings) == 0:
                return {'message': f'No Person detected in the uploaded image'}, 400

            new_person = PersonModel(name,face_encodings = json.dumps(face_encodings[0].tolist()) )
            return new_person.upsert(), 201

        return {'message': f'No Person Detected in image'}, 400

    @jwt_required()
    def delete(self, name):
        person = PersonModel.find_person_by_name(name)
        if not person:
            return {'message': f'No Person with name {name} found.'}, 404

        person.delete()
        return {'message': f'person with name {name} deleted.'}


class PersonList(Resource):
    @jwt_required()
    def get(self):
        return {'persons': [person.name for person in PersonModel.query.all()]}
