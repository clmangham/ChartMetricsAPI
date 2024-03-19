# Import necessary modules from Flask and the configuration file
from flask import render_template
import config

# Retrieve the Connexion app instance from the config module
app = config.connex_app

# Add the API endpoints to the app based on the OpenAPI specification file (api.yml)
# This file defines the API structure, endpoints, and their corresponding operations
app.add_api(config.basedir / "api.yml")

# Define a route for the root URL which serves the home page of the application
@app.route("/")
def home():
    # Render and return the home.html template when the root URL is accessed
    return render_template("home.html")

# Check if the script is executed directly (i.e., not imported as a module)
if __name__ == "__main__":
    # Run the app on all network interfaces (making it accessible from other machines in the network)
    # The port is set to 8000, and debug mode is turned off for production safety
    app.run(host="0.0.0.0", port=8000, debug=False)
