from flask import Blueprint


api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


def register_api_routes(app):

    app.register_blueprint(
        api_bp
    )

    return app