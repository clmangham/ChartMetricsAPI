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

*Note: If running locally outside docker the API will be accessed at port 8000 - http://localhost:8000*

## Example Usage

#### User interface with API documentation and example queries: http://localhost:5001/ui/

![](assets/swagger_ui.gif)

Example as web address or with POSTMAN (GET):

```
http://localhost:5001/records?Ids=1,2,3
```

Example using Curl:
```
curl "http://localhost:5001/summary/pandas"
```

## Run app with scripts
Shell scripts to start the application locally (`run_app.sh`), or via docker (`run_docker.sh`), and to run sample commands (`flask_api_query.sh`), (`docker_api_query.sh`) are also provided in `/scripts`.

Example (after running `scripts/run_docker.sh`):

![](assets/docker_api_query.gif)

## Design Summary

The Flask application utilizes Connexion for API routing, SQLAlchemy for ORM, and Marshmallow for serialization. Key design choices include:

- **Connexion + Flask**: Uses Connexion for RESTful API management, leveraging OpenAPI for clear API documentation and validation, enhancing maintainability.
- **API Specification in YAML**: Defines API in `api.yml` for readability and easy modification, utilizing OpenAPI for automatic routing and validation.
- **SQLAlchemy ORM**: Models data in `models.py`, abstracting SQL queries for cleaner, safer code, and ensuring data consistency.
- **Marshmallow Serialization**: Integrates with SQLAlchemy in models.py for efficient data serialization/deserialization, offering advanced validation and transformation.
- **Data Handling**: Functions defined in `chart_data.py` centralize data processing, promoting modularity and easier testing.

These decisions foster a robust, scalable Flask API, supported by a strong Python community and extensive documentation, ensuring long-term stability and maintainability.