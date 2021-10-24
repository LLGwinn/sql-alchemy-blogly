from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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

    return redirect('/users')

@app.route('/users')
def show_all_users():
    """ Shows list of all users in db """
    users = User.query.all()

    return render_template('user_list.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """ Shows details for user with given user_id """
    user = User.query.get_or_404(user_id)

    return render_template('user_detail.html', user=user)

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



