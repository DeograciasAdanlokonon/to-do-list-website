from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length


# ToDo: Registration Form
class RegisterForm(FlaskForm):
  username = StringField("Name", validators=[DataRequired(), Length(4, 80)])
  email = EmailField("Email", validators=[DataRequired(), Length(4, 120)])
  password_hash = PasswordField("Password", validators=[DataRequired(), Length(8, 12)])
  confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(8, 12)])
  submit = SubmitField("Sign Up")


# ToDo: Login Form
class LoginForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired(), Length(4, 120)])
  password = PasswordField("Password", validators=[DataRequired(), Length(8, 12)])
  submit = SubmitField("Log in")

# ToDo: New Task Form
class TaskForm(FlaskForm):
  description =  StringField("Description", validators=[DataRequired()])
  submit = SubmitField("Add task")

# ToDo: Edit Task Form
class EditForm(FlaskForm):
  # hidden_id = StringField("Id")
  description =  StringField("Description", validators=[DataRequired()])
  submit = SubmitField("Modify description")