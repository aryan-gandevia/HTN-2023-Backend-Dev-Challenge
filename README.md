Author: Aryan Gandevia

## LOCAL SETUP
- Instal Python 3.10.0
    - If you already have PyEnv setup:
        - In the terminal, run these commands in order:
            - `pyenv install 3.10.0`
            - `pyenv local 3.10.0` to set the Python version in this environment
- Now, run this command: `pip install virtualenv`
- To create the virtul environment: `virtualenv env`
- To activate the virtual environment:
    - `source env/bin/activate` (this is for macOS)
    - `env\Scripts\activate.bat` (this is for windows)
* To deactivate the virtual environment at any point: `deactivate` *
- run `python -m pip install flask`, `python -m pip install flask_sqlalchemy` and `python -m pip install flask_restful` to download what is required for the program to run


## RUNNING THE PROGRAM LOCALLY
- `flask run` or `flask --debug run` for debugging


## API ROUTES
- `/users/`
    - GET: Gets all users

*`<name>` is replaced with with the fullname of who you desire to find.*
- `/users/<name>`
    - GET: Gets the user and all their corresponding information
    - PUT: Updates certain/all fields of a user's information (in JSON format)

*`<min_num>` and `<max_num>` are replaced with the minimum and maximum frequency of skills.*
- `/skills/min=<min_num> & max=<max_num>`
    - GET: Gets all the skills that appear in the database in between the minimum and maximum number given

*`<name>` is replaced with with the fullname of who you desire to find.*
- `/events/<name>`
    - GET: Gets all the events the user has attended
    - POST: Adds an event to all the events the user has attended. This is the "scan" function (in JSON format)
        - for example:
        {
            "event": "frontend developing",
            "eType": "workshop"
        }

- `/information/`
    - GET: Gets all information regarding the Hackathon

- `/addOrRemove/`
    - POST: Adds a new applicant to the database (in JSON format)
        - for example (skills and event field are optional):
        {
            "name": "Aryan Gandevia",
            "email": "aryan.gandevia@gmail.com",
            "phone": "6474737264",
            "company": "Ontario Institute of Cancer Research",
            "skills": [
                {
                    "skill": "Python",
                    "rating": 5
                },
                {
                    "skill": "Flask",
                    "rating": 4
                },
                {
                    "skill": "SQL",
                    "rating": 4
                }
            ],
            "events": [
                {
                    "event": "Hack the North 2020++",
                    "eType": "activity"
                },
                {
                    "event": "All about 3D modelling",
                    "eType": "workshop"
                },
                {
                    "event": "ethnic table of foods",
                    "eType": "getting food"
                }
            ]
        }
    - DELETE: Deletes an applicant from the database (give the user_id in JSON format)
        - for example:
        {
            "user_id": 1001
        }