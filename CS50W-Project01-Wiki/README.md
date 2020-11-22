# Project 1

Web Programming with Python and JavaScript


## Overview
This is a book review website. Users are able to register and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. A third-party API by Goodreads is used to pull in ratings from a broader audience. Finally, users are able to query for book details and book reviews programmatically via website’s API.
***

### What does each file contains?

#### aplication.py
* The application code is here with all routes and logic.
***

#### helpers.py
* In this file you can find all helping functions that I am using
***

#### forms.py
* All forms in this project are created with **flask_wtf**.
* The implementation code can be found here.
***

#### import.py
* This program takes the books from *books.csv* and imports them into PostgreSQL database.

#### layout.html
* The base layout for the project. It is extended by other files.
* The navigation bar is displayed only when the user is logged.
***

#### register.html
* Registration form. 
* User must register with username, email and password. 
* Password must be verified.
 ***

#### login.html
* Login form.
* user must login with username and password.
***

#### search.html
* Search form
* It has select menu where the user can choose between isbn, author and title.
* There is search field where the user can enter search query.
***

#### search-result.html
* The user is redirected here after submitting the search form.
* All results are displayed here.
* The results list is paginated with **flask-paginate**.
***

#### book.html
* The required information about the book is displayed here.
* *Writing review* is created with **bootstrap modal**.
* *Write review* form has text area field for comments and select menu for ratings with values from 1 to 5.
* The user can't write more than one comment per book. Once the user submit a comment *Write review* is no longer available.
* *View reviews* is created with **bootstrap collapse**.
***

#### apology.html
* This file is used to display any error messages or other information to the user.
***

#### Additional functionality 
* **@login_required** and **@logout_required** decorators created.
* User can't access certain routes if he\she is not logged in\out.
