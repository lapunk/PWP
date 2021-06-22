from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from .. import db
from .. import api
from ..utils import PlantBuilder, create_error_response
from ..models import Plant, Specie
from ..constants import *
import json

class PlantsAll(Resource):

    def get(self):
        '''
        Get PlantsAll Resource
        /plants/
        '''

        body = PlantBuilder(items=[])

        for specie in Specie.query.all():
            for plant in Plant.query.filter_by(specie_name=specie.specie).all():

                plantItem = PlantBuilder(
                    name=plant.name,
                    specie_name=plant.specie_name,
                    acquired=plant.acquired,
                    location=plant.location
                )

                plantItem.add_control("self",
                        url_for("api.plantsall"))

                plantItem.add_control("profile", PLANT_COLLECTION_PROFILE)
                body["items"].append(plantItem)

        body.add_namespace("plandi", LINK_RELATIONS_URL)
        body.add_control_add_plants_all()

        return Response(json.dumps(body), 200, mimetype=MASON)

