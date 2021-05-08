from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from .. import db
from .. import api
from ..utils import PlantBuilder, create_error_response
from ..models import Specie
from ..constants import *
import json
from .. import models


class SpecieItem(Resource):

    def get(self, plant_id):
        '''
        GET single specie information
        uuid used as identifier
        /api/species/<plant_id>/
        '''
        saved_specie = Specie.query.filter_by(id=plant_id).first()
        if saved_specie is None:
            return create_error_response(
                title="Not found",
                status_code=404,
                message="No specie with id {} saved".format(plant_id)
            )

        body = PlantBuilder(
            id=saved_specie.id,
            instruction=saved_specie.instruction,
            specie=saved_specie.specie
        )
        body.add_control("self",
            url_for("api.specie", plant_id=saved_specie.id))
        body.add_control("profile", SPECIE_PROFILE)
        body.add_control_delete_specie(plant_id=saved_specie.id)
        body.add_control_modify_specie(plant_id=saved_specie.id)
        body.add_namespace("plandi", LINK_RELATIONS_URL)

        return Response(response=json.dumps(body), status=200, mimetype=MASON)

    def put(self, plant_id):
        '''
        PUT (UPDATE()) single specie information
        uuid used as identifier
        /api/species/<plant_id>/
        '''

        if not request.json:
            return create_error_response(
                415,
                "Content type error",
                "Content type must be json"
            )
        try:
            validate(request.json, Specie.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                "Invalid JSON document",
                str(e)
            )

        saved_specie = Specie.query.filter_by(uuid=plant_id).first()

        # Plant with given name does not exists in the database
        if saved_specie is None:
            return create_error_response(
                404,
                "Not found",
                "No plant with uuid {} found".format(plant_id)
            )
        # Previous checks OK, update plant item
        saved_specie.instruction=request.json["instruction"]
        saved_specie.specie=request.json["specie"]

        db.session.commit()

        return Response(status=204, mimetype=MASON)


    def delete(self, plant_id):
        '''
        DELETE single specie information
        /api/species/<plant_id>/
        '''

        saved_plant = Specie.query.filter_by(uuid=plant_id).first()
        if saved_plant is None:
            return create_error_response(
                404,
                "Not found",
                "No plant with id {} found".format(plant_id)
            )

        db.session.delete(saved_plant)
        db.session.commit()

        return Response(status=204, mimetype=MASON)

class SpecieCollection(Resource):
    def get(self):
        '''
        Get Specie Collection Resource
        '''
        gen_plants = Specie.query.all()
        if gen_plants is None:
            return create_error_response(
            404,
            "Not found",
            "Database is empty"
            )

        body = PlantBuilder(items=[])
        for plant in gen_plants:
            plantItem = PlantBuilder(
                instruction=plant.instruction,
                specie=plant.specie
            )
            plantItem.add_control("self",
                url_for("api.specieitem", plant_id=plant.id))
            plantItem.add_control("profile", SPECIE_PROFILE)
            body["items"].append(plantItem)
        body.add_namespace("plandi", LINK_RELATIONS_URL)
        body.add_control_add_specie()
        return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self):
        if not request.json:
            return create_error_response(
                415,
                "Wrong content type",
                "content type not json")

        try:
            validate(request.json, Specie.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                "Invalid json document",
                str(e)
            )

        gen_plant = Specie(
            instruction=request.json["instruction"],
            specie=request.json["specie"]
        )
        try:
            db.session.add(gen_plant)
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409,
                "Already exists",
                "Plant with id {} already exists".format(gen_plant.id)
            )

        return Response(
            status=201,
            mimetype=MASON)
