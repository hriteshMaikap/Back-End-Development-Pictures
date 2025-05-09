from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return picture with given id"""
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    
    abort(404)

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    picture = request.get_json()
    
    # Check if picture with id already exists
    for existing_picture in data:
        if existing_picture["id"] == picture["id"]:
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Add new picture to data list
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE 
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture with the given id"""
    # Get updated picture data from request body
    updated_picture = request.get_json()
    
    # Find and update the picture
    for i, picture in enumerate(data):
        if picture["id"] == id:
            # Update picture while preserving its id
            updated_picture["id"] = id
            data[i] = updated_picture
            return jsonify(data[i]), 200
    
    # Picture not found
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture with the given id"""
    # Find and delete the picture
    for i, picture in enumerate(data):
        if picture["id"] == id:
            data.pop(i)
            return "", 204
    
    # Picture not found
    return jsonify({"message": "picture not found"}), 404
