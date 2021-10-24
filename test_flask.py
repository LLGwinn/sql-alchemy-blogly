from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):

    def setUp(self):
        """ Add test user """

        User.query.delete()

        user = User(first_name="TestFirst", 
                    last_name="TestLast", 
                    image_url="https://images.unsplash.com/photo-1518020382113-a7e8fc38eac9?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=417&q=80")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """ Remove leftover db transactions """

        db.session.rollback()

    def test_home_page(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code,302)
            self.assertEqual(response.location,'http://localhost/users')

    def test_show_all_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('TestFirst', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<button class="btn btn-danger btn-sm" type="submit">Delete</button>', html)

    def test_add_user_form(self):
        with app.test_client() as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<form method='POST'>", html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {'first-name':'TestFirst2', 'last-name':'TestLast2', 'img-URL':''}
            response = client.post('/users/new', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("TestFirst2 TestLast2", html)

    def test_show_edit_page(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}/edit')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<form method='POST'>", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {'first-name':'TestFirst3', 'last-name':'TestLast3', 'img-URL':''}
            response = client.post(f'/users/{self.user_id}/edit', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("TestFirst3 TestLast3", html)

    def test_delete_user(self):
        with app.test_client() as client:
            d = {'first-name':'TestFirst1', 'last-name':'TestLast1', 'img-URL':''}
            response = client.post(f'/users/{self.user_id}/delete', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn("TestFirst1 TestLast1", html)


