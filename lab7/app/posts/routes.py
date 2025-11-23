from flask import render_template, request, redirect, url_for
from app.posts import bp
from app.posts.forms import PostForm
from app.posts.models import Post, Tag
from app import db

@bp.route("/new", methods=["GET", "POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            author_id=form.author_id.data
        )

        for tag_id in form.tags.data:
            tag = Tag.query.get(tag_id)
            post.tags.append(tag)

        db.session.add(post)
        db.session.commit()
        return redirect("/posts/list")

    return render_template("post_form.html", form=form)

