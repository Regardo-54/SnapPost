from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from main import db
from main.models import Post,User
from main.posts.forms import Posts
from main.posts.utils import save_picture_post

posts = Blueprint('posts',__name__)

@posts.route('/new_post',methods=['GET','POST'])
def new_post():
    form = Posts()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,user_id = current_user.id)
        if form.image.data:
            picture_file = save_picture_post(form.image.data)
            post.image = picture_file
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('others.home'))
    return render_template('new_post.html',title='New Post',form=form,legend='Create a New Post')

@posts.route('/post/<int:post_id>',methods=['GET','POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post=post)

@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = Posts()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html',title='New Post',form=form,legend='Update Post')

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('others.home'))

@posts.route("/user/<int:user_id>")
def user_post(user_id):
    page_num = request.args.get('page',1,type=int)
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page_num,per_page=2)
    return render_template('user_post.html',posts = posts,title = "Posts",user=user)
