from flask import Flask, render_template, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Define PostgreSQL connection URL
POSTGRES_URL = os.getenv("POSTGRES_URL") 

# Create engine and session
engine = create_engine(POSTGRES_URL)
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
