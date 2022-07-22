# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate


def create_app(extensions=None,
               modules=None,
               config=None,
               converters=None,
               db=None):
    app = Flask(__name__)
    migrate = Migrate()

    if converters:
        for key in converters.keys():
            app.url_map.converters[key] = converters[key]

    configure_app(app, config)
    configure_extensions(app, extensions)
    configure_modules(app, modules)
    if db:
        migrate.init_app(app, db)
    return app

def configure_app(app, config):
    if config is not None:
        app.config.from_object(config)

def configure_modules(app, modules):
    for module in modules:
        app.register_blueprint(module)

def configure_extensions(app, exts):
    for ext in exts:
        ext.init_app(app)
