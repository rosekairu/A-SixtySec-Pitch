from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,ValidationError
from wtforms.validators import Required,Email,EqualTo
from ..models import User



class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()], render_kw={"placeholder": "e.g JaneDoe@pitchtoday.com"})
    password = PasswordField('Password',validators =[Required()], render_kw={"placeholder": "Your password"})
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(), Email()], render_kw={"placeholder": "Enter your email address"})
    username = StringField('Enter your username',validators = [Required()], render_kw={"placeholder": "Enter your prefered username"})
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')], render_kw={"placeholder": "Prefered password"})
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
                if User.query.filter_by(email =data_field.data).first():
                    raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')