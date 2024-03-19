# Import necessary modules and objects
from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy import fields as msfields
from marshmallow import Schema, fields



# Define the ORM models for the database tables
class Observation_Type(db.Model):
    __tablename__ = 'Observation_Type'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)

class Result_Status(db.Model):
    __tablename__ = 'Result_Status'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)


class Unit_Of_Measure(db.Model):
    __tablename__ = 'Unit_Of_Measure'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text)

# Marshmallow Schemas for serialization and deserialization
class ObservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Observation_Type
        load_instance = True
        sqla_session = db.session
        include_fk = True

class ResultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Result_Status
        load_instance = True
        sqla_session = db.session
        include_fk = True


class MeasureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit_Of_Measure
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Chart_Data(db.Model):
    __tablename__ = 'Chart_Data'
    Id = db.Column(db.Integer, primary_key=True)
    SUBJECT_ID = db.Column(db.Integer)
    HADM_ID = db.Column(db.Integer)
    ICUSTAY_ID = db.Column(db.Float)
    CHARTTIME = db.Column(db.DateTime)
    VALUENUM = db.Column(db.Float)
    WARNING = db.Column(db.Integer)
    ERROR = db.Column(db.Integer)
    STOPPED = db.Column(db.Integer)
    Observation_Type_Id = db.Column(db.Integer, db.ForeignKey('Observation_Type.Id'))
    Result_Status_Id = db.Column(db.Integer, db.ForeignKey('Result_Status.Id'))
    Unit_Of_Measure_Id = db.Column(db.Integer, db.ForeignKey('Unit_Of_Measure.Id'))

    observation_type = db.relationship('Observation_Type', backref='Chart_Data', foreign_keys=[Observation_Type_Id])
    result_status = db.relationship('Result_Status', backref='Chart_Data', foreign_keys=[Result_Status_Id])
    unit_of_measure = db.relationship('Unit_Of_Measure', backref='Chart_Data', foreign_keys=[Unit_Of_Measure_Id])


class DataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chart_Data
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True
        exclude = ('HADM_ID', 'ICUSTAY_ID', 'Observation_Type_Id', 'Result_Status_Id', 'SUBJECT_ID', 'Unit_Of_Measure_Id')  # Exclude fields
        ordered = True

    # observation_type = msfields.Nested(ObservationSchema)
    # result_status = msfields.Nested(ResultSchema)
    # unit_of_measure = msfields.Nested(MeasureSchema)

    Id = fields.Integer()
    CHARTTIME = fields.DateTime()
    VALUENUM = fields.Float()
    ERROR = fields.Integer(allow_none=True)
    WARNING = fields.Integer(allow_none=True)
    STOPPED = fields.Integer()

    # Custom methods to get related data
    observation_type = fields.Method("get_observation_type")
    result_status = fields.Method("get_result_status")
    unit_of_measure = fields.Method("get_unit_of_measure")

    def get_observation_type(self, obj):
        return obj.observation_type.Name if obj.observation_type else None

    def get_result_status(self, obj):
        return obj.result_status.Name if obj.result_status else None

    def get_unit_of_measure(self, obj):
        return obj.unit_of_measure.Name if obj.unit_of_measure else None



# Schemas for API output
class AggregatedDataSchema(Schema):
    Observation_Type = fields.Str()
    Unit_Of_Measure = fields.Str()
    Valid_Records = fields.Integer()
    Num_Admissions = fields.Integer()
    Min_Value = fields.Float()
    Max_Value = fields.Float()

# Initialize the schema instances
datum_schema =  DataSchema()
data_schema = DataSchema(many = True)
aggregated_data_schema = AggregatedDataSchema(many=True)



