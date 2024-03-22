from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


app = Flask(__name__, template_folder='admin_templates')
# Set secret key using the SECRET_KEY environment variable
app.secret_key = os.environ.get('SECRET_KEY')
login_manager = LoginManager(app)

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
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    country = Column(String)
    phone_number = Column(Numeric)
    interest = Column(String)
    receive_newsletter = Column(String, default='yes')
    agree_terms_and_conditions = Column(Integer, default=0)
    password = Column(String, nullable=False)
    
# Create tables
Base.metadata.create_all(engine)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))
    
# Login route    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check login credentials (e.g., username and password)
        # If valid, load user and login
        user = session.query(User).filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirect to dashboard or any other route
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/dashboard')
@login_required
def dashboard():
    # Only authenticated users can access this route
    return render_template('dashboard.html')

# Flask route to display users
@app.route('/users')
def users():
    users = session.query(User).all()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
