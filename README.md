# Data Collection Webapp
This web app was created while learning Python with _Head First Python_ book I can recommend. <br>
It collects data about users request (HTML form data, user agent, IP, response) and stores it in MySQL database. <br>
To create it, I used various technologies including Python, Flask, MySQL and Jinja2 template engine.
## All pages in the webapp
`/` or `/entry` - the main page for a normal user. They can submit a request here using a form <br>
`/search4` - results of the request are displayed here <br>
`/login` and `/logout` - simple simulation of logging in and out <br>
`/viewlog` - here a logged in user can see the database content <br>
## Python files
`search4web.py` - contains the main webapp code <br>
`DBcm.py` - database context manager - provides abstraction for connection of the database with Python's DB-API <br>
`checker.py` - provides a function decorator that checks if a user is logged in or not
