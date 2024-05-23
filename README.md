# FastAPI Base Project

## About This Repository

This repository contains a REST API project developed using the FastAPI framework. The purpose of this repository is to provide a base project for individuals who want to develop a REST API for their application and have some knowledge of FastAPI, but are not experts in the field.

## Project Overview

The project is a REST API for a Todo List application. Each user of this application has a personal list of todos, and they can add, edit, and remove items from their list.

## User Information

Each user has the following information:
- **ID**
- **Username**
- **Email**
- **First Name**
- **Last Name**
- **Password**
- **Role** (user/admin)
- **Phone Number**

## Todo Item Details

Each todo item includes the following details:
- **Title**
- **Description**
- **Priority**
- **Completed** (True/False)
- **Owner ID** (refers to the user ID)


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

# To run the tests on the project open the "FastAPI" folder in your terminal run:
pytest
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


## Request Handling

The project efficiently manages different types of client requests. Here's an overview of how various requests are handled:

- **GET Requests**: Retrieve data from the server. For example, fetching the list of todos or user details.
- **POST Requests**: Send data to the server to create new records. For example, adding a new todo item or registering a new user.
- **PUT Requests**: Update existing records on the server. For example, editing a todo item or updating user information.
- **DELETE Requests**: Remove records from the server. For example, deleting a todo item or removing a user account.

The API ensures proper validation and error handling for all request types, ensuring a smooth and reliable user experience.


## Database Integration

To connect the project to your own database, follow these steps:

1. **Create your own MySQL database with the following tables:**

   **Users Table Query:**

   ```sql
   CREATE TABLE `users` (
       `id` int(11) NOT NULL AUTO_INCREMENT,
       `email` varchar(200) DEFAULT NULL,
       `username` varchar(45) DEFAULT NULL,
       `first_name` varchar(45) DEFAULT NULL,
       `last_name` varchar(45) DEFAULT NULL,
       `hashed_password` varchar(200) DEFAULT NULL,
       `is_active` int(1) DEFAULT NULL,
       `role` varchar(45) DEFAULT NULL,
       `phone_number` varchar(45) DEFAULT NULL,
       PRIMARY KEY (`id`)
   ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
   ```

   **Todos Table Query:**
   
   ```sql
   CREATE TABLE 'todos' (
        'id' int(11) NOT NULL AUTO_INCREMENT,
        'title' varchar(200) DEFAULT NULL,
        'description' varchar(200) DEFAULT NULL,
        'priority' int(1) DEFAULT NULL,
        'completed' int(1) DEFAULT ,
        'owner_id' int(11) DEFAULT NULL,
        PRIMARY KEY ('id'),
        FOREIGN KEY ('owner_id') REFERENCES 'users' ('id')
    ) ENGINE=InnoDB AUTO_INCEREMNT=1 DEFAULT CHARSET=latin1;

    ```
2. **Connect the project to your own MySQL database:**
   
    Open the database.py file and update the following line:
      ```bash
      SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:{root-password}@127.0.0.1:3306/{the name of your database}"
      ```
      For example, if your password is test1234! and your database name is TodoApplicationDatabase, the line should look like this:
      ```bash
      SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:test1234!@127.0.0.1:3306/TodoApplicationDatabase"
      ```

   Great!! now the project is connected to your database

## Testing

Testing for this project is done using pytest. You can find all the tests in the `tests` folder inside the `TodoApp` directory. Feel free to add any tests you like by including them in one of the existing files in the `tests` folder.

To run the tests, open the terminal, navigate to the `TodoApp` directory, and execute the following command:

```bash
pytest
```

## Connect

If you have any questions, suggestions, or would like to connect regarding this project, feel free to reach out to me. Here are my contact details:

- **Email**: dvir.friedler@gmail.com
- **LinkedIn**: https://www.linkedin.com/in/dvir-friedler-225211128/
- **GitHub**: https://github.com/dvirfriedler

I look forward to connecting with you!
