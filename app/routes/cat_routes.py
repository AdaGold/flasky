from flask import Blueprint, jsonify, abort, make_response

cat_bp = Blueprint("cat", __name__,url_prefix="/cats")

class Cat:
    def __init__(self, id, name, color, personality):
        self.id = id
        self.name = name
        self.color = color
        self.personality = personality

cats = [
    Cat(1, "Muna", "black", "mischevious"),
    Cat(2, "Matthew", "spotted", "cuddly"),
    Cat(3, "George", "Gray","Sassy")
]

# get all cats
@cat_bp.route("", methods=["GET"])
def handle_cats():
    cats_response = [vars(cat) for cat in cats]
    return jsonify(cats_response)

# get one cat
@cat_bp.route("/<cat_id>", methods=["GET"])
def handle_cat(cat_id):
    try:
        cat_id = int(cat_id)
    except:
        return abort(make_response({"message": f"Cat {cat_id} invalid"}, 400))

    for cat in cats:
        if cat.id == cat_id:
            return vars(cat)
            
    return abort(make_response({"message": f" Cat {cat_id} Not found"}, 404))