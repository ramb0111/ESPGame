## Welcome

ESP-Game App

### Submitted To

![squad-run-logo](https://squadrun.co/wp-content/uploads/2016/10/sr-fb.png)

### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/mjhea0/flask-boilerplate.git
  $ cd flask-boilerplate
  ```

2. Initialize and activate a virtualenv:
  ```
  $ pip install virtualenv
  $ virtualenv game_venv
  $ source game_venv/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```
4. Install Postgresql:
  ```
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
  postgres=# CREATE USER tester WITH PASSWORD 'password';
  postgres=# GRANT ALL PRIVILEGES ON DATABASE game to tester;
  postgres=# \q
  ```

7. Insert Data into the database
  ```
   psql game -f /path/to/game_db.sql
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

5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)


