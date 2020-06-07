import markdown2 
from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required, current_user
from ..models import Soundbyt, User, Comment, Upvote, Downvote
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
@main.route('/sharepitch', methods=['GET','POST'])
def sharepitch():
    '''
    View share post page function that returns the post sharing page and its data
    '''
    quote = get_quote()
        
    form = PitchForm()
    
    if form.validate_on_submit():
        soundbyt = Soundbyt(category=form.topic.data, soundbyt=form.content.data)
        db.session.add(soundbyt)
        db.session.commit()
    
        return redirect(url_for('main.goToSoundbyts'))
    
    title = 'SixtySec Pitch'
    return render_template('pitch.html', title=title, SharePostForm=form, quote=quote)

# Redirect to Soundbyt page
@main.route('/soundbyts', methods=['GET','POST'])
def goToSoundbyts():
    '''
    View soundbyts page function that returns the pitches page and its details
    '''   
    TechSavyPosts = Soundbyt.query.filter_by(category='TechSavy').all()
    MoneySmartPosts = Soundbyt.query.filter_by(category='MoneySmart').all()
    LifenLaughterPosts = Soundbyt.query.filter_by(category='Life & Laughter').all()
    
    comment_form = CommentForm()
    comments = Comment.query.filter(Comment.soundbyt_id > 0).all()

    
    title = 'SixtySec Pitch'
    return render_template('/blog.html', TechSavyPosts=TechSavyPosts, MoneySmartPosts=MoneySmartPosts, LifenLaughterPosts=LifenLaughterPosts, comments = comments, CommentForm=comment_form, title=title)


@main.route('/newPitch', methods=['POST', 'GET'])
@login_required
def new_pitch():

    #quote = get_quote()

    form = PitchForm()

    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        content = form.content.data
        user_id = current_user
        new_pitch_object = Pitch(post=content, user_id=current_user._get_current_object(
        ).id, category=category, title=title)
        new_pitch_object.save_p()
        return redirect(url_for('main.index'))

    return render_template('pitch.html', form=form)


@main.route('/soundbyts', methods=['GET','POST'])
@login_required
def comment():
    form = CommentForm()
    soundbyt = Soundbyt.query.get(soundbyt_id)
    all_comments = Comment.query.filter_by(soundbyt_id=soundbyt_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        soundbyt_id = soundbyt_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(
            comment=comment, user_id=user_id, soundbyt_id=soundbyt_id)
        new_comment.save_comment()
        
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.goToSoundbyts'))
    
    title='SixtySec Pitch'
    return render_template('blog.html', TechSavyPosts=TechSavyPosts, MoneySmartPosts=MoneySmartPosts, LifenLaughterPosts=LifenLaughterPosts, form=form, pitch=pitch, all_comments=all_comments, title=title)

# user profile page
@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username=name).first()
    user_id = current_user._get_current_object().id
    posts = Pitch.query.filter_by(user_id=user_id).all()
    
    if user is None:
        abort(404)

    title = 'SixtySec Pitch: myProfile'
    return render_template("profile/profile.html", user=user, title=title)

# update profile page - update user bio
@main.route('/user/<name>/updateprofile', methods=['POST', 'GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username=name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_u()
        return redirect(url_for('.profile', name=name))
    return render_template('profile/update.html', form=form)

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


@main.route('/like/<int:id>', methods=['POST', 'GET'])
@login_required
def like(id):
    get_soundbyts = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for soundbyt in get_soundbyts:
        to_str = f'{soundbyt}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index', id=id))
        else:
            continue
    new_vote = Upvote(user=current_user, soundbyt_id=id)
    new_vote.save()
    return redirect(url_for('main.index', id=id))


@main.route('/dislike/<int:id>', methods=['POST', 'GET'])
@login_required
def dislike(id):
    soundbyt = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for soundbyt in soundbyt:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index', id=id))
        else:
            continue
    new_downvote = Downvote(user=current_user, soundbyt_id=id)
    new_downvote.save()
    return redirect(url_for('main.index', id=id))