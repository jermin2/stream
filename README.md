# STREAM
#### Video Demo:
#### Description:
A website that allows users to subscribe and update their to a regular magazine that will get sent to them. This application interacts and stores the user data in a database which can later be extracted to create postage labels. The end-user can login and update their details, or choose to unsubscribe at any time.

This application was written using Python, HTML, CSS, with some JavaScript using the Flask framework
It uses sqlite3 to connect to a database. This should be changed later during deployment.

There are 5 main pages to this website, but the ones of note are shown below

#### index.html
Index is the first page, which shows some brief information and includes a buttom to register
There is a yellow square created using CSS and an image wrapped in a div for a background.
At small screen sizes (<600px), you should only see an image. At larger screen sizes (>1500px), the yellow square should expand to fill up the gap and the image should stop getting larger. In between, the yellow squre should take up 40% of the width.

The image is contained in a div. This allows the image scale while also being cropped (by the div).

#### register.html
Register.html has two main components, a form and a div containing some information.
Having the form on the left looks better, but during screen-width breaks, this means the form would appear on the bottom. This was solved by using the <code>order-md-?</code> class in Bootstrap

#### update.html
update.html will first check to see if there is existing data for this user. If so, it will load it. Otherwise, when the user first enters their data, it will create a new record in the database and store it. 
An interesting design choice on this was to have the checkbox enabled by default (as a new user) but if it was unchecked on purpose, it should remain uncheck. This was accomplished by designating the checkbox as checking for active, but the database is storing the inactive state. If there is no inactive state in the database, then check the checkbox by default. The active checkbox is turned into the inactive variable by using a ternary operator in app.py

There is a dropdown of countries on this page. This affects the fields shown. Anywhere apart from NZ or Australia will also show a "Village" field. Additionally, selecting the Solomon Islands will show a "Province" field.


## How to run

To run, first start the environment by 

<code>venv\Scripts\activate</code>

Then you can run the website by:

<code>flask run</code>
