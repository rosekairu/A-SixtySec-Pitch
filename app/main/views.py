import markdown2 
from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required, current_user
from ..models import Pitch, User, Comment, Upvote, Downvote,PhotoProfile
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
    
    pitches = Pitch.query.all()
    job = Pitch.query.filter_by(category='Job').all()
    event = Pitch.query.filter_by(category='Events').all()
    advertisement = Pitch.query.filter_by(category='Advertisement').all()

    title = 'SixtySec Pitch'
    return render_template('index.html', title=title, quote= quote, event=event, pitches=pitches, advertisement=advertisement)


# share pitch 
@main.route('/create_new', methods=['POST', 'GET'])
@login_required
def new_pitch():

    quote = get_quote()
    form = PitchForm()
    
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_pitch_object = Pitch(post=post, user_id=current_user._get_current_object(
        ).id, category=category, title=title)
        new_pitch_object.save_pitch()
        return redirect(url_for('main.index'))
    
    title = 'SixtySec Pitch'
    return render_template('pitch.html', form=form, title=title,  quote=quote)
    

# Redirect to pitch page
@main.route('/comment/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(
            comment=comment, user_id=user_id, pitch_id=pitch_id)
        new_comment.save_c()
        return redirect(url_for('.comment', pitch_id=pitch_id))

    
    title = 'SixtySec Pitch'
    return render_template('comment.html', title=title, form=form, pitch=pitch, all_comments=all_comments)
    

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
    pitch = Downvote.query.filter_by(pitch_id= pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))