from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)               
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    image_url = db.Column(db.Text, nullable=True, default='no image available')
    
    def __repr__(self):
        u = self
        return f'<User id:{u.id} Name:{u.first_name} {u.last_name}>'

    
def connect_db(app):
    db.app = app
    db.init_app(app)

