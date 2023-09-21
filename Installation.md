# Installation
This file containing instructions for how to install and configure application.

## Clone code from GitHub
Clone this repository using this command in your terminal to your desired directory
```
git clone https://github.com/ThanadolU/ku-polls.git .
```

## Create a virtual environment and install dependencies

* Create a virtual environment:
    1. To create a virtual environment in your directory, type:
        * For Windows:
            ```
            python -m venv path\to\directory
            # for example: python -m venv env
            ```

        * For MacOS:
            ```
            python3 -m venv /path/to/directory
            ```
    2. To activate the virtual environment, type:
        * For Windows:
            ```
            path\to\venv\Scripts\activate
            # for example: env\Scripts\activate
            ```
        * For MacOS:
            ```
            </path/to/venv>/bin/activate
            ```

    3. Install Dependencies: 

        Install everything inside `requirements.txt` file.
        * For Windows:
            ```
            pip install -r requirements.txt
            ```

        * For MacOS:
            ```
            pip3 install -r requirements.txt
            ```

* More details about virtual environment :
    * Linux: https://www.pragmaticlinux.com/2021/12/create-a-python-virtual-environment-in-the-linux-terminal/
    * Offcial Python Document for virtual environment: https://docs.python.org/3/library/venv.html.

## Set values for externalized variables
    
Inside [sample.env](sample.env), I already wrote a structure of all externalized variables like this:
```
# put your secret key here
SECRET_KEY = secret_key-value-without-quotes
# set DEBUG to True for testing, False for actual use
DEBUG=True
# set ALLOWED_HOSTS ex. *.ku.th, localhost, 127.0.0.1, ::1
ALLOWED_HOSTS=localhost, 127.0.0.1
# set TIME_ZONE to your timezone
TIME_ZONE=Asia/Bangkok
```

## Run migrations

* For Windows
    ```
    python manage.py migrate
    ```
* For MacOS
    ```
    python3 manage.py migrate
    ```

## Run tests
Run all tests for this application
* For Windows
    ```
    python manage.py test
    ```
* For MacOS
    ```
    python3 manage.py test
    ```
    
## Install data from the data fixtures

* Load question data from JSON files
    ```
    python manage.py loaddata data/polls-question.json
    ```
* Load choice data from JSON files
    ```
    python manage.py loaddata data/polls-choice.json
    ```