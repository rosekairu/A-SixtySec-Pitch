from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,TextAreaField,SubmitField
from wtforms.validators import Required
from wtforms import ValidationError

class PitchForm(FlaskForm):
    '''
    The pitch-post sharing form
    '''
    title = StringField('Pitch Title',validators=[Required()])
    category = SelectField('', choices=[('TechSavy', 'TechSavy'), ('MoneySmart','MoneySmart'), ('Life & Laughter', 'Life & Laughter')], validators=[Required()])
    pitch = TextAreaField('', validators=[Required()], render_kw={"placeholder": "Write your story here..."})
    submit = SubmitField('Share') 
    
class CommentForm(FlaskForm):
    comment = TextAreaField('',validators=[Required()], render_kw={"placeholder": "Post your comment here..."})
    submit = SubmitField('Post Comment')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you...',validators = [Required()])
    submit = SubmitField('Submit')