# Valpo ACM's Website

A website for the Valpo chapter of ACM/ACM-W. Tentatively in Flask

run.py - will contain the actual python code that will import the app and start the development server.

\_\_init\_\_.py - will initialize the app, creating a Flask app instance.

views.py - will define the routes.

models.py - will define models for the app.

## Install Database

The plan is to use MariaDB as a database. Make sure you install MariaDB server before installing the library with pip.

### Debian/Ubuntu

`# apt install mariadb-server`

### Windows

Download it: https://mariadb.com/downloads/

### MacOS

`# brew install mariadb`

### Docker

`# docker run mariadb`

## Install Flask and Requirements

Make sure you are using Python 3.9.

`$ pip3 install flask mariadb`

## How to run

### Run Flask Development Server

Unix:
```
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```

Windows:
```
> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run
```
### Run MariaDB Server

`# systemctl start mariadb`
