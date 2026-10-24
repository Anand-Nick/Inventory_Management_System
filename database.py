from models import db, Admin


def create_database(app):
    """
    Creates all database tables and inserts
    the default admin if it does not exist.
    """

    with app.app_context():
        # Create all tables
        db.create_all()

        # Check whether admin already exists
        admin = Admin.query.filter_by(username="Anand").first()

        if admin is None:
            admin = Admin(
                username="Anand",
                password="anand123"
            )

            db.session.add(admin)
            db.session.commit()

            print("Default Admin Created Successfully!")
        else:
            print("Admin Already Exists!")