from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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

    return render_template('new_post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """ Add post to db for this user """
    user = User.query.get(user_id)

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user.id)

    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """ Show details of post with given id """
    post = Post.query.get(post_id)
    nice_date = post.format_date

    return render_template('/post_detail.html', post=post, post_date=nice_date)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """ Display form to edit post with given id """
    post = Post.query.get(post_id)

    return render_template('/edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """ Edit data for an existing post """
    post = Post.query.get(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

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



