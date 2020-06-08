import markdown2 
from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required, current_user
from ..models import Blogpost, User, Comment, Upvote, Downvote,PhotoProfile
from .forms import UpdateProfile, SharePostForm, CommentForm
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



# share blogpost 
@main.route('/sharepost', methods=['GET','POST'])
def sharepost():
    '''
    View share post page function that returns the post sharing page and its data
    '''
    quote = get_quote()
        
    form = SharePostForm()
    # blogposts = Blogpost.query.all()
    
    if form.validate_on_submit():
        blogpost = Blogpost(category=form.topic.data, blogpost=form.content.data)
        db.session.add(blogpost)
        db.session.commit()
    
        return redirect(url_for('main.goToBlogposts'))
    
    title = 'SixtySec Pitch'
    return render_template('sharepost.html', title=title, SharePostForm=form, quote=quote)
    

# Redirect to blogpost page
@main.route('/blogposts', methods=['GET','POST'])
def goToBlogposts():
    '''
    View blogposts page function that returns the pitches page and its details
    '''   
    TechSavyPosts = Blogpost.query.filter_by(category='TechSavy').all()
    MoneySmartPosts = Blogpost.query.filter_by(category='MoneySmart').all()
    LifenLaughterPosts = Blogpost.query.filter_by(category='Life & Laughter').all()
    
    comment_form = CommentForm()
    # comments = Blogpost.query.filter_by(blogpost_id=id)
    # comments = Comment.query.filter_by(blogpost_id=id).first()
    comments = Comment.query.filter(Comment.blogpost_id > 0).all()

    
    title = 'SixtySec Pitch'
    return render_template('/blogposts.html', TechSavyPosts=TechSavyPosts, MoneySmartPosts=MoneySmartPosts, LifenLaughterPosts=LifenLaughterPosts, comments = comments, CommentForm=comment_form, title=title)


#posting comments
@main.route('/blogposts', methods = ['GET','POST'])
def postComments():
    '''
    View comments function that returns the blogposts page with the posted comments
    '''
    print('===================================================')
    
    commentform = CommentForm()
        
    print('===================================================')
    
    if commentform.validate_on_submit():
        comment = Comment(comment=commentform.comment.data, blogpost_id=3, users_id = 2)
        print(comment)
        print('===================================================')
        db.session.add(comment)
        db.session.commit()
    
        return redirect(url_for('main.goToBlogposts'))
    
    title='SixtySec Pitch'
    return render_template('/blogposts.html', TechSavyPosts=TechSavyPosts, MoneySmartPosts=MoneySmartPosts, LifenLaughterPosts=LifenLaughterPosts, comment = comment, CommentForm=comment_form, title=title)
    

@main.route('/upvote/<pitch_id>', methods=['POST', 'GET'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('.postComments'))


    new_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))



@main.route('/downvote/<pitch_id>', methods=['POST', 'GET'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch = Downvote.query.filter_by(pitch_id= pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('.postComments'))


    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))


# user profile page
@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username=name).first()
    
    
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


