from flask import Flask, session, request, render_template, g
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_session import Session
import random


# Configure app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Configure flask session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database and database models
db = SQLAlchemy(app)

# Database model for Website A
class PageView_A(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    page = db.Column(db.String(255))
    time_spent = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)

# Database model for Website B
class PageView_B(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(10))
    page = db.Column(db.String(255))
    time_spent = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)


with app.app_context():
    db.create_all()

@app.before_request
def track_time():
    global start_time

    # Initiate start time for homepage
    if request.path == '/':
        start_time = datetime.now()

    # Adding data for the time spent for website A to database PageView

    if request.path == '/learn_more':
        time_spent = (datetime.now() - start_time).total_seconds()
        page_view = PageView_A(
                visitor_id = session.get('visitor_id'),
                page='HomePage',
                time_spent=time_spent,
                start_time=start_time)
        db.session.add(page_view)
        db.session.commit()

    # Update Start Time
        start_time = datetime.now()

    elif request.path == '/confirmation':
        time_spent = (datetime.now() - start_time).total_seconds()
        page_view = PageView_A(
                visitor_id=session.get('visitor_id'),
                page='Learn More',
                time_spent=time_spent,
                start_time=start_time)
        db.session.add(page_view)
        db.session.commit()


    # Adding data for the time spent for website B to database PageView_B
    if request.path == '/website_b':
        start_time = datetime.now()

    elif request.path == '/learn_more_b':
        time_spent = (datetime.now() - start_time).total_seconds()
        page_view = PageView_B(
                visitor_id=session.get('visitor_id'),
                page='HomePage',
                time_spent=time_spent,
                start_time=start_time)
        db.session.add(page_view)
        db.session.commit()
        start_time = datetime.now()
    elif request.path == '/confirmation_b':
        time_spent = (datetime.now() - start_time).total_seconds()
        page_view = PageView_B(
                visitor_id=session.get('visitor_id'),
                page='Learn More',
                time_spent=time_spent,
                start_time=start_time)
        db.session.add(page_view)
        db.session.commit()
        start_time = datetime.now()



##################################################################################
#
# Routes
#


# Function to create a unique ID for each visitor
def add_visitor():
    visitor_id = session.get("visitor_id")
    if visitor_id is None:
        visitor_id = str(random.randint(1000000000, 9999999999))
        session["visitor_id"] = visitor_id
    return visitor_id

@app.route('/')
def index():
    add_visitor()
    return render_template('index.html')


@app.route('/learn_more')
def learn_more():
    add_visitor()
    return render_template('learn_more.html')



@app.route('/confirmation')
def confirmation():
    visitor_id = add_visitor()
    return render_template('done.html', visitor_id = visitor_id)

@app.route('/website_b')
def website_b():
    add_visitor()
    return render_template('website_b.html')

@app.route('/learn_more_b')
def learn_more_b():
    add_visitor()
    return render_template('learn_more_b.html')

@app.route('/confirmation_b')
def confirmation_b():
    visitor_id = add_visitor()
    return render_template('done_b.html', visitor_id = visitor_id)


if __name__ == '__main__':
    app.run(port=4000, debug = True)
