from server.app import create_app
from server.models import db, User, Recipe, Plant

app = create_app()

with app.app_context():
    print("🌱 Seeding database...")

    # Clear old data
    db.drop_all()
    db.create_all()

    # --- Users ---
    user1 = User(username="alice", bio="Plant lover", image_url="https://i.imgur.com/abc123.jpg")
    user1.set_password("password123")

    user2 = User(username="bob", bio="Chef in training", image_url="https://i.imgur.com/xyz789.jpg")
    user2.set_password("password456")

    db.session.add_all([user1, user2])
    db.session.commit()

    # --- Recipes ---
    recipe1 = Recipe(
        title="Avocado Toast",
        instructions="Toast bread, smash avocado, sprinkle salt and pepper.",
        minutes_to_complete=5,
        user_id=user1.id,
    )
    recipe2 = Recipe(
        title="Pasta Salad",
        instructions="Boil pasta, add veggies, mix with dressing.",
        minutes_to_complete=15,
        user_id=user2.id,
    )

    db.session.add_all([recipe1, recipe2])
    db.session.commit()

    # --- Plants ---
    plant1 = Plant(name="Monstera", image="https://i.imgur.com/plant1.jpg", price=20.5, is_in_stock=True)
    plant2 = Plant(name="Snake Plant", image="https://i.imgur.com/plant2.jpg", price=15.0, is_in_stock=True)
    plant3 = Plant(name="Aloe Vera", image="https://i.imgur.com/plant3.jpg", price=12.0, is_in_stock=False)

    db.session.add_all([plant1, plant2, plant3])
    db.session.commit()

    print("✅ Done seeding!")
