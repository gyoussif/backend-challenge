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