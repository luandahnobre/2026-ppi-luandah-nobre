import os
from flask import Flask
from dotenv import load_dotenv


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import news_bp
    app.register_blueprint(news_bp.bp)
    app.add_url_rule('/', endpoint='index')

    return app
