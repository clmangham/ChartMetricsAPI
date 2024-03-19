from flask import make_response, abort, jsonify
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
from sqlalchemy import func, and_
from sqlalchemy import case
import pandas as pd
from collections import OrderedDict

def get_chart_data_by_ids(Ids):
    ids = [int(id_str) for id_str in Ids.split(",") if id_str.isdigit()]

    # Query the Chart_Data objects fully, including related entities
    result = (
        db.session.query(Chart_Data)
        .outerjoin(Observation_Type)
        .outerjoin(Result_Status)
        .outerjoin(Unit_Of_Measure)
        .filter(Chart_Data.Id.in_(ids))
        .all()
    )

    return data_schema.dump(result)

    # # Manual serialization to ensure order
    # serialized_result = []
    # for item in result:
    #     serialized_item = OrderedDict([
    #         ("Id", item.Id),
    #         ("CHARTTIME", item.CHARTTIME),
    #         ("VALUENUM", item.VALUENUM),
    #         ("ERROR", item.ERROR),
    #         ("WARNING", item.WARNING),
    #         ("STOPPED", item.STOPPED),
    #         ("observation_type", item.observation_type.Name if item.observation_type else None),
    #         ("result_status", item.result_status.Name if item.result_status else None),
    #         ("unit_of_measure", item.unit_of_measure.Name if item.unit_of_measure else None),
    #     ])
    #     serialized_result.append(serialized_item)

    # return serialized_result



def get_aggregated_chart_data_sql():
    result = (
        db.session.query(
            Observation_Type.Name.label("Observation_Type"),
            Unit_Of_Measure.Name.label("Unit_Of_Measure"),
            func.sum(
                case(
                    (
                        and_(
                            Chart_Data.ERROR != 1,
                            Chart_Data.WARNING != 1,
                            Chart_Data.Result_Status_Id != 1,
                        ),
                        1,
                    ),
                    else_=0,
                )
            ).label("Valid_Records"),
            func.count().label(
                "Num_Admissions"
            ),  # You can use func.count() without '*'
            func.min(Chart_Data.VALUENUM).label("Min_Value"),
            func.max(Chart_Data.VALUENUM).label("Max_Value"),
        )
        .join(Observation_Type, Observation_Type.Id == Chart_Data.Observation_Type_Id, isouter=True)
        .join(Result_Status, Result_Status.Id == Chart_Data.Result_Status_Id, isouter=True)
        .join(Unit_Of_Measure, Unit_Of_Measure.Id == Chart_Data.Unit_Of_Measure_Id, isouter=True)
        .group_by(Observation_Type.Name, Unit_Of_Measure.Name)
        .all()
    )  # Group by both fields

    return aggregated_data_schema.dump(result)


def get_aggregated_chart_data_pandas():
    # Establish a connection to the SQLite database
    conn = sqlite3.connect("randomized_chart_data.sqlite")

    # Load data into Pandas DataFrames
    chart_data_df = pd.read_sql_query("SELECT * FROM Chart_Data", conn)
    observation_type_df = pd.read_sql_query("SELECT * FROM Observation_Type", conn)
    result_status_df = pd.read_sql_query("SELECT * FROM Result_Status", conn)
    unit_of_measure_df = pd.read_sql_query("SELECT * FROM Unit_Of_Measure", conn)

    # Close the connection
    conn.close()

    # Merge the DataFrames
    merged_df = chart_data_df.merge(
        observation_type_df, left_on="Observation_Type_Id", right_on="Id", how="left"
    )
    merged_df = merged_df.rename(columns={"Name": "Observation_Type"})
    merged_df = merged_df.merge(
        result_status_df,
        left_on="Result_Status_Id",
        right_on="Id",
        how="left",
        suffixes=("", "_r"),
    )
    merged_df = merged_df.rename(columns={"Name_r": "Result_Status"})
    merged_df = merged_df.merge(
        unit_of_measure_df,
        left_on="Unit_Of_Measure_Id",
        right_on="Id",
        how="left",
        suffixes=("", "_u"),
    )
    merged_df = merged_df.rename(columns={"Name_u": "Unit_Of_Measure"})

    # Calculate Valid Records
    conditions = (
        (merged_df["ERROR"] != 1)
        & (merged_df["WARNING"] != 1)
        & (merged_df["Result_Status_Id"] != 1)
    )
    merged_df["Valid_Records"] = conditions.astype(int)

    # Aggregate the data
    aggregation = {"VALUENUM": ["count", "min", "max"], "Valid_Records": "sum"}
    aggregated_data = merged_df.groupby(["Observation_Type", "Unit_Of_Measure"]).agg(
        aggregation
    )

    # Rename the columns for clarity
    aggregated_data.columns = [
        "Num_Admissions",
        "Min_Value",
        "Max_Value",
        "Valid_Records",
    ]
    aggregated_data = aggregated_data.reset_index()

    return aggregated_data.to_dict(orient="records")
