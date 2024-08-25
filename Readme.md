# FastAPI + MySQL

This project is a FastAPI-based REST API with a MySQL database, managed using Poetry for dependency management, and containerized with Docker. The application includes user and post management with basic CRUD operations and relationship handling.

## Features

- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **MySQL**: A popular relational database management system used as the project's database.
- **Poetry**: Python packaging and dependency management made easy.
- **Docker**: Containerization to make the project portable and easy to run on any system.
- **SQLAlchemy ORM**: ORM used to interact with the MySQL database.
- **Pydantic**: Data validation and serialization for input/output.
- **Testing**: Automated testing with Pytest.

## Installation and Setup

### Prerequisites

Ensure you have the following installed:

- **Docker** (required for running the containers)
- **Poetry** (optional if you want to manage dependencies outside Docker)

### Running the Project

1. Clone the Repository

```
git clone https://github.com/codeldorado/fastapi_mysql_simple.git
cd fastapi_mysql_simple
```

2. Build and Run with Docker Compose

Build and run the containers for both FastAPI and MySQL:

```
docker-compose up --build
```

This will start the FastAPI app on http://localhost:8000 and a MySQL database on localhost:3306.

3. Access the API Documentation

Once the application is running, you can access the interactive API documentation (provided by Swagger UI) by navigating to:

```
http://localhost:8000/docs
```

### Running Tests

You can run the unit tests using the following command:

```
docker-compose run web pytest
```

This will execute the tests in a containerized environment, ensuring consistency across different systems.

## Environment Variables

The project uses environment variables for configuration. Here's a list of important ones:

- `DATABASE_URL`: Connection string for the MySQL database.

#### Example `.env` File

```
DATABASE_URL=mysql+mysqlconnector://codeldorado:example_password@db/ziptie
```

You can place this in a .env file in the root of the project and modify the docker-compose.yml to load it:

## Project Dependencies

The dependencies for the project are managed by Poetry and listed in pyproject.toml.

To install the dependencies manually (without Docker):

```
poetry install
```

## Docker Containerization

The project is fully containerized using Docker:

- `Dockerfile`: Defines the environment for running the FastAPI application.
- `docker-compose.yml`: Defines and orchestrates the FastAPI and MySQL containers.

Common Docker Commands

- Build and Run Containers: docker-compose up --build
- Stop Containers: docker-compose down
- Rebuild Containers: docker-compose up --build --force-recreate
