# -*- coding: utf-8 -*-
import config
from create_app import create_app
from extensions import db
from views.tasks import tasks
from views.main import main

blueprints = [
    tasks,
    main
]

extensions = [
    db
]

app = create_app(extensions=extensions, modules=blueprints, config=config, db=db)