from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,TextAreaField,RadioField,SubmitField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class PitchForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    category = SelectField('Category', choices=[('Events', 'Django'), (
        'Job', 'Flask'), ('Advertisement', 'Angular')], validators=[Required()])
    post = TextAreaField('Your Pitch', validators=[Required()])
    submit = SubmitField('Pitch')
    
class CommentForm(FlaskForm):
    description = TextAreaField('',validators=[Required()], render_kw={"placeholder": "Post your comment here..."})
    submit = SubmitField('Post Comment')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you...',validators = [Required()])
    submit = SubmitField('Submit')

class UpvoteForm(FlaskForm):
	submit = SubmitField()

class Downvote(FlaskForm):
	submit = SubmitField()