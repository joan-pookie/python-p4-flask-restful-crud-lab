#!/usr/bin/env python3

from app import app
from models import db, Plant

if __name__ == "__main__":
    with app.app_context():
        print("⚡ Debugging with Flask App Context ⚡")
        print("You can now access `db` and `Plant` directly.")
        import ipdb; ipdb.set_trace()
