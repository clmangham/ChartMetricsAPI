import sqlite3
from config import db
from models import (
    Chart_Data,
    Observation_Type,
    Result_Status,
    Unit_Of_Measure,
    data_schema,
    datum_schema,
    aggregated_data_schema,
)
from sqlalchemy import func, and_, case, or_
import pandas as pd
from flask import jsonify


# Function to retrieve chart data by a list of IDs
def get_chart_data_by_ids(Ids):
    # Convert the comma-separated ID string into a list of integers
    ids = [int(id_str) for id_str in Ids.split(",") if id_str.isdigit()]

    # Query the database for records with the specified IDs, including related data
    result = (
        db.session.query(Chart_Data)
        .outerjoin(Observation_Type)
        .outerjoin(Result_Status)
        .outerjoin(Unit_Of_Measure)
        .filter(Chart_Data.Id.in_(ids))
        .all()
    )

    # Serialize the query result into JSON format and return
    return data_schema.dump(result)


# Function to get aggregated data using SQL queries
# Perform an SQL query to aggregate data, applying conditions and grouping by relevant fields
def get_aggregated_chart_data_sql():
    result = (
        db.session.query(
            Observation_Type.Name.label("Observation_Type"),
            Unit_Of_Measure.Name.label("Unit_Of_Measure"),
            func.count(Chart_Data.VALUENUM).label("Num_Admissions"),
            func.min(Chart_Data.VALUENUM).label("Min_Value"),
            func.max(Chart_Data.VALUENUM).label("Max_Value"),
            func.sum(
                case(
                    (
                        and_(
                            or_(Chart_Data.ERROR.is_(None), Chart_Data.ERROR != 1),
                            or_(Chart_Data.WARNING.is_(None), Chart_Data.WARNING != 1),
                            or_(
                                Result_Status.Name.is_(None),
                                Result_Status.Name != "Manual",
                            ),
                        ),
                        1,
                    ),
                    else_=0,
                )
            ).label("Valid_Records"),
        )
        .join(
            Observation_Type,
            Observation_Type.Id == Chart_Data.Observation_Type_Id,
            isouter=True,
        )
        .join(
            Result_Status, Result_Status.Id == Chart_Data.Result_Status_Id, isouter=True
        )
        .join(
            Unit_Of_Measure,
            Unit_Of_Measure.Id == Chart_Data.Unit_Of_Measure_Id,
            isouter=True,
        )
        .group_by(Observation_Type.Name, Unit_Of_Measure.Name)
        .all()
    )

    # Serialize and return the aggregated data
    return aggregated_data_schema.dump(result)


# Function to get aggregated data using Pandas for data processing
def get_aggregated_chart_data_pandas():
    # Use a context manager to ensure the database connection is closed after use
    with sqlite3.connect("randomized_chart_data.sqlite") as conn:
        # Load data into Pandas DataFrames
        chart_data_df = pd.read_sql_query("SELECT * FROM Chart_Data", conn)
        observation_type_df = pd.read_sql_query("SELECT * FROM Observation_Type", conn)
        result_status_df = pd.read_sql_query("SELECT * FROM Result_Status", conn)
        unit_of_measure_df = pd.read_sql_query("SELECT * FROM Unit_Of_Measure", conn)

    # Perform data merging and renaming for clarity
    # Merge Observation_Type
    merged_df = chart_data_df.merge(
        observation_type_df,
        left_on="Observation_Type_Id",
        right_on="Id",
        how="left",
        suffixes=("", "_o"),
    )
    merged_df = merged_df.rename(columns={"Name": "Observation_Type"})

    # Merge Result_Status
    merged_df = merged_df.merge(
        result_status_df,
        left_on="Result_Status_Id",
        right_on="Id",
        how="left",
        suffixes=("", "_r"),
    )
    merged_df = merged_df.rename(columns={"Name": "Result_Status"})

    # Merge Unit_Of_Measure
    merged_df = merged_df.merge(
        unit_of_measure_df,
        left_on="Unit_Of_Measure_Id",
        right_on="Id",
        how="left",
        suffixes=("", "_u"),
    )
    merged_df = merged_df.rename(columns={"Name": "Unit_Of_Measure"})

    # Define conditions for valid records and perform data aggregation
    conditions = (
        (merged_df["ERROR"] != 1)
        & (merged_df["WARNING"] != 1)
        & (merged_df["Result_Status"] != "Manual")
    )
    merged_df["Valid_Records"] = conditions.astype(int)

    # Aggregate the data
    aggregation = {"VALUENUM": ["count", "min", "max"], "Valid_Records": "sum"}
    aggregated_data = merged_df.groupby(
        ["Observation_Type", "Unit_Of_Measure"], dropna=False
    ).agg(aggregation)

    # Rename the columns for clarity
    aggregated_data.columns = [
        "Num_Admissions",
        "Min_Value",
        "Max_Value",
        "Valid_Records",
    ]
    aggregated_data = aggregated_data.reset_index()

    # Return the aggregated data as a dictionary
    return aggregated_data_schema.dump(aggregated_data.to_dict(orient="records"))
