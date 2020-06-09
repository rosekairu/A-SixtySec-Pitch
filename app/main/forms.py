from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,TextAreaField,RadioField,SubmitField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class PitchForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	description = TextAreaField("What would you like to pitch ?",validators=[Required()])
	category = RadioField('Label', choices=[ ('promotionpitch','promotionpitch'), ('interviewpitch','interviewpitch'),('pickuplines','pickuplines'),('productpitch','productpitch')],validators=[Required()])
	submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
	description = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField()

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you...',validators = [Required()])
    submit = SubmitField('Submit')

class UpvoteForm(FlaskForm):
	submit = SubmitField()

class Downvote(FlaskForm):
	submit = SubmitField()