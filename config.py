# Import necessary libraries
import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Determine the base directory path of the current file.
# This is used to set file paths relative to the location of this configuration file.
basedir = pathlib.Path(__file__).parent.resolve()

# Initialize the Connexion application.
# Connexion is an extension of Flask that adds Swagger/OpenAPI support to the application.
# The specification_dir is set to the base directory where the API specification file (api.yml) is expected to be found.
connex_app = connexion.App(__name__, specification_dir=basedir)

# Extract the underlying Flask app from the Connexion app.
app = connex_app.app

# Configure the SQLAlchemy database URI.
# This application uses SQLite for simplicity and ease of setup, and the database file is located in the base directory.
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'randomized_chart_data.sqlite'}"

# Disable SQLAlchemy's modification tracking feature for performance reasons.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the SQLAlchemy object, which provides ORM capabilities for the application.
db = SQLAlchemy(app)

# Initialize Marshmallow, which is used for object serialization and deserialization (converting between Python objects and JSON).
ma = Marshmallow(app)