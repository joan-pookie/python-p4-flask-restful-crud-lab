from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from server.models import db, Plant
from server.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)

    # --------- ROUTES ---------

    # GET all plants
    @app.route("/plants", methods=["GET"])
    def get_plants():
        plants = Plant.query.all()
        return jsonify([p.to_dict() for p in plants]), 200

    # POST a new plant
    @app.route("/plants", methods=["POST"])
    def create_plant():
        data = request.get_json()
        new_plant = Plant(
            name=data.get("name"),
            image=data.get("image"),
            price=data.get("price"),
            is_in_stock=data.get("is_in_stock", True),
        )
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201

    # GET one plant by id
    @app.route("/plants/<int:id>", methods=["GET"])
    def get_plant(id):
        plant = db.session.get(Plant, id)   # ✅ updated
        if not plant:
            return jsonify({"error": "Plant not found"}), 404
        return jsonify(plant.to_dict()), 200

    # PATCH update plant
    @app.route("/plants/<int:id>", methods=["PATCH"])
    def update_plant(id):
        plant = db.session.get(Plant, id)   # ✅ updated
        if not plant:
            return jsonify({"error": "Plant not found"}), 404
        data = request.get_json()
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]
        if "price" in data:
            plant.price = data["price"]
        db.session.commit()
        return jsonify(plant.to_dict()), 200

    # DELETE plant
    @app.route("/plants/<int:id>", methods=["DELETE"])
    def delete_plant(id):
        plant = db.session.get(Plant, id)   # ✅ updated
        if not plant:
            return jsonify({"error": "Plant not found"}), 404
        db.session.delete(plant)
        db.session.commit()
        return jsonify({"message": "Plant deleted"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
