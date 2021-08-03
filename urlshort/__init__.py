from flask import Flask


def create_app(test_config=None):
    app=Flask(__name__)
    app.secret_key='h3hhg23h2g2h222hhghnb'


    from . import urlshort

    app.register_blueprint(urlshort.bp)

    return app
