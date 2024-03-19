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

*Note: If running locally outside docker the API will be accessed at port 8000 - http://localhost:8000*

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
Shell scripts to start the application locally (`run_app.sh`), via docker (`run_docker.sh`), and to run sample commands (`sample_api_query.sh`) are also provided.