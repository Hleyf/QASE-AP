# QASE-APP

## Description

QASE-APP is a CRUD solution based in Python Flask

## Installation

Python 3 will be required for running the project locally, this can be easily achieved by installing it from the Microsoft Store (for Windows users).
For running this project locally, virtualenviroment is recomended. 'requirements.txt' in the root folder contains all the necessary dependencies for running and testing the app.

To install QASE-AP, follow these steps:

1. Install Python 3 from Microsoft Store (Windows users only)
2. Clone project to a local folder
3. Install virtual Enviroment and activate your new enviroment
```
python -m venv .env
```
5. Activate your virtual enviroment
```
./.env/Scripts/Activate
```
7. Install dependencies using 'requirements.txt'
```
pip install -r requirements.txt
``` 
8. Run project
```
 python src/app.py
``` 

If you wish to run the tests for this project simply run the following: 

To run all the test:
```
python -m pytest
```
Or you can run the tests individually:

Main tests: Login, Logout and registry tests
```
pytest src/tests/main_test.py
```

User tests: Remaining CRUD interactions for users withing the app.
```
pytest src/tests/user_test.py
```

Task tests: Task CRUD interactions.
```
pytest src/tests/task_test.py
```

## Usage

Here's how you can use QASE-AP:

1. The app will generate 30 users and tasks the first time it runs, Login as admin for starting using the app.
```
User: admin
Password: admin
```
2. Home page has been left blank on purpose, since I am meant to develop a dashboard with various stadistics about users and tasks
3. User page contains a list of users. Admin type users are allowed to perform all CRUD operations with users, except change their passwords
4. Users can view other user's profiles and edit their own profile and password. 
5. Task page contains a list of task. Tasks can be created, edited and deleted by all users. They can also be asigned to other users and change their status. 
