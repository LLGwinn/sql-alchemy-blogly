from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """ Show 5 most recent posts """
    q = Post.query
    all_posts = q.order_by(Post.created_at.desc())
    recent_posts = all_posts.limit(5)

    return render_template('/home.html', recent_posts=recent_posts)

@app.route('/users')
def show_all_users():
    """ Shows list of all users in db """
    users = User.query.all()

    return render_template('user_list.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """ Shows details for user with given user_id """
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()

    return render_template('user_detail.html', user=user, posts=posts)

@app.route('/users/new')
def add_user_form():
    """ Display form to add a new user """

    return render_template('add_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """ Create a new user with form data """
    first = request.form['first-name']
    last = request.form['last-name']
    photo = request.form['img-URL']

    new_user = User(first_name=first, last_name=last, image_url=photo)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """ Show form to edit user data """
    user = User.query.get(user_id)
    
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """ Edit data for an existing user """
    user = User.query.get(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-URL']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """ Delete user from db """
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """ Display form to create a new post """
    user = User.query.get(user_id)
    tag_options = Tag.query.all()

    return render_template('new_post_form.html', user=user, tag_options=tag_options)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """ Add post to db for this user """
    user = User.query.get(user_id)

    title = request.form['title']
    content = request.form['content']
    tag_names = request.form.getlist('name')

    new_post = Post(title=title, content=content, user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    for tag_name in tag_names:
        t = Tag.query.filter(Tag.name == tag_name).all()
        new_post_tag = PostTag(post_id=new_post.id, tag_id=t[0].id)
        
        db.session.add(new_post_tag)
        db.session.commit()
    
    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """ Show details of post with given id """
    post = Post.query.get(post_id)
    nice_date = post.format_date
    tags = post.tags

    return render_template('/post_detail.html', post=post, post_date=nice_date, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """ Display form to edit post with given id """
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    post_tags = post.tags

    return render_template('/edit_post.html', post=post, tags=tags, post_tags=post_tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """ Edit data for an existing post """
    post = Post.query.get(post_id)

    post.title = request.form['title']
    post.content = request.form['content']
    checked_tags = request.form.getlist('name')
    post.tags = []


    for tag in checked_tags:
        t = Tag.query.filter(Tag.name == tag).all()
        post.tags.append(t[0])

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """ Delete post from db """
    post = Post.query.get(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def list_tags():
    """ Lists all tags, with links to the tag detail page """
    tags = Tag.query.all()

    return render_template('tag_list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """ Show detail about a tag """
    tag = Tag.query.get(tag_id)
    posts = tag.posts

    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new')
def show_tag_form():
    """ Show form to add a new tag """

    return render_template('add_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_new_tag():
    """ Retrieve tag form data, add tag to db """
    name = request.form['name']

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit_form(tag_id):
    """ Show form to edit a tag """
    tag = Tag.query.get(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """ Edit details for given tag """
    tag = Tag.query.get(tag_id)

    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """ Delete a tag """
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')



