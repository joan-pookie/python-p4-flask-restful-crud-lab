#!/usr/bin/env python3

from server.app import app
from server.models import db, Plant

with app.app_context():
    # Clear existing plants
    db.session.query(Plant).delete()

    # Create plants without manually setting IDs
    aloe = Plant(
        name="Aloe",
        image="./images/aloe.jpg",
        price=11.50,
        is_in_stock=True,
    )

    zz_plant = Plant(
        name="ZZ Plant",
        image="./images/zz-plant.jpg",
        price=25.98,
        is_in_stock=False,
    )

    # Add to session and commit
    db.session.add_all([aloe, zz_plant])
    db.session.commit()

    print("🌱 Database seeded with sample plants!")
