from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from esp_game import config


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def get_connection_string():
    """
    Creates a connection string for postgres database.
    :return: returns a connection string if successfully created.
    """
    connection_string = 'postgresql://' + config.GM_DB_USER + ":" + config.GM_DB_PASSWORD + "@" \
                        + config.GM_DB_HOST + ":" + config.GM_DB_PORT + "/" + config.GM_DB_NAME
    return connection_string



app = Flask(__name__)
app.config['SECRET_KEY'] = 'my precious'
app.config['DEBUG'] = True

# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

