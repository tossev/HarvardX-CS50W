
# Project 01 - Books

Web Programming with Python and JavaScript

Video for CS50W-Project01-Books -> https://youtu.be/sRQdEljUnow

## Objectives

-   Become more comfortable with Python.
-   Gain experience with Flask.
-   Learn to use SQL to interact with databases. 
## Overview
This is a book review website. Users are able to register and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. A third-party API by Goodreads is used to pull in ratings from a broader audience. Finally, users are able to query for book details and book reviews programmatically via website’s API.

**You can find database credentials in *`application.py`***.
***
## Requirements

Alright, it’s time to actually build your web application! Here are the requirements:

-   **Registration**: Users should be able to register for your website, providing (at minimum) a username and password.
-   **Login**: Users, once registered, should be able to log in to your website with their username and password.
-   **Logout**: Logged in users should be able to log out of the site.
-   **Import**: Provided for you in this project is a file called  `books.csv`, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called  `import.py`  separate from your web application, write a program that will take the books and import them into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running  `python3 import.py`  to import the books into your database, and submit this program with the rest of your project code.
-   **Search**: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
-   **Book Page**: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
-   **Review Submission**: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
-   **Goodreads Review Data**: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
-   **API Access**: If users make a GET request to your website’s  `/api/<isbn>`  route, where  `<isbn>`  is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:

```
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}

```

If the requested ISBN number isn’t in your database, your website should return a 404 error.

-   You should be using raw SQL commands (as via SQLAlchemy’s  `execute`  method) in order to make database queries. You should not use the SQLAlchemy ORM (if familiar with it) for this project.
-   In  `README.md`, include a short writeup describing your project, what’s contained in each file, and (optionally) any other additional information the staff should know about your project.
-   If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to  `requirements.txt`!

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
