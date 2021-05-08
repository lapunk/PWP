from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from .. import db
from .. import api
from ..utils import PlantBuilder, create_error_response
from ..models import Plant
from ..constants import *
import json


class PlantItem(Resource):

    def get(self, name):
        '''
        GET single plant information
        name used as identifier
        /api/plants/<name>/
        '''
        saved_plant = Plant.query.filter_by(name=name).first()
        if saved_plant is None:
            return create_error_response(
                status_code=404,
                title="Not found",
                message="No plant named {}".format(name)
            )

        body = PlantBuilder(
            uuid=saved_plant.uuid,
            name=saved_plant.name,
            specie=saved_plant.specie
        )
        body.add_control("self",
            url_for("api.plantitem", name=saved_plant.name))
        body.add_control("profile", PLANT_ITEM_PROFILE)
        body.add_control_delete_plant(name=saved_plant.name)
        body.add_control_modify_plant(name=saved_plant.name)
        body.add_namespace("plandi", LINK_RELATIONS_URL)

        return Response(response=json.dumps(body), status=200, mimetype=MASON)

    def put(self, name):
        '''
        PUT (UPDATE()) single plant information
        name used as identifier
        /api/plants/<name>/
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

        saved_plant = Plant.query.filter_by(name=name).first()

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

        db.session.commit()

        return Response(status=204, mimetype=MASON)

    def delete(self, name):
        '''
        DELETE single plant information
        name used as identifier
        /api/plants/<name>/
        '''
        saved_plant = Plant.query.filter_by(name=name).first()
        if saved_plant is None:
            return create_error_response(
                404,
                "Not found",
                "No plant with name {} found".format(name)
            )
        db.session.delete(saved_plant)
        db.session.commit()

        return Response(status=204, mimetype=MASON)


class PlantCollection(Resource):

    def get(self):
        '''
        Get PlantCollection Resource
        /api/species/
        '''
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
                specie=plant.specie
            )
            plantItem.add_control("self",
                url_for("api.plantitem", name=plant.name))
            plantItem.add_control("profile", PLANT_ITEM_PROFILE)
            body["items"].append(plantItem)
        body.add_namespace("plandi", LINK_RELATIONS_URL)
        body.add_control_add_plant()
        return Response(json.dumps(body), 200, mimetype=MASON)



    def post(self):
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

        plant = Plant(
            name=request.json["name"],
            specie=request.json["specie"]
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
            headers={"Location": url_for("api.plantitem", name=request.json["name"])})
