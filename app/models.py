from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# User model
class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    #category = db.Column(db.String(255), unique = True,index = True)
    #role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")

    pass_secure = db.Column(db.String(255))
    pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
    
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    upvotes = db.relationship('Upvote', backref='user', lazy='dynamic')
    downvotes = db.relationship('Downvote', backref='user', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


class Pitch(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(255))

    comment = db.relationship('Comment', backref='pitch', lazy='dynamic')
    upvote = db.relationship('Upvote', backref='pitch', lazy='dynamic')
    downvote = db.relationship('Downvote', backref='pitch', lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Pitch {self.content}'

# Comment Model
class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(255))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey(
        'pitches.id'))

    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    
    
    @classmethod
    def get_comments(cls, pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()

        return comments

    def __repr__(self):
        return f'comment:{self.comment}'


class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    upvote = db.Column(db.Integer,default=1)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    
    def save_upvotes(self):
        db.session.add(self)
        db.session.commit()

    def add_upvotes(cls,id):
        upvote_pitch = Upvote(user = current_user, pitch_id=id)
        upvote_pitch.save_upvotes()
  
    @classmethod
    def get_upvotes(cls, id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote

    @classmethod
    def get_all_upvotes(cls,pitch_id):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'

class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    downvote = db.Column(db.Integer,default=1)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_downvotes(self):
        db.session.add(self)
        db.session.commit()

    def add_downvotes(cls,id):
        downvote_pitch = Downvote(user = current_user, pitch_id=id)
        downvote_pitch.save_downvotes()

    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    @classmethod
    def get_all_downvotes(cls,pitch_id):
        downvote = Downvote.query.order_by('id').all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'




