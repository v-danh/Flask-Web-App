from os import path

from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from forms import SignUpForm, SignInForm, TaskForm, EditTaskForm

# Create a base directory...
basedir = path.abspath(path.dirname(__file__))
# print(basedir)

app = Flask(__name__)
app.config["SECRET_KEY"] = 'd54dfaa946a6092642414acc6bf1c199'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)
# Mapping to the database migrate
migrate = Migrate(app, db)
import models


# Routing and Writing the main function
@app.route('/')
@app.route('/logOut')
def main():
    todolist = [
        {"name": "Buy milk", "description": "Buy 2 liters of milk in the supermarket."},
        {"name": "Get money", "description": "Get 500.000 VND from ATM."},
        {"name": "Buy food", "description": "Buy food for the lunch."},
        {
            "name": "Buy some notebooks and books",
            "description": "Buy both them at Bach Dang bookstore.",
        },
        {"name": "And NOTE: Buy vegetable", "description": "Buy much vegetable."},
    ]
    return render_template('index.html', todolist=todolist, title='Home')


# Routing and Writing the addTask function
@app.route('/addTask', methods=['GET', 'POST'])
def addTask():
    _user_id = session.get('user')
    form = TaskForm()
    form.inputPriority.choices = [
        (p.priority_id, p.text) for p in db.session.query(models.Priority).all()
    ]

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()

        if form.validate_on_submit():
            _description = form.inputDescription.data
            _priority_id = form.inputPriority.data
            print('Add task description:', _description)
            print('Add priority id:', _priority_id)
            priority = (
                db.session.query(models.Priority)
                .filter_by(priority_id=_priority_id)
                .first()
            )
            _task_id = request.form['hiddenTaskId']
            if _task_id == "0":
                task = models.Task(
                    user=user, description=_description, priority=priority, complete=False
                )
                db.session.add(task)
                flash('You have successfully added item(s): {}'.format(_description), category='success')
            else:
                task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
                task.description = _description
                task.priority = priority
                flash('You have successfully updated item(s): {}'.format(_description), category='success')

            db.session.commit()
            return redirect('/userHome')

        return render_template('addTask.html', form=form, user=user, title='Add Task')

    return redirect(url_for(''))


# Routing and Writing the updateTask function
@app.route('/updateTask', methods=['GET', 'POST'])
def updateTask():
    _user_id = session.get("user")

    if _user_id:
        _task_id = request.form['hiddenTaskId']

        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            task.complete = not task.complete
            db.session.commit()

        flash('Task item(s) is {} completed!'.format(task.complete), category='success')
        return redirect('/userHome')

    return redirect(url_for(''))


# Routing and Writing the editTask function
@app.route("/editTask", methods=["GET", "POST"])
def editTask():
    _user_id = session.get("user")
    form = EditTaskForm()
    form.inputPriority.choices = [
        (p.priority_id, p.text) for p in db.session.query(models.Priority).all()
    ]

    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        _task_id = request.form['hiddenTaskId']

        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            print('Edit task id', _task_id)
            form.inputDescription.default = task.description
            form.inputPriority.default = task.priority_id
            form.process()

            return render_template(
                'addTask.html', form=form, user=user, task=task, title='Edit Task'
            )

    return redirect(url_for(''))


# Routing and Writing the deleteTask function
@app.route('/deleteTask', methods=['GET', 'POST'])
def deleteTask():
    _user_id = session.get('user')
    if _user_id:
        _task_id = request.form['hiddenTaskId']

        if _task_id:
            task = db.session.query(models.Task).filter_by(task_id=_task_id).first()
            db.session.delete(task)
            db.session.commit()
            print("Deleted task id", _task_id)

        flash('You have successfully deleted item(s)', category='success')
        return redirect("/userHome")

    return redirect(url_for(''))


# Routing and Writing the signUp function
@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()

    # if form.is_submitted()
    if form.validate_on_submit():
        print('Validate on submit.')
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        if db.session.query(models.User).filter_by(email=_email).count() == 0:
            user = models.User(first_name=_fname, last_name=_lname, email=_email)
            user.set_password(_password)
            db.session.add(user)
            db.session.commit()
            return render_template('signUpSuccess.html', user=user)
        else:
            flash('Email {} is already exist!'.format(_email), category='danger')
            return render_template('signUp.html', form=form, title='Sign Up')

    # return render_template('signUp.html')
    print('Not validate on submit.')
    return render_template('signUp.html', form=form, title='Sign Up')


# Routing and Writing the signIn function
@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    form = SignInForm()

    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        user = db.session.query(models.User).filter_by(email=_email).first()
        if user is None:
            flash("Non-exist email address or password!", category='danger')
        else:
            if user.check_password(_password):
                session["user"] = user.user_id
                # return render_template('userHome.html')
                flash('Login successfully for {}'.format(_email), category='success')
                return redirect("/userHome")
            else:
                flash("Login unsuccessfully for {}".format(_email), category='danger')

    return render_template("signIn.html", form=form, title="Sign In")


# Routing and Writing the userHome function
@app.route('/userHome', methods=['GET', 'POST'])
def userHome():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id=_user_id).first()
        #flash('Congratulations, you have successfully logged in!', 'success')
        return render_template('userHome.html', user=user)
    else:
        return redirect('/')


# Routing and Writing the about function
@app.route('/about')
def about():
    return render_template('about.html', title='About')


# Run Server Service
if __name__ == '__main__':
    app.run(debug=True)