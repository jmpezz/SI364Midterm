# SI364Midterm - Julia Pezzullo

For my 364 Midterm, I used the Yelp API to search and pull reviews for restaurants. A user can enter a restaurant along with its location and they'll be able to see reviews for that restaurant from Yelp! A user can also rate a restaurant that they've been to regarding its service, food, and prices! 

**ROUTES**
1. http://localhost:5000/ --> base.html
2. http://localhost:5000/names --> name_example.html
3. http://localhost:5000/restaurants --> restaurants.html
4. http://localhost:5000/get_data --> restaurant_reviews.html
5. http://localhost:5000/rating --> rate_form.html
6. http://localhost:5000/see_ratings --> see_ratings.html

# Requirements all met

1. **Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)**
2. **Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, like this )**
3. **Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.**
4. **Include at least 2 additional template .html files we did not provide.**
5. **At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.**
These could be in the same template, and could be 1 of the 2 additional template files.
6. **At least one errorhandler for a 404 error and a corresponding template.**
7. **At least one request to a REST API that is based on data submitted in a WTForm.**
8. **At least one additional (not provided) WTForm that sends data with a GET request to a new page.**
9. **At least one additional (not provided) WTForm that sends data with a POST request to the same page.**
10. **At least one custom validator for a field in a WTForm.**
11. **At least 2 additional model classes.**
12. **Have a one:many relationship that works properly built between 2 of your models.**
13. **Successfully save data to each table.**
14. **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**
15. **Query data using an .all() method in at least one view function and send the results of that query to a template.**
16. **Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...)**
17. **Include at least one use of url_for. (HINT: This could happen where you render a form...)**
18. **Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)**

# Additional Requirements Met
19. **(100 points) Include an additional model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)**

20. **(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will not save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).**
