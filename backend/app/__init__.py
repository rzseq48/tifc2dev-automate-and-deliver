from flask import Flask, jsonify

from app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///helpdesk.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app import models  # Register models before creating tables.

    with app.app_context():
        db.create_all()

    @app.get("/")
    def health():
        return jsonify({"status": "running"}), 200

    @app.get("/api/tickets")
    def list_tickets():
        return jsonify(
            [ticket.to_dict() for ticket in models.Ticket.query.order_by(models.Ticket.id)]
        ), 200

    return app
