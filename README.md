# Backend Challenge
## Getting Started
### Prerequisites
For Local run 
Make sure you have a `pip`, `virtualenv` and `docker` installed on your machine
To install:
  ```sh
    sudo apt install python3-pip && pip3 install virtualenv
  ```
## Docker
###### Image Build
```bash
# main directory
docker build -f docker/Dockerfile .
```
###### Compose Build
```bash
cd docker
docker-compose -f docker-compose.dev.yml up
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
3. creating a superuser (username:admin, password:password)
    ```sh
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@email.com', 'password')" | python manage.py shell
    ```
4. run django server
    ```sh
    python manage.py runserver 8000      
    ```
5. run unit tests
    ```sh
    python manage.py test 
    ```
## Requirements
- [x] you should use django-rest-framework to build the endpoint, otherwise, feel free to use any other packages you
need.
- [x] you should use PostgreSQL as your database for this task.
- [x] you should write test cases for your endpoint.
- [x] you shouldn't expose any secrets in your codebase.

## Bonus
- [x] implement an endpoint that returns the number of answers per day over time (given from and to dates)."
- [x] the endpoint should be accessed by authenticated users only.
- [x] create 3 users using the built-in user module in Django, make the first one superuser only, the second one staff only and the last one is active only. now, do whatever is necessary to make the endpoint only accessed by a superuser or a staff user and otherwise a user is not allowed.
- [x] do a benchmark of your endpoint performance when there are 4000, 8000, 12000, 16000, 20000 reviews, is there any performance issues? how it could be improved?.
- [x] when merging reviews under the same date the answers gets repeated under this object, can you also merge answers to appear once and add a new field for their count?
- [x] dockerize your application ( ignore adding the DB backup file as long as your DB will be dockerized with the data
## Submit-requirements
- [x] backup your DB with all the data it has and add the backup file along with your app files.
- [x] create a readme.md file in the root of your app that shows your app requirements, what did you use and why, how to build it and run it,... etc.
- [x] create a public git repo on any platform you like ex: GitHub, GitLab,... etc and share the link of this repo when you are ready.
- [x] putin the readme.md file which bonuses did you decide to do.

## How to Improve and Optimize the performance
1. we can cache the queries using redis to reduce the load on the db
2. we can optimize the database schema by
    1. remove Review table
    2. replace review field in the answer model by inheriting the timestampmodel
    3. make choices and questions relation one to many instead of many to many 
3. use pagination to limit the number of results returned by the endpoint
4. we can integrate with elasticsearch for faster querying