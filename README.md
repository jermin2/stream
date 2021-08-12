# STREAM
#### Video Demo:
#### Description:
A website that allows users to subscribe and update their to a regular magazine that will get sent to them. This application interacts and stores the user data in a database which can later be extracted to create postage labels. The end-user can login and update their details, or choose to unsubscribe at any time.

This application was written using Python, HTML, CSS, with some JavaScript using the Flask framework
It uses sqlite3 to connect to a database. This should be changed later during deployment.

There are 5 main pages to this website

#### about.html
Contains a few paragraphs about the purpose of the magazine on offer

#### index.html
Index is the first page, which shows some brief information and includes a buttom to register
There is a yellow square created using CSS and an image wrapped in a div for a background.
At small screen sizes (<600px), you should only see an image. At larger screen sizes (>1500px), the yellow square should expand to fill up the gap and the image should stop getting larger. In between, the yellow squre should take up 40% of the width.

The image is contained in a div. This allows the image scale while also being cropped (by the div).

#### layout.html
This file contains the main layout from which other templates will be the block bodys
The navbar was mostly copied from the Bootstrap header examples. It has been slightly modified since it was causing some problems on small screens, with some of the buttons stacking. 

There is some code to flash messages included in this file. The messages will disappear after 3 seconds

#### login.html
A simple login screen, copied from the Bootstrap examples

#### register.html
Register.html has two main components, a form and a div containing some information.
Having the form on the left looks better, but during screen-width breaks, this means the form would appear on the bottom. This was solved by using the <code>order-md-?</code> class in Bootstrap

#### update.html
update.html will first check to see if there is existing data for this user. If so, it will load it. Otherwise, when the user first enters their data, it will create a new record in the database and store it. 
An interesting design choice on this was to have the checkbox enabled by default (as a new user) but if it was unchecked on purpose, it should remain uncheck. This was accomplished by designating the checkbox as checking for active, but the database is storing the inactive state. If there is no inactive state in the database, then check the checkbox by default. The active checkbox is turned into the inactive variable by using a ternary operator in app.py

There is a dropdown of countries on this page. This affects the fields shown. Anywhere apart from NZ or Australia will also show a "Village" field. Additionally, selecting the Solomon Islands will show a "Province" field.


#### app.py
This is the main application and connects to a local database and performs all the routing and error checking.

#### stream.db
This is a temporary database used for checking the code

#### statis/css/styles.css
This is the CSS file. The styling should be able to handle multiple screen sizes. There was a bit of effort trying to make the index.html look nice for different screen sizes

## How to run

To run, first start the environment by 

<code>venv\Scripts\activate</code>

Then you can run the website by:

<code>flask run</code>
