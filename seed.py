""" Seed data for users db """

from models import User, db 
from app import app

# Create table
db.drop_all()
db.create_all()

# Clear table
User.query.delete()

# Add users
test1 = User(first_name='Strawberry', last_name='Pancake')
test2 = User(first_name='Blueberry', last_name='Pancake', image_url='https://images.unsplash.com/photo-1634500242645-151910ed2a4a?ixid=MnwxMjA3fDB8MHx0b3BpYy1mZWVkfDExfHRvd0paRnNrcEdnfHxlbnwwfHx8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60')

# Add to users db
db.session.add(test1)
db.session.add(test2)

db.session.commit()