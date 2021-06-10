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


class PlantItem(Resource):

    def get(self, specie_name, plant_name):
        '''
        GET single plant information
        name used as identifier
        /api/specie/<specie_name>/plants/<plant_name>/
        '''
        saved_plant = Plant.query.filter_by(name=plant_name).first()
        if saved_plant is None:
            return create_error_response(
                status_code=404,
                title="Not found",
                message="No plant named {}".format(name)
            )

        body = PlantBuilder(
            id=saved_plant.id,
            name=saved_plant.name,
            specie=saved_plant.specie,
            acquired=saved_plant.acquired,
            location=saved_plant.location
        )

        body.add_control("self",
            url_for("api.plantitem", name=saved_plant.name, specie_name=saved_plant.specie))
        body.add_control("profile", PLANT_ITEM_PROFILE)
        body.add_control_delete_plant(name=saved_plant.name)
        body.add_control_modify_plant(name=saved_plant.name)
        body.add_namespace("plandi", LINK_RELATIONS_URL)

        return Response(response=json.dumps(body), status=200, mimetype=MASON)

    def put(self, specie_name, plant_name):
        '''
        PUT (UPDATE()) single plant information
        name used as identifier
        /api/specie/<specie_name>/plants/<plant_name>/
        '''

        if not request.json:
            return create_error_response(
                415,
                "Content type error",
                "Content type must be json"
            )
        try:
            validate(request.json, Plant.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                "Invalid JSON document",
                str(e)
            )

        saved_plant = Specie.query.filter_by(specie=specie_name).filter_by(name=plant_name).first()

        # Plant with given name does not exists in the database
        if saved_plant is None:
            return create_error_response(
                404,
                "Not found",
                "No plant with name {} found".format(name)
            )
        # Previous checks OK, update plant item
        saved_plant.name=request.json["name"]
        saved_plant.specie=request.json["specie"]
        saved_plant.acquired=request.json["acquired"]
        saved_plant.location=request.json["location"]

        db.session.commit()

        return Response(status=204, mimetype=MASON)

    def delete(self, name):
        '''
        DELETE single plant information
        name used as identifier
        /api/specie/<specie_name/plants/<plant_name>/
        '''
        saved_plant = Plant.query.filter_by(name=plant_name).first()
        if saved_plant is None:
            return create_error_response(
                404,
                "Not found",
                "No plant with name {} found".format(plant_name)
            )
        db.session.delete(saved_plant)
        db.session.commit()

        return Response(status=204, mimetype=MASON)


class PlantCollection(Resource):

    def get(self, specie_name):
        '''
        Get PlantCollection Resource
        /species/<specie_name>/plants/
        '''

        body = PlantBuilder(items=[])

        plants = Plant.query.all()
        if plants is None:
            return create_error_response(
                    404,
                    "Not found",
                    "Database is empty"
                    )

        body = PlantBuilder(items=[])

        for plant in plants:
            plantItem = PlantBuilder(
                    name=plant.name,
                    specie=plant.specie_name,
                    acquired=plant.acquired,
                    location=plant.location
                    )

            plantItem.add_control("self",
                    url_for("api.plantitem",
                        name=plant.name,
                        specie_name=plant.specie_name))

            plantItem.add_control("profile", PLANT_ITEM_PROFILE)

        body.add_namespace("plandi", LINK_RELATIONS_URL)
        body.add_control_add_plant()
        return Response(json.dumps(body), 200, mimetype=MASON)


    def post(self, specie_id):
        if not request.json:
            return create_error_response(
                415,
                "Wrong content type",
                "content type not json"
            )

        try:
            validate(request.json, Plant.get_schema())
        except ValidationError as e:
            return create_error_response(
                400,
                "Invalid json document",
                str(e)
            )

        specie_name = request.json["specie"]

        print(specie_name)

        saved_specie = Specie.query.filter_by(specie=specie_name).first()
        if saved_specie is None:
            return create_error_response(
                404,
                "Not found",
                "No plant with name {} found".format(plant_name)
            )

        plant = Plant(
            name=request.json["name"],
            specie_name=request.json["specie"],
            acquired=request.json["acquired"],
            location=request.json["location"],
            specie=saved_specie
        )
        try:
            db.session.add(plant)
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409,
                "Already exists",
                "Plant with name {} already exists".format(request.json["name"])
            )

        return Response(
            status=201,
            mimetype=MASON,
            headers={"Location": url_for("api.plantitem",
                name=request.json["name"],
                specie_name=request.json["specie"])})
