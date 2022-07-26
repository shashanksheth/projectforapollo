This folder contains the solution to Part 1 of the project.

First, you will need to execute load_trades_data.py. This will create a SQLight DB where the trades data is stored.

NOTE that you will need to install SQLAlchemy to the working environment. A simple "pip install SQLAlchemy" command should suffice. You can find more documentation on this package here: https://pypi.org/project/SQLAlchemy/

Second, you will need to execute app.py. This will start the webserver where the data is exposed via RESTful API. Once this is running, you will notice that the location of the server is given in command-line. The 4th bullet should contain the relevant address.

NOTE that you will need to install Flask as well as Flask-SQLAlchemy. A simple "pip install Flask" and "pip install Flask-SQLAlchemy" command should suffice. You can find more documentation on this packages here: https://pypi.org/project/Flask/ , https://pypi.org/project/Flask-SQLAlchemy/

Example: * Running on http://127.0.0.1:5000 (Press CTRL+C to quit).

This will take you to an index page where the the available API routes and instructions are specified.
