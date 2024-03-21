from flask import Flask, render_template, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


app = Flask(__name__, template_folder='admin_templates')

# Define SQLite3 database file path
DB_FILE_PATH = 'sqlite:///admin/mydb.db'

# Create engine and session
engine = create_engine(DB_FILE_PATH)
Session = sessionmaker(bind=engine)
session = Session()

# Define declarative base
Base = declarative_base()

# Define a User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

# Create tables
Base.metadata.create_all(engine)

# Flask route to display users
@app.route('/users')
def users():
    users = session.query(User).all()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
