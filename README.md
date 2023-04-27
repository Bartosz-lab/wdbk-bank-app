# Simple Bank App

## Develop

1. Set up env enviroment
    ```
    python3 -m venv venv
    source ./venv/bin/activate
    ```
2. Install reguired packages
    ```
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3. Run database from Docker compose
    ```
    docker compose up db -d
    ```

4.  Set up connection with database in file  `instance/config.py`
    ```
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://hello_flask:hello_flask@localhost:5432/hello_flask_dev"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    ```
    You should also configure Mail Server

5. Run Debug Flask server
    ```
    flask run
    ```


## Web server with nginx in docker
```
docker compose up --build
```
You shoud config enviroment variables for mail server

## Server in DigitalOcean
Comming Soon