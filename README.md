# Toopher Iframe Example in Flask

A simple demonstration of Toopher 2fa using Flask.

## Running it

Clone the repo

    git clone git@github.com:smholloway/toopher-iframe-example-in-python.git

Install the requirements ([Toopher v1.1.0+](https://github.com/toopher/toopher-python) and [Flask](http://flask.pocoo.org/))

    # make a virtual environment, if you're into that sort of thing
    pip install -r requirements.txt

Set a TOOPHER_CONSUMER_KEY and TOOPHER_CONSUMER_SECRET (obtained from
the [Toopher Dev site](https://dev.toopher.com/)).

    export TOOPHER_CONSUMER_KEY=xxx
    export TOOPHER_CONSUMER_SECRET=xxx

Run the app

    python app.py

Fire up a browser and navigate to the site

>[http://localhost:5000/](http://localhost:5000/)

You should see a pairing screen

![Imgur](http://i.imgur.com/FrtpH4D.png)

Enjoy!

