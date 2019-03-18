from . import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(255))
    email = db.Column(db.String(80), unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.userid)  # python 2 support
        except NameError:
            return str(self.userid)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
    
class UserProfileNew(db.Model):
    id = db.Column(db.String(7), primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    gender = db.Column(db.String(10))
    email = db.Column(db.String(80))
    location = db.Column(db.String(180))
    bio = db.Column(db.String(255))
    created = db.Column(db.DateTime())
    pic = db.Column(db.String(80))
    
    def __init__(self, fName, lName, email, location, bio, image, gender, created):
        self.first_name = fName
        self.last_name = lName
        self.gender = gender
        self.email = email
        self.location = location
        self.bio = bio
        self.created = created
        self.image = image
        