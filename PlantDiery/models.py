import click
from flask.cli import with_appcontext
from . import db

class Plant(db.Model):
    """
    Plant table
    name:     String(64) (unique) (identifier)
    specie:   String
    acquired: DateTime (optional)
    location: String (optional)
    """

    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    specie = db.Column(db.String(128), nullable=False)
    acquired = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(128), nullable=True)

    @staticmethod
    def get_schema():
        """Returns schema for Plant"""
        schema = {
                "type": "object",
                "required": ["specie", "name"]
                }
        props = schema["properties"] = {}
        props["specie"] = {
                "description": "Specie of the plant",
                "type": "string"
                }
        props["name"] = {
                "description": "Name of the plant",
                "type": "string"
                }
        props["acquired"] = {
                "description": "Date of acquiral of the plant",
                "type": "string",
                #"pattern": "^[0-9]{4}-[01][0-9]-[0-3][0-9]T[0-9]{2}:[0-5][0-9]:[0-5][0-9]Z$"
        }
        props["location"] = {
                "description": "Placement of the plant",
                "type": "string"
        }
        return schema

class Specie(db.Model):
    """
    Specie table
    instruction: String
    specie:       String
    water:        String (optional)
    humidity:     String (optional)
    temperature:  String (optional)
    soil:         String (optional)
    """

    uuid = db.Column(db.Integer, primary_key=True)
    instruction = db.Column(db.String(512), nullable=False)
    specie = db.Column(db.String(128), nullable=False)
    water = db.Column(db.String(64), nullable=True)
    humidity = db.Column(db.String(64), nullable=True)
    temperature = db.Column(db.String(64), nullable=True)
    soil = db.Column(db.String(64), nullable=True)

    @staticmethod
    def get_schema():
        """ Returns the schema for Specie"""
        schema = {
                "type": "object",
                "required": ["instruction", "specie"]
                }
        props = schema["properties"] = {}
        props["instruction"] = {
                "description": "Instructions how to take care of the plant",
                "type": "string"
                }
        props["specie"] = {
                "description": "Specie of the plant",
                "type": "string"
                }
        props["water"] = {
                "description" :"Watering information",
                "type": "string"
        }
        props["humidity"] = {
                "description": "Description of the humidity in plant's location",
                "type": "string"
        }
        props["temperature"] = {
                "description": "Temperature in the plant's location",
                "type": "string"
        }
        props["soil"] = {
                "description": "Type of soil used",
                "type": "string"
        }
        return schema


class Diary(db.Model):
    """
    Diary database
    date:       DateTime
    description:String
    plant:      String
    water_info: String (optional)
    wellbeing:  String (optional)
    """
    __tablename__ = "diary"
    uuid = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    #date = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.String, nullable=False)
    water_info = db.Column(db.String, nullable=True)
    wellbeing = db.Column(db.String, nullable=True)
    plant = db.Column(db.String, nullable=False)

    @staticmethod
    def get_schema():
        """ Returns the schema for Diary"""
        schema = {
                "type": "object",
                "required": ["date", "description", "plant"]
                }
        props = schema["properties"] = {}
        props["date"] = {
                "description": "Date of the diary record",
                "type": "string",
                #"pattern": "^[0-9]{4}-[01][0-9]-[0-3][0-9]T[0-9]{2}:[0-5][0-9]:[0-5][0-9]Z$"
                #"pattern": "/^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/"
                }
        props["description"] = {
                "description": "The journal itself",
                "type": "string"
                }
        props["water_info"] = {
                "description": "Watering information",
                "type": "string"
                }
        props["wellbeing"] = {
                "description": "Overall description of the plant's wellbeing",
                "type": "string"
                }
        props["plant"] = {
                "description": "Plant's name",
                "type": "string"
                }
        return schema

# Creates command "init-db" which can be used to create db
@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
