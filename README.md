## Welcome

ESP-Game App:

Please be connected to the internet while playing the game because images are http urls

### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/ramb0111/ESPGame.git
  $ cd ESPGame
  ```

2. Initialize and activate a virtualenv:
  ```
  $ pip install virtualenv
  $ virtualenv game_venv
  $ source game_venv/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r esp_game/requirements.txt
  ```

4. Install Postgresql:
  ```
  Installation commands for postgresql in ubuntu
  $ sudo apt-get update
  $ sudo apt-get install postgresql postgresql-contrib
  ```

5. Launch Postgresql Shell:
  ```
  $ sudo -i -u postgres psql
  ```

6. Create Database and User:
  ```
  postgres=# CREATE DATABASE game;
  postgres=# CREATE USER tester WITH PASSWORD 'password' SUPERUSER CREATEDB;
  postgres=# GRANT ALL PRIVILEGES ON DATABASE game to tester;
  postgres=# \q
  ```

7. Copy paste the Database credentials to ~/.bashrc:
  ```
    export GM_DB_USER='tester'
    export GM_DB_PASSWORD='password'
    export GM_DB_HOST='localhost'
    export GM_DB_PORT='5432'
    export GM_DB_NAME='game'
  ```

8. To reflect the changes in bashrc , Source it:
  ```
  $ source ~/.bashrc
  ```

9. Run the development server:
  ```
  $ python esp_game/app.py
  ```

10. Insert Data into the database
  ```
  $ psql game -f /path/to/game_db.sql
  ```

11. Navigate to [http://localhost:5000](http://localhost:5000)


