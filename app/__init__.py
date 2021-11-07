from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'lksjsdifjdscm'
    from .api import nps
    app.register_blueprint(nps.parks_blueprint)
    return app

app = create_app()
