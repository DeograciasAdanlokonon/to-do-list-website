from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import os


# CREATE DATABASE
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


#  TODO: Create a User table for registerd users. PARENT TABLE
class User(UserMixin, db.Model):
  __tablename__ = "users"

  id:Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
  email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
  password_hash: Mapped[str] = mapped_column(String(250), nullable=False)
  created_at: Mapped[str] = mapped_column(DateTime, default=datetime.now)
  tasks = relationship("Task", back_populates="user")


class Task(db.Model):
  __tablename__ = "tasks"

  #  One-to-Many realation between User and Task
  user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
  user = relationship("User", back_populates="tasks")

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  description: Mapped[str] = mapped_column(Text, nullable=False)
  done: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[str] = mapped_column(DateTime, default=datetime.now)


class MyDataBase:
  """Initiate db"""
  def __init__(self, app):
    self.app = app
    self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL', 'sqlite:///todos.db'
        )
    self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(self.app)

    with self.app.app_context():
      db.create_all()