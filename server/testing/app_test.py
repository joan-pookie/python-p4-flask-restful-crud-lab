import pytest
import json
from server.app import create_app, db
from server.models import Plant

# Use the application factory
app = create_app()

@pytest.fixture(autouse=True)
def run_around_tests():
    """
    Setup and teardown for each test.
    Creates a fresh in-memory database so tests don’t interfere with each other.
    """
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


class TestPlant:
    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        with app.app_context():
            plant = Plant(name="Rose", image="rose.png", price=5, is_in_stock=True)
            db.session.add(plant)
            db.session.commit()

            response = app.test_client().get(f"/plants/{plant.id}")
            assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        with app.app_context():
            plant = Plant(name="Tulip", image="tulip.png", price=7, is_in_stock=True)
            db.session.add(plant)
            db.session.commit()

            response = app.test_client().get(f"/plants/{plant.id}")
            data = json.loads(response.data.decode())

            assert type(data) == dict
            assert data["id"] == plant.id
            assert data["name"] == "Tulip"

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        with app.app_context():
            plant = Plant(name="Orchid", image="orchid.png", price=10, is_in_stock=True)
            db.session.add(plant)
            db.session.commit()

            response = app.test_client().patch(
                f"/plants/{plant.id}",
                json={"is_in_stock": False}
            )
            data = json.loads(response.data.decode())

            assert response.status_code == 200
            assert data["is_in_stock"] is False
