from flask import render_template, request, redirect, url_for, flash
from . import post_bp
from ..extensions import db
from ..models import Post

@post_bp.route('/posts')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts/index.html', posts=posts)

@post_bp.route('/posts/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('posts.create'))

        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('posts.index'))

    return render_template('posts/create.html')

@post_bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts.index'))
    return render_template('posts/edit.html', post=post)

@post_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'info')
    return redirect(url_for('posts.index'))

