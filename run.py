#!/usr/bin/env python

import os

from app import create_app, db

app = create_app(os.getenv("FLASK_ENV", "development"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, host="0.0.0.0", port=5000)