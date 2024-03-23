from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__, template_folder='admin_templates')
# Set secret key using the SECRET_KEY environment variable
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
csrf = CSRFProtect(app)  # Initialize CSRF protection
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
    phone_number = Column(String) #change for simplicity
    interest = Column(String)
    receive_newsletter = Column(String, default='yes')
    agree_terms_and_conditions = Column(Integer, default=0)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

# Add a method to satisfy Flask-Login requirements
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
# Create tables
Base.metadata.create_all(engine)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

# Registration form
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    country = StringField('Country')
    phone_number = StringField('Phone Number')
    interest = SelectField('Interest', choices=[('technology', 'Technology'), ('finance', 'Finance'), ('entertainment', 'Entertainment')])
    receive_newsletter = BooleanField('Receive Newsletter', default=True)
    agree_terms_and_conditions = BooleanField('Agree to Terms and Conditions', default=False)
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user with provided email already exists
        if session.query(User).filter_by(email=form.email.data).first():
            flash('Email address already registered.', 'error')
        else:
            # Create a new user instance
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                country=form.country.data,
                phone_number=form.phone_number.data,
                interest=form.interest.data,
                receive_newsletter='yes' if form.receive_newsletter.data else 'no',
                agree_terms_and_conditions=1 if form.agree_terms_and_conditions.data else 0,
                password=generate_password_hash(form.password.data)
            )
            # Add the new user to the session and commit
            session.add(new_user)
            session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)
    
# Define the LoginForm class
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')
    
# Login route             
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Assuming you have a LoginForm defined
    if form.validate_on_submit():
        # Check login credentials (e.g., email and password)
        user = session.query(User).filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard or any other route
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)



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
