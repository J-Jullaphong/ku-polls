@echo off

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install Dependencies
python -m pip install -r requirements.txt

REM Create a .env file for externalized variables
copy sample.env .env

REM Run migrations
python manage.py migrate

REM Run tests
python manage.py test

REM Install data from the data fixtures
python manage.py loaddata data/users.json data/polls.json

echo "\nPlease continue with How to Run instructions in README.md"