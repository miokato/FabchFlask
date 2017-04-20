from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object('fabch.config')


db = SQLAlchemy(app)

import fabch.views
