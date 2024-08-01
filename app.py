#FLASK APP BOILER PLATE FOR POSTGRES DB

from flask import Flask, session, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from ignore_DO_NOT_UPLOAD import db_url
import logging
from logging.handlers import RotatingFileHandler



app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_ENABLED'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True

db = SQLAlchemy()

def connect_db(app):
    """CONNECT TO DB"""

    db.app = app
    db.init_app(app)

connect_db(app)

app.debug = True

toolbar = DebugToolbarExtension(app)

#Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create a file handler and set the log level
file_handler = RotatingFileHandler('flask.log', maxBytes=10240, backupCount=10)
file_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logging.getLogger().addHandler(file_handler)

# Build Engine
engine = create_engine(db_url)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

