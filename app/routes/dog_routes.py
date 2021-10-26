from app import db
from app.models.dog import Dog
from flask import Blueprint, jsonify, make_response, request, abort

dog_bp = Blueprint("dog", __name__,url_prefix="/dogs")

# Helper Functions
def check_valid_int(number, parameter_type):
    try:
        number = int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_dog_from_id(dog_id):
    check_valid_int(dog_id, "dog_id")
    return Dog.query.get_or_404(dog_id, description="{dog not found}")

# Routes
@dog_bp.route("", methods=["GET"])
def read_all_dogs():
    
    age_query = request.args.get("age")
    older_query = request.args.get("older")
    sort_query = request.args.get("sort")

    dogs = Dog.query

    if age_query:
        check_valid_int(age_query, "age")
        dogs = dogs.filter_by(age=age_query)
    elif older_query:
        check_valid_int(older_query, "older")
        dogs = dogs.filter(Dog.age > older_query)

    if sort_query == "asc":
        dogs = dogs.order_by(Dog.age.asc())
    elif sort_query == "desc":
        dogs = dogs.order_by(Dog.age.desc())

    dogs_response = []
    for dog in dogs:
        dogs_response.append(
            dog.to_dict()
        )
    return jsonify(dogs_response)

@dog_bp.route("", methods=["POST"])
def create_dog():
    request_body = request.get_json()
    if "name" not in request_body or "breed" not in request_body:
        return {"error": "incomplete request body"}, 400

    new_dog = Dog(
        name=request_body["name"],
        breed=request_body["breed"],
    )

    db.session.add(new_dog)
    db.session.commit()

    return make_response(f"Dog {new_dog.name} created!", 201)

@dog_bp.route("/<dog_id>", methods=["GET"])
def read_dog(dog_id):
    dog = get_dog_from_id(dog_id)

    return dog.to_dict()

@dog_bp.route("/<dog_id>", methods=["PATCH"])
def update_dog(dog_id):
    dog = get_dog_from_id(dog_id)
    request_body = request.get_json()

    if "name" in request_body:
        dog.name = request_body["name"]
    if "breed" in request_body:
        dog.breed = request_body["breed"]
    if "age" in request_body:
        dog.age = request_body["age"]
    
    db.session.commit()
    return jsonify(dog.to_dict())

@dog_bp.route("/<dog_id>", methods=["DELETE"])
def delete_dog(dog_id):
    dog = get_dog_from_id(dog_id)

    db.session.delete(dog)
    db.session.commit()
    return jsonify(dog.to_dict())

    
    