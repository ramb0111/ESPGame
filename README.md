## Welcome

ESP-Game App

### Screenshots

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

6. Create Database and User
   ```
   $ CREATE DATABASE Game;
   $ CREATE USER tester WITH PASSWORD 'password' CREATEDB SUPERUSER;
   $ GRANT ALL PRIVILEGES ON DATABASE "Game" to tester;
   ```

7. Copy paste the following credentials to ~/.bashrc
   ```

   $ source ~/.bashrc
   ```

5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)


