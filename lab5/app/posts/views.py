from flask import render_template, request, redirect, url_for, flash, session
from . import post_bp
from .forms import PostForm
from .models import Post
from ..extensions import db
from datetime import datetime

@post_bp.route('/')
def list_posts():
    stmt = Post.query.filter_by(is_active=True).order_by(Post.posted.desc())
    posts = stmt.all()
    return render_template('posts/all_posts.html', posts=posts)

@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        is_active = form.enabled.data
        # publish_date handling
        if hasattr(form, 'publish_date') and form.publish_date.data:
            try:
                publish_date = form.publish_date.data
                if isinstance(publish_date, str):
                    publish_date = datetime.strptime(publish_date, '%Y-%m-%d %H:%M')
            except Exception:
                publish_date = datetime.utcnow()
        else:
            publish_date = datetime.utcnow()

        author = session.get('username', 'Anonymous')

        p = Post(title=title, content=content, category=category, is_active=is_active, author=author, posted=publish_date)
        db.session.add(p)
        db.session.commit()
        flash('Post added successfully', 'success')
        return redirect(url_for('posts.list_posts'))

    return render_template('posts/add_post.html', form=form)

@post_bp.route('/<int:id>')
def detail_post(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/detail_post.html', post=post)

@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    # populate publish_date manually if form uses DateTimeLocalField
    if request.method == 'GET':
        if hasattr(form, 'publish_date') and hasattr(post, 'posted'):
            try:
                form.publish_date.data = post.posted
            except Exception:
                form.publish_date.data = post.posted.strftime('%Y-%m-%d %H:%M')
    if form.validate_on_submit():
        form.populate_obj(post)
        # form publishes date field named publish_date but model uses posted
        if hasattr(form, 'publish_date') and form.publish_date.data:
            pd = form.publish_date.data
            if isinstance(pd, str):
                try:
                    post.posted = datetime.strptime(pd, '%Y-%m-%d %H:%M')
                except Exception:
                    pass
            else:
                post.posted = pd
        db.session.commit()
        flash('Post updated successfully', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))
    return render_template('posts/add_post.html', form=form, post=post)

@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', 'info')
        return redirect(url_for('posts.list_posts'))
    return render_template('posts/delete_confirm.html', post=post)

