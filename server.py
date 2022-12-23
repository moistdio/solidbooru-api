from application import create_app
from loginmanager import create_loginmanager
from database import create_database, populate_database


def main():
    app = create_app()
    create_database(app)
    create_loginmanager(app)
    populate_database(app)
    app.run(host=app.config['IP'], port=app.config['PORT'], debug=False)


if __name__ == "__main__":
    main()
