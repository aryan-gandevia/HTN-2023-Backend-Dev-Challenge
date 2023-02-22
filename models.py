from app import db

# table for all the applicants
class Applicant(db.Model):
    __tablename__ = 'applicant' # table name

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String, unique=True)
    company = db.Column(db.String)
    
    # One to many relationships
    skills = db.relationship("Skills", cascade="all, delete-orphan", passive_deletes=True)
    events = db.relationship("Events", cascade="all, delete-orphan", passive_deletes=True)

# table for all the skills
class Skills(db.Model):
    __tablename__ = 'skills' # table name

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))

# table for all the events
class Events(db.Model):
    __tablename__ = 'events' # table name

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String)
    eType = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))