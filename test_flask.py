from unittest import TestCase

from app import app
from models import db, User, Post

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
        """ Add test users and a post """

        User.query.delete()

        user = User(first_name="TestFirst", 
                    last_name="TestLast", 
                    image_url="https://images.unsplash.com/photo-1518020382113-a7e8fc38eac9?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=417&q=80")
        user2 = User(first_name="Test2First", 
                    last_name="Test2Last", 
                    image_url="")
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        post = Post(title='Test Title', content='Test Content', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post = post
        self.post_id = post.id

    def tearDown(self):
        """ Remove leftover db transactions """

        db.session.rollback()


    def test_home_page(self):
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h2>Test Title</h2>', html)

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
            self.assertIn('<h1>TestFirst TestLast</h1>', html)

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
            d = {'first-name':'TestFirst', 'last-name':'TestLast', 'img-URL':''}
            response = client.post(f'/users/{self.user_id}/delete', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("TestFirst TestLast", html)

    def test_show_post_form(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}/posts/new')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<input type="text" class="form-control" id="title" name="title">', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {'title':'Testing123', 'content':'Testing123 Content'}
            response = client.post(f'/users/{self.user_id}/posts/new', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<li><a href=\'/posts/2\'>Testing123</li>', html)

    def test_show_post_details(self):
        with app.test_client() as client:
            response = client.get(f'/posts/{self.post_id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<h1>{self.post.title}</h1>', html)

    def test_show_edit_post(self):
        with app.test_client() as client:
            response = client.get(f'/posts/{self.post_id}/edit')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<label for="content" class="form-label">Content</label>', html)

    def test_edit_post(self):
        with app.test_client() as client:
            d = {'title':'Testing123', 'content':'Testing123 Content'}
            response = client.post(f'/posts/{self.post_id}/edit', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<h1>Testing123</h1>', html)

    def test_delete_post(self):
        with app.test_client() as client:
            d = {'title':'Test Title', 'content':'Test Content'}
            response = client.post(f'/posts/{self.post_id}/delete', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("Test Title", html)

