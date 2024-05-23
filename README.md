# FastAPI Coursework Repository - NOT FINISHED

## About This Repository

This repository contains a REST API project developed using the FastAPI framework. The purpose of this repository is to provide a base project for individuals who want to develop a REST API for their application and have some knowledge of FastAPI, but are not experts in the field.

## Projects Overview


The Project covers a wide range of topics within FastAPI, including:

- **API Design**: Structuring endpoints effectively.
- **Request Handling**: Managing different types of client requests.
- **Data Validation and Serialization**: Using Pydantic models for robust data handling.
- **Database Integration**: Connecting to databases and performing CRUD operations.(MySQL,SQLite,PostgreSQL)
- **Authentication and Authorization**: Implementing security measures to protect APIs.
- **Testing**: Unit and Integration tests with pytest


![Screenshot 2024-05-16 at 13 18 33](https://github.com/dvirfriedler/FastAPI/assets/101118398/f1cd5a3b-3b8d-4f6b-bc95-07a3aad42b82)

## Installation

To run the projects in this repository, you will need to set up your environment properly. Here are the steps to get started:

```bash
# Clone the repository
git clone https://github.com/dvirfriedler/FastAPI


# Navigate into the project directory
cd FastAPI-Tutorial

# Install required dependencies
pip install -r requirements.txt

# Run the application
uvicorn TodoApp.main:app --reload

# To view the automatically generated interactive API documentation, open your browser and go to:
http://127.0.0.1:8000/docs
```

## Projects Architecture Explanation

At the root of the TodoApp project, you will find the following structure:

- **router folder**: Contains files for each router.
- **test folder**: Contains tests for each router.
- **database.py file**: Responsible for connecting the project to the database (more details provided later).
- **main.py file**: The entry point to the project.
- **models.py file**: Responsible for defining models for the different database tables.

Inside the router folder, you will find four files for the different routers in the project:
- **admin.py**: Contains the router for the admin section.
- **auth.py**: Contains the router for authentication when the user logs in.
- **todos.py**: Contains the router that enables deleting, adding, and changing the user's todos.
- **users.py**: Contains the router responsible for the user's information.


Inside the test folder you will see all the different files of the test for the project












