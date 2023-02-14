# Backend Challenge
## Getting Started
### Prerequisites
Make sure you have a `pip` and `virtualenv` installed on your machine
To install:
  ```sh
    sudo apt install python3-pip && pip3 install virtualenv
  ```
## Installation
1. Clone the repo
   ```sh
   git clone https://github.com/gyoussif/backend-challenge.git
   ```
2. Create a virtual environment and activate it
   ```sh
    virtualenv venv && source {ABSOLUTE_PATH_TO_VENV}/venv/bin/activate  
   ```

   It's preferable to create the venv outside your workdir as it slows down the file processing of some IDEs.
   However, if it works with you in any other way then that's great.

2.  Install requirements using poetry
    ```sh
    poetry install
    ```
## Database Setup
1. you can run the postgis docker image 
    ```bash
    cd docker
    docker-compose -f docker-compose-postgis.yml up
    ```
    or run it locally 
2. make sure to add the database credintials in apps/.env file
## Django Setup
1. db migration
    ```sh
    python manage.py makemigrations #create migration files
    python manage.py migrate #apply migration files on the db
    ```
2. populate db with random reviews
    ```sh
    python -m create_reviews 
    ```
3. creating a superuser (username:admin, password:admin)
    ```sh
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@email.com', 'admin')" | python manage.py shell
    ```
4. run django server
    ```sh
    python manage.py runserver 8000      
    ```
## Requirements
- [x] you should use django-rest-framework to build the endpoint, otherwise, feel free to use any other packages you
need.
- [x] you should use PostgreSQL as your database for this task.
- [x] you should write test cases for your endpoint.
- [x] you shouldn't expose any secrets in your codebase.

## Bonus
- [x] implement an endpoint that returns the number of answers per day over time (given from and to dates)."
- [] the endpoint should be accessed by authenticated users only.
- [] create 3 users using the built-in user module in Django, make the first one superuser only, the second one staff only and the last one is active only. now, do whatever is necessary to make the endpoint only accessed by a superuser or a staff user and otherwise a user is not allowed.
- [] do a benchmark of your endpoint performance when there are 4000, 8000, 12000, 16000, 20000 reviews, is there any performance issues? how it could be improved?.
- [] when merging reviews under the same date the answers gets repeated under this object, can you also merge answers to appear once and add a new field for their count?
- [] dockerize your application ( ignore adding the DB backup file as long as your DB will be dockerized with the data
## Submit-requirements
- [] backup your DB with all the data it has and add the backup file along with your app files.
- [] create a readme.md file in the root of your app that shows your app requirements, what did you use and why, how to build it and run it,... etc.
- [] create a public git repo on any platform you like ex: GitHub, GitLab,... etc and share the link of this repo when you are ready.
- [] putin the readme.md file which bonuses did you decide to do.