###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField, RadioField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import yelp_api

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/jmpezzMidterm364"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)

client_id = yelp_api.client_id
api_key = yelp_api.api_key


######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key = True)
    restaurant = db.Column(db.String(200), unique = True)
    location = db.Column(db.String(200))
    reviews = db.relationship('Review', backref = 'restaurant')

    def __repr__(self):
        return 'Restaurant Name: {} (Restaurant ID: {})'.format(self.restaurant, self.id)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key = True)
    review = db.Column(db.String(5000))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    def __repr__(self):
        return 'Review: {} (Restaurant ID: {})'.format(self.review, self.restaurant_id)

class Ratings(db.Model):
    __tablename__ = 'restaurant_ratings'
    id = db.Column(db.Integer, primary_key = True)
    restaurant_name = db.Column(db.String(200))
    rate_rest = db.Column(db.Integer)
    service = db.Column(db.Integer)
    food = db.Column(db.Integer)
    price = db.Column(db.Integer)
    goback = db.Column(db.String(200))

    def __repr__(self):
        return "You gave {} a {} overall!".format(self.restaurant_name, self.rate_rest)

###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name.",validators=[Required()])
    restaurant = StringField('Please enter the name of a restaurant. (Must be more than 3 characters)', validators = [Required()])
    location = StringField('Please enter the location of the restaurant.', validators = [Required()])
    submit = SubmitField()

    def validate_rest(self, field):
        if len(field.data) < 3:
            raise ValidationError('Restaurant name must be more than 3 characters!')

class RateForm(FlaskForm):
    restaurants = StringField('Please enter the name of a restaurant you want to rate.', validators = [Required()])
    rate_rest = StringField('Please rate this restaurant from 1 (worst) to 10 (best)', validators = [Required()])
    service = StringField('Please rate the service at this restaurant from 1 (worst) to 10 (best)', validators = [Required()])
    food = StringField('Please rate the food at this restaurant from 1 (worst) to 10 (best)', validators = [Required()])
    price = StringField('Please rate the prices at this restaurant from 1 (worst) to 10 (best)', validators = [Required()])
    goback = RadioField("Would you like to go back to this restaurant?", choices = [('yes', 'yes'), ('no', 'no')], validators = [Required()])
    submit = SubmitField()


#######################
###### VIEW FXNS ######
#######################
@app.errorhandler(404)
def Error(x):
    return render_template('404.html'), 404

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if form.validate_on_submit():
        name = form.name.data
        restaurant = form.restaurant.data
        location = form.location.data

        newname = Name(name = name)
        db.session.add(newname)
        db.session.commit()

        same_rest = Restaurant.query.filter_by(restaurant = restaurant, location = location).first()
        if same_rest:
            rest = Restaurant.query.filter_by(restaurant = restaurant, location = location)
        else:
            rest = Restaurant(restaurant = restaurant, location = location)
            db.session.add(rest)
            db.session.commit()

        baseurl = 'https://api.yelp.com/v3/businesses/search'
        params = {'api_key': api_key, 'term': restaurant, 'location': location}
        headers = {'Authorization': 'Bearer %s' % api_key}
        data = requests.get(baseurl, headers = headers, params = params)
        json_data = json.loads(data.text)

        #retrieving restaurant ID & reviews data
        restaurantID = json_data['businesses'][0]['id']
        url_review = 'https://api.yelp.com/v3/businesses/'
        url_review2 = url_review + restaurantID + '/reviews'
        getdata = requests.get(url_review2, headers = headers)
        rev_data = json.loads(getdata.text)

        for x in rev_data['reviews']:
            rest = Restaurant.query.filter_by(restaurant = restaurant, location = location).first()
            review = Review(review = x['text'], restaurant_id = rest.id)
            rev_entry = Review.query.filter_by(review = x['text']).first()
            if rev_entry:
                rev = rev_entry
            else:
                rev = Review(review = x['text'], restaurant_id = rest.id)
                db.session.add(rev)
                db.session.commit()
        return redirect(url_for('get_data'))
    #taken from HW3
    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
    return render_template('base.html', form=form)

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html', names=names)

@app.route('/restaurants')
def all_restaurants():
    restaurants = Restaurant.query.all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/get_data')
def get_data():
    restaurants = Restaurant.query.all()
    reviews = Review.query.all()
    datalist = []
    for x in restaurants:
        restID = x.id
        datalist.append(x)
        for y in reviews:
            if restID == y.restaurant_id:
                datalist.append(y)
    return render_template('restaurant_reviews.html', data = datalist)

@app.route('/rating', methods = ['GET', 'POST'])
def rate_form():
    form = RateForm()
    if request.method == 'POST':
        rating = []
        restaurants = request.form['restaurants']
        rate = request.form['rate_rest']
        service = request.form['service']
        food = request.form['food']
        price = request.form['price']
        goback = request.form['goback']
        ratetup = (restaurants, rate)
        rating.append(ratetup)
        rate_obj = Ratings(restaurant_name = restaurants, rate_rest = rate, service = service, food = food, price = price, goback = goback)
        db.session.add(rate_obj)
        db.session.commit()

        return render_template('rate_form.html', form = form, all_ratings = rating)
    return render_template('rate_form.html', form = form)

@app.route('/see_ratings')
def ratings():
    see_ratings = Ratings.query.all()
    return render_template('see_ratings.html', see_ratings = see_ratings)



# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True, debug=True)
