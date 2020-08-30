import os
import click

from flask import Flask

from IED.settings import config
from IED.apis.v1 import api_v1
from IED.extensions import db

from IED.models.article import *
from IED.models.resources import *
from IED.models.user import *
from IED.models.log import *

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('IED')
    app.config.from_object(config[config_name])

    register_extension(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extension(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api_v1, url_prefix='/api/v1')


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop。')
    def initdb(drop):
        """initialize the database"""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo("Drop tables.")
        db.create_all()
        click.echo('Initialize database.')