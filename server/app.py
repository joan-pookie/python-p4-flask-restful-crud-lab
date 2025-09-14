from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Resource, Api
from models import db, Plant   # ✅ import from models.py

def create_app():
    app = Flask(__name__)

    # Config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init db + migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    # -------- Resources --------
    class PlantById(Resource):
        def get(self, id):
            plant = Plant.query.get_or_404(id)
            return jsonify(plant.to_dict())

        def patch(self, id):
            plant = Plant.query.get_or_404(id)
            data = request.get_json()

            if "is_in_stock" in data:   # ✅ lab test expects updating is_in_stock
                plant.is_in_stock = data["is_in_stock"]

            db.session.commit()
            return jsonify(plant.to_dict())

        def delete(self, id):
            plant = Plant.query.get_or_404(id)
            db.session.delete(plant)
            db.session.commit()
            return "", 204

    # Register resources
    api.add_resource(PlantById, "/plants/<int:id>")

    @app.route("/")
    def index():
        return "<h1>Plant API</h1>"

    return app


# Entrypoint
app = create_app()
