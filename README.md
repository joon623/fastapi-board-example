The following is the README file for the FastAPI Board Example project, which demonstrates how to build a web
application using FastAPI and SQLAlchemy to create, read, update, and delete (CRUD) functionalities for a bulletin
board.

# Overview

This project provides an example implementation of a bulletin board with CRUD functionalities using FastAPI and
SQLAlchemy to manage the database.

# Installation and Running

1. Clone this repository.

```shell
git clone https://github.com/joon623/fastapi-board-example.git
```

2. Move into the cloned directory and create a virtual environment.
   Copy code

```shell
cd fastapi-board-example
python -m venv venv
```

3. Activate the virtual environment.

- Windows:

```shell
venv\Scripts\activate
```

- macOS/Linux:

```shell
source venv/bin/activate
```

4. Install the necessary packages.
```shell
pip install -r requirements.txt
```
5. Run the server.
```shell
uvicorn app.main:app --reload
```

6. Access the API documentation using Swagger UI by navigating to
http://localhost:8000/docs in a web browser.

## Technologies Used

- FastAPI
- SQLAlchemy
- Mysql

## Functionality

- Create, read, update, and delete posts
- User registration, login, and logout

For more detailed information, please refer to the README.md file in the repository.