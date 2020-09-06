import os
import click

from flask import Flask

from IED.settings import config
from IED.apis.v1 import api_v1
from IED.extensions import db
from IED.apis.v1.apiException import APIException, ServerError
from werkzeug.exceptions import HTTPException

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
    register_error(app)
    return app


def register_extension(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api_v1, url_prefix='/api/v1')


def register_error(app):
    @app.errorhandler(Exception)
    def exception_solve(e):
        if isinstance(e, APIException):
            return e
        if isinstance(e, HTTPException):
            code = e.code
            # 获取具体的响应错误信息
            msg = e.description
            error_code = 1007
            return APIException(code=code, msg=msg, error_code=error_code)
        else:
            # 如果是调试模式,则返回e的具体异常信息。否则返回json格式的ServerException对象！
            # 针对于异常信息，我们最好用日志的方式记录下来。
            import traceback
            traceback.print_exc()
            if app.config["DEBUG"]:
                return e
            else:
                return ServerError()


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