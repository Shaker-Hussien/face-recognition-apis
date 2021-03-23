from db import db


class PersonModel(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    face_encodings = db.Column(db.JSON)

    def __init__(self, name, face_encodings):
        self.name = name
        self.face_encodings = face_encodings

    @ classmethod
    def find_person_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def upsert(self):
        db.session.add(self)
        db.session.commit()

        return self.name

    def delete(self):
        db.session.delete(self)
        db.session.commit()
