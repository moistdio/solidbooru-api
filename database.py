from flask_sqlalchemy import SQLAlchemy
from db.init.rank import populate_ranks

db = SQLAlchemy()


def create_database(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return db

def populate_database(app):
    ranks = []

    with app.app_context():
        migr_list = [
            populate_ranks()
        ]

        for item in migr_list:
            migration = item[-1]

            print(migration.query.filter_by(name = migration.name).first())

            if migration.query.filter_by(name = migration.name).first():
                return None

            for query in item:
                db.session.add(query)
            db.session.commit()
