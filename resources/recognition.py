from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from werkzeug.datastructures import FileStorage
import os
import json
import face_recognition
import numpy as np
from models.person import PersonModel


class Recognition(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image',
                        type=FileStorage,
                        location='files',
                        required=True,
                        help="image required"
                        )

    @jwt_required()
    def post(self):
        data = Recognition.parser.parse_args()

        image_file = data['image']
        if image_file:
            loaded_image = face_recognition.load_image_file(image_file)

            # Get face encodings for any people in the picture
            face_locations = face_recognition.face_locations(
                loaded_image, number_of_times_to_upsample=2)

            face_encodings = face_recognition.face_encodings(
                loaded_image, known_face_locations=face_locations)

            if len(face_encodings) == 0:
                return {'message': f'No Person detected in the uploaded image'}, 400

            detected_faces = []

            for saved_data in PersonModel.query.all() :
                data_face_encodings = np.array(json.loads(saved_data.face_encodings))
                if face_recognition.compare_faces([data_face_encodings], face_encodings[0], tolerance=0.6)[0]:
                    detected_faces.append(saved_data.name) 

            return detected_faces[0] if len(detected_faces) > 0 else {'message': 'Faces in image not Recognized.'}

        return {'message': f'No Person Detected in image'}, 400
