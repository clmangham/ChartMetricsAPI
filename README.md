# ChartMetricsAPI

The ChartMetricsAPI project is designed to demonstrate proficiency in developing RESTful APIs using Python, interacting with SQLite databases, and containerizing applications using Docker. This project encompasses two main challenges:

1. API Development: Development of a REST API to query and return data from a provided SQLite database, focusing on specific data manipulation and aggregation tasks.
2. Containerization: Packaging the developed API into a Docker container, ensuring isolated and consistent execution environments.

## Technical Stack

- Programming Language: Python 3.8
- Database: SQLite
- API Framework: Flask
    - Connexion (API documentation)
    - Marshmallow (Python object serialization)
    - SQLAlchemy (SQL data modeling),
    - Pandas (General Data Processing)
- Containerization: Docker, Docker Compose

## API Endpoints

- Record Lookup:
    - Path: /records/
    - Method: GET
    - Description: Accepts a comma-separated list of Ids to fetch corresponding records from the Chart_Data table. Returns detailed data including related Observation_Type, Result_Status, and Unit_Of_Measure.

- Data Summary (SQL):
    - Path: /summary/sql
    - Method: GET
    - Description: Returns a summary of the data directly via SQL queries (SQLAlchemy), showcasing the observation types and units of measure along with metrics like the number of valid records, admissions, and value ranges.

- Data Summary (Pandas):
    - Path: /summary/pandas
    - Method: GET
    - Description: Similar to the SQL summary endpoint, but the data aggregation is performed using Pandas in Python, illustrating an alternative approach to data processing.

## Getting Started

The application is containerized using Docker, which simplifies deployment and ensures that the application runs the same in every environment.

### Prerequisites

- Docker
- Python 3.8 (if running locally outside Docker)

### Installation and Running

Clone and enter the repo:
```
git clone https://github.com/clmangham/ChartMetricsAPI.git
cd ChartMetricsAPI
```

Build a docker image and run the application as a container using docker-compose:
```
docker-compose up --build
```

After running the application API can now be accessed at http://localhost:5001

#### To run without docker using python 3.8:

```
pip install -r requirements.txt
python app.py
```

####  *Note: If running locally outside docker the API will be accessed at port 8000 - http://localhost:8000*

### Example Usage

A user interface with API documentation and example queries can be found at http://localhost:5001/ui/

#### OR

Use as web address or with POSTMAN (GET):

```
http://localhost:5001/records?Ids=1,2,3
```

#### OR

Using Curl:
```
curl "http://localhost:5001/summary/pandas"
```

### Run with Shell Scripts
Shell scripts to start the application locally (`run_app.sh`), via docker (`run_docker.sh`), and to run sample commands (`flask_api_query.sh`), (`docker_api_query.sh`) are also provided.




## Design Summary

The code across the different files (`config.py`, `app.py`, `api.yml`, `models.py`, `chart_data.py`) represents a Flask application leveraging Connexion for API management, SQLAlchemy for Object-Relational Mapping (ORM), and Marshmallow for serialization. Here's a summary of the key design decisions and their rationale:

### 1. **Use of Connexion + Flask**

- **Decision**: Implement the API with Connexion, defining endpoints in `api.yml`.
- **Rationale**: Connexion provides a robust framework for handling RESTful APIs in Flask applications. It allows for defining APIs using the OpenAPI specification, which enhances API documentation and validation. This approach ensures a clear separation between the API definition and business logic, improving maintainability and scalability.

### 2. **API Specification in YAML**

- **Decision**: Use `api.yml` to define the API structure, endpoints, and expected responses.
- **Rationale**: YAML is human-readable and widely used for configuration files. By using `api.yml` for the API specification, the project benefits from an easily understandable and modifiable API structure. This external definition file also aids in auto-generating routing and validation based on the OpenAPI standard.

### 3. **Data Modeling with SQLAlchemy**

- **Decision**: Define data models in `models.py` using SQLAlchemy ORM.
- **Rationale**: SQLAlchemy abstracts away SQL queries and provides a high-level ORM interface to interact with the database. This makes the code cleaner, easier to write and maintain, and reduces the likelihood of SQL injection vulnerabilities. It also promotes code reusability and data consistency.

### 4. **Serialization with Marshmallow**

- **Decision**: Use Marshmallow schemas in `models.py` for data serialization and deserialization.
- **Rationale**: Marshmallow integrates seamlessly with SQLAlchemy models to provide easy serialization of query results to JSON, which is essential for RESTful API responses. It also supports advanced validations and transformations, enhancing the robustness and flexibility of data handling.

### 5. **Data Access and Processing Layer**

- **Decision**: Implement functions in `chart_data.py` to handle data retrieval and processing.
- **Rationale**: Isolating the data access and processing logic in `chart_data.py` separates concerns within the application, making the codebase more organized and modular. This approach enables easier unit testing and refactoring when business requirements change.

### 6. **Configuration and Environment Management**

- **Decision**: Centralize configuration settings in `config.py`.
- **Rationale**: Having a dedicated configuration file (`config.py`) simplifies managing application settings (like database URI) and enhances the application's scalability and adaptability to different environments (development, testing, production).

These design decisions collectively support the development of a robust, scalable, and maintainable web API application. The chosen tools and frameworks (Flask, Connexion, SQLAlchemy, Marshmallow) are well-established in the Python community, offering extensive documentation, community support, and compatibility, thereby reducing the long-term maintenance overhead and ensuring the application's longevity and reliability.