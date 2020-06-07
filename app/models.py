from . import db,login_manager
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
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())

    pass_secure = db.Column(db.String(255))
    
    soundbyts = db.relationship('Soundbyt',backref = 'user',lazy="dynamic")
    
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    upvote = db.relationship('Upvote', backref='user', lazy='dynamic')
    downvote = db.relationship('Downvote', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'

class Soundbyt(db.Model):
    __tablename__ = 'soundbyts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    soundbyt = db.Column(db.String(700))
    category = db.Column(db.String(255), index=True, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='pitch', lazy='dynamic')
    upvote = db.relationship('Upvote', backref='pitch', lazy='dynamic')
    downvote = db.relationship('Downvote', backref='pitch', lazy='dynamic')
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def save_soundbyt(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Pitch {self.soundbyt}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    soundbyt_id = db.Column(db.Integer, db.ForeignKey(
        'soundbyts.id'), nullable=False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, soundbyt_id):
        comments = Comment.query.filter_by(soundbyt_id=soundbyt_id).all()

        return comments

    def __repr__(self):
        return f'comment:{self.comment},{self.users_id}, {self.soundbyt_id}'


class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    soundbyt_id = db.Column(db.Integer, db.ForeignKey('soundbyts.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls, id):
        upvote = Upvote.query.filter_by(soundbyt_id=id).all()
        return upvote

    def __repr__(self):
        return f'{self.user_id}:{self.soundbyt_id}'


class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    soundbyt_id = db.Column(db.Integer, db.ForeignKey('soundbyts.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls, id):
        downvote = Downvote.query.filter_by(soundbyt_id=id).all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.soundbyt_id}'


