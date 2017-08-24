import os

# Grabs the folder where the script runs.
# basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.


# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php



# Database Environment Variables
GM_DB_USER = os.environ['GM_DB_USER']
GM_DB_PASSWORD = os.environ['GM_DB_PASSWORD']
GM_DB_HOST = os.environ["GM_DB_HOST"]
GM_DB_PORT = os.environ["GM_DB_PORT"]
GM_DB_NAME = os.environ["GM_DB_NAME"]