import markdown2 
from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required, current_user
from ..models import Pitch, User, Comment, Upvote, Downvote
from .forms import UpdateProfile, PitchForm, CommentForm
from .. import db, photos
from ..requests import get_quote


#Views

# home page
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    quote = get_quote()
    
    title = 'SixtySec Pitch'
    return render_template('index.html', title=title, quote= quote)

# share pitchposts 
@main.route('/pitch/', methods=['GET','POST'])
@login_required
def new_pitch():
    '''
    View pitch page function that returns the post sharing page and its data
    '''
    quote = get_quote()
        
    form = PitchForm()
    
    if form.validate_on_submit():
          category = form.category.data
          pitch = form.pitch.data
          comment = form.comment.data

          new_pitch = Pitches(title = title, category = category, pitch = pitch, user_id=current_user_id)

          title = 'New Pitch'

          new_pitch.save_pitch()

          return redirect(url_for('main.index'))
          db.session.add(new_pitch)
          db.session.commit()

          return redirect(url_for('main.index'))
    
    title = 'SixtySec Pitch'
    return render_template('pitch.html', title=title, PitchForm=form, quote=quote)

@main.route('/comments/<id>', methods=['GET','POST'])
@login_required
def postComments(id):
    '''
    View comments function that returns the blogposts page with the posted comments
    '''
    print('===================================================')
    
    comment = Comments.get_comment(id)
        
    print('===================================================')

    print(comment)
    title = 'comments'
    
    title='SixtySec Pitch'
    return render_template('comments.html', form = form, postComments = comment, title=title)

@main.route('/new_comment/<int:pitch_id>', methods = ['GET', 'POST'])
@login_required
def new_comment(pitch_id):
    pitches = Pitch.query.filter_by(id = pitch_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comments(comment=comment,user_id=current_user.id, pitch_id=pitch_id)


        new_comment.save_comment()


        return redirect(url_for('main.index'))
    title='New Pitch'
    return render_template('new_comment.html',title=title,comment_form = form,pitch_id=pitch_id)

# user profile page
@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username=name).first()
    #user_id = current_user._get_current_object().id
    #posts = Pitch.query.filter_by(user_id=user_id).all()
    
    if user is None:
        abort(404)

    title = 'SixtySec Pitch: myProfile'
    return render_template("profile/profile.html", user=user, title=title)

# update profile page - update user bio
@main.route('/user/<name>/updateprofile', methods=['GET', 'POST'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username=name).first()
    
    if user == None:
        abort(404)
    
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_user()

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', name=name))
    
    title = 'SixtySec Pitch'
    return render_template('profile/update.html', form=form, user = user, title =title)

# update prof pic
@main.route('/user/<name>/update/pic', methods=['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username=name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', name=name))


@main.route('/upvote/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))



@main.route('/downvote/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id= pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))