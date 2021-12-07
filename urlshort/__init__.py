from flask import Flask


def create_app(test_config=None):
    application=Flask(__name__)
    application.secret_key='h3hhg23h2g2h222hhghnb'


    from . import urlshort

    application.register_blueprint(urlshort.bp)

    return application
