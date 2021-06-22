from flask import Blueprint
from flask_restful import Api

from . resources.specie import SpecieCollection, SpecieItem
from . resources.plant import PlantItem, PlantCollection
from . resources.diary import DiaryEntry, DiaryCollection
from . resources.plants_all import PlantsAll

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(SpecieCollection, "/species/")
api.add_resource(SpecieItem, "/species/<specie_name>/")
api.add_resource(PlantsAll, "/plants/")
api.add_resource(PlantCollection, "/species/<specie_name>/plants/")
api.add_resource(PlantItem, "/species/<specie_name>/plants/<plant_name>")
api.add_resource(DiaryCollection, "/plantdiary/")
api.add_resource(DiaryEntry, "/plantdiary/<entry_id>/")
