from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import requests
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

swagger = Swagger(app)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brewery_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('search'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    breweries = []
    search_performed = False  # Initialize the flag

    if request.method == 'POST':
        search_performed = True  # Set the flag to True when a search is performed
        search_by = request.form['search_by']
        search_value = request.form['search_value']
        if search_by == 'city':
            response = requests.get(f'https://api.openbrewerydb.org/breweries?by_city={search_value}')
        elif search_by == 'name':
            response = requests.get(f'https://api.openbrewerydb.org/breweries?by_name={search_value}')
        elif search_by == 'type':
            response = requests.get(f'https://api.openbrewerydb.org/breweries?by_type={search_value}')
        breweries = response.json()
    
    return render_template('search.html', breweries=breweries, search_performed=search_performed)

@app.route('/brewery/<id>', methods=['GET', 'POST'])
def brewery(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    response = requests.get(f'https://api.openbrewerydb.org/breweries/{id}')
    brewery = response.json()
    
    if request.method == 'POST':
        rating = request.form['rating']
        description = request.form['description']
        new_review = Review(brewery_id=id, user_id=session['user_id'], rating=rating, description=description)
        db.session.add(new_review)
        db.session.commit()
    
    reviews = Review.query.filter_by(brewery_id=id).all()
    
    return render_template('brewery.html', brewery=brewery, reviews=reviews)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
