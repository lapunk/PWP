from flask import Blueprint
from flask_restful import Api

from . resources.specie import SpecieCollection, SpecieItem
from . resources.plant import PlantItem, PlantCollection
from . resources.diary import DiaryEntry, DiaryCollection

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(SpecieCollection, "/species/")
api.add_resource(SpecieItem, "/species/<specie_id>/")
api.add_resource(PlantCollection, "/species/<specie_id>/plants/")
api.add_resource(PlantItem, "/species/<specie_id>/plants/<plant_id>")
api.add_resource(DiaryCollection, "/plantdiary/")
api.add_resource(DiaryEntry, "/plantdiary/<entry_id>/")
