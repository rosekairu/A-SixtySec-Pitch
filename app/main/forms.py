from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,TextAreaField,RadioField,SubmitField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class SharePostForm(FlaskForm):
    '''
    The blog-post sharing form
    '''
    topic = SelectField('', choices=[('TechSavy', 'TechSavy'), ('MoneySmart','MoneySmart'), ('Life & Laughter', 'Life & Laughter')], validators=[Required()])
    content = TextAreaField('', validators=[Required()], render_kw={"placeholder": "Write your story here :)"})
    submit = SubmitField('Share')
    
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