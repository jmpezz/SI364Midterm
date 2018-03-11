###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField, RadioField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
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
    price = db.Column(db.String(10))
    rating = db.Column(db.Integer)
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

        newname = Name(name)
        db.session.add(newname)
        db.session.commit()

        same_rest = Restaurant.query.filter_by(restaurant = restaurant, location = location)
        if same_rest:
            rest = Restaurant.query.filter_by(restaurant = restaurant, location = location)
        else:
            rest = Restaurant(restaurant = restaurant, location = location)
            db.session.add(rest)
            db.session.commit()

        baseurl = ''
        return redirect(url_for('all_names'))
    return render_template('base.html',form=form)

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)


# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)
