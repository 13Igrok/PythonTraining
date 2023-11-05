import flask

import Misc.functions

app = flask.Flask(__name__)
app.secret_key = '#$ab9&^BB00_.'

# Setting DAO Class
import Models.DAO

DAO = Models.DAO.DAO(app)

# Registering blueprints
from routes.user import user_view
from routes.book import book_view
from routes.admin import admin_view

# Registering custom functions to be used within templates
app.jinja_env.globals.update(
    ago=Misc.functions.ago,
    str=str,
)

app.register_blueprint(user_view)
app.register_blueprint(book_view)
app.register_blueprint(admin_view)
