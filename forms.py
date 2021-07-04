from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired


class SignUpForm(FlaskForm):
    inputFirstName = StringField('First Name',
                                [DataRequired(message='Please enter your first name!')])

    inputLastName = StringField('Last Name',
                                [DataRequired(message='Please enter your last name!')])

    inputEmail = StringField('Email',
                            [Email(message='Not a valid email address!'),
                                DataRequired(message="Please enter your email!")])

    inputPassword = PasswordField('Password',
                                  [InputRequired(message='Please enter your password!'),
                                    EqualTo('inputConfirmPassword', message='Password does not match!')])

    inputConfirmPassword = PasswordField('Confirm Password')
    submit = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    inputEmail = StringField('Email address',
                             [Email(message='Not a valid email address!'),
                                DataRequired(message='Please enter your email address again!')])

    inputPassword = PasswordField('Password',
                                    [InputRequired(message='Please enter your password!')])

    submit = SubmitField('Sign In')


class TaskForm(FlaskForm):
    inputDescription = StringField('Task Description',
                                   [DataRequired(message="Please enter your task description!")])
    inputPriority = SelectField('Priority', coerce=int)

    submit = SubmitField('Add Task')


class EditTaskForm(FlaskForm):
    inputDescription = StringField('Task Description',
                                   [DataRequired(message="Please enter your task description!")])
    inputPriority = SelectField('Priority', coerce=int)

    submit = SubmitField('Edit Task')