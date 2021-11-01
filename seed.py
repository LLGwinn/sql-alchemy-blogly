""" Seed data for blogly db """

from models import User, Post, Tag, db 
from app import app

# Create table
db.drop_all()
db.create_all()

# Clear table
User.query.delete()

# Create users
user1 = User(first_name='Strawberry', last_name='Pancake')
user2 = User(first_name='Blueberry', last_name='Pancake', image_url='https://images.unsplash.com/photo-1634500242645-151910ed2a4a?ixid=MnwxMjA3fDB8MHx0b3BpYy1mZWVkfDExfHRvd0paRnNrcEdnfHxlbnwwfHx8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60')
user3 = User(first_name='Some', last_name='Gal', image_url='https://images.unsplash.com/photo-1634928077932-574b1d63c145?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=387&q=80')

# Add users to db
db.session.add_all([user1, user2, user3])
db.session.commit()

# Create posts
post1 = Post(title='First Post!', content='Oh, hai.', user_id=user1.id)
post2 = Post(title='Yet Another Post', content="Here's more content.", user_id=user1.id)
post3 = Post(title='Flask is Awesome!', content='Just need more practice.', user_id=user2.id)

# Add posts to db
db.session.add_all([post1, post2, post3])
db.session.commit()

# Create tags
tag1 = Tag(name='funny')
tag2 = Tag(name='boring')
tag3 = Tag(name='whatever')


# Add tags to db
db.session.add_all([tag1, tag2, tag3])
db.session.commit()