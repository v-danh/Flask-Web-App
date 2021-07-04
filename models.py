from main import db
from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


# Create User class
class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    tasks = relationship('Task', back_populates='user')

    def __repr__(self):
        return '<User full name: {} {}, User email: {}>'.format(self.first_name, self.last_name, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Create Task class
class Task(db.Model):
    task_id = db.Column(db.Integer, Sequence('task_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    priority_id = db.Column(db.Integer, ForeignKey('priority.priority_id'))
    description = db.Column(db.String(255), nullable=False)
    complete = db.Column(db.Boolean)

    # Create relationship between tables
    user = relationship('User', back_populates='tasks')
    priority = relationship('Priority', back_populates='tasks')

    def __repr__(self):
        return '<Task: {} of user {}>'.format(self.description, self.user_id)

    def getPriorityClass(self):
        if self.priority_id == 1:
            return "table-danger"
        elif self.priority_id == 2:
            return "table-warning"
        elif self.priority_id == 3:
            return "table-info"
        elif self.priority_id == 4:
            return "table-primary"
        else:
            return "table-default"


# Create Priority Class
class Priority(db.Model):
    priority_id = db.Column(db.Integer, Sequence('priority_id_seq'), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

    # Create relationship between tables
    tasks = relationship('Task', back_populates='priority')

    def __repr__(self):
        return '<Priority: {} with {}>'.format(self.priority_id, self.text)