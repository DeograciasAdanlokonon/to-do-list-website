from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, LoginManager, current_user, logout_user
from base import MyDataBase, db, User, Task
from forms import RegisterForm, LoginForm, TaskForm, EditForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sjkds698sjJD46ddilr64qds'
Bootstrap5(app=app)

# Flask Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"

# user loader callback
@login_manager.user_loader
def load_user(user_id):
  return db.get_or_404(User, user_id)

# DataBase configuration
database = MyDataBase(app=app)

#  ToDo: Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
  # initialize refigisterform
  register_form = RegisterForm()

  try:
    # on submit
    if register_form.validate_on_submit():
      username = register_form.username.data
      email = register_form.email.data

      # check password equal
      if register_form.password_hash.data == register_form.confirm_password.data:
        password = generate_password_hash(register_form.password_hash.data, salt_length=8)

        # check if user already exist
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
          # create new user
          new_user = User(
            username=username,
            email=email,
            password_hash = password
          )

          # insert new user in db
          db.session.add(new_user)
          db.session.commit()

          login_user(new_user)

          # head user to home route
          return redirect(url_for('index', logged_in=current_user.is_authenticated))
        else:
          flash('You already have an account with that email. Please, sign in!', 'warning')

          # head user to login page
          return redirect(url_for('login'))

      else:
        flash('Your passwords should be equal', 'danger')
  except Exception as e:
    flash(f'Something went wrong: {e}', 'error')

  return render_template('register.html', form=register_form)

# ToDo: Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
  # initialize login form
  login_form = LoginForm()

  try:
    # if from submitted
    if login_form.validate_on_submit():
      email = login_form.email.data
      password = login_form.password.data

      # check if user exits in db
      result = db.session.execute(db.select(User).where(User.email == email))
      user = result.scalar()

      if user:
        # check password is correct
        if check_password_hash(user.password_hash, password=password):
          # then let user log in
          login_user(user=user)

          flash('Logged in Successfully!', 'success')

          # head user to home page
          return redirect(url_for('index', logged_in=current_user.is_authenticated))
        else:
          flash('Password incorrect! Please, try again', 'warning')
      else:
        flash('The email address does not exist. Please try again!', 'danger')
  except Exception as e:
    flash(f'Something went wrong: {e}', 'danger')

  return render_template("login.html", form=login_form)

# Todo: Logout Route
@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

# Todo: Home Route
@app.route('/', methods=['GET', 'POST'])
def index():
  
  task_form = TaskForm()# initialize new task form
  edit_form = EditForm() # initailize edit form

  # add new task method
  add_task(form=task_form)

  if not current_user.is_authenticated:
    return redirect(url_for('login'))  # send user to login page

  result = db.session.execute(db.select(Task).where(Task.user_id == current_user.id))
  tasks = result.scalars().all()
  return render_template("index.html", tasks=tasks, current_user=current_user, form=task_form, edit_form=edit_form)

# ToDo: Toggle task status route
@app.route('/toggle-task/<int:id>', methods=['GET', 'POST'])
def toggle_task(id):
  task = db.get_or_404(Task, id)

  try:
    task.done = not task.done  # flip the boolean
    db.session.commit()
    
    flash('Task status changed', 'success')

    return redirect(url_for('index'))
  except Exception as e:
    flash(f'Something went wrong: {e}', 'danger')
  
# ToDo: Delete task route
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_task(id):
  task = db.get_or_404(Task, id)

  try:
    db.session.delete(task)
    db.session.commit()

    flash('Task successfully deleted', 'success')

    return redirect(url_for('index'))
  except Exception as e:
    flash(f'Something went wrong: {e}')

# ToDo: Add task method
def add_task(form):
  """Commit a new task in db"""
  try:
    if form.validate_on_submit():
      if current_user.is_authenticated:
        new_task = Task(
        description = form.description.data,
        user_id = current_user.id
      )
        db.session.add(new_task)
        db.session.commit()

        flash('Task successfully added!', 'success')

        return redirect(url_for("index"))
      else:
        flash('You need to login or register to add a task', 'danger')
  except Exception as e:
    flash(f'Somethin went wrong {e}', 'danger ')

  return redirect(url_for('index'))

# ToDo: Edit task status route
@app.route('/edit-task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
  """Updates a task description"""
  task = db.get_or_404(Task, id)

  form = EditForm() # initailize edit form

  try:
    if form.validate_on_submit():
      new_description = form.description.data
      task.description = new_description
      db.session.commit()
      
      flash('Task successfully updated', 'success')

      return redirect(url_for('index'))
  except Exception as e:
    flash(f'Error: {e}', 'danger')
  return redirect(url_for('index'))

# Todo: Profile Route
@app.route('/profile')
@login_required
def profile():
  return render_template('profile.html')

if __name__ == "__main__":
  app.run(debug=True, port=5002)