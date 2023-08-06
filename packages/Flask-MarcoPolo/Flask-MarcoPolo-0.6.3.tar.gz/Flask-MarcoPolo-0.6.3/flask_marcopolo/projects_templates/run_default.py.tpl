"""
Flask-MarcoPolo

run_{project_name}.py

To initiate your Flask-MarcoPolo project

"""

from flask import Flask
from flask.ext.marcopolo import MarcoPolo

# Import all views to be available in this project
from {project_name}.views import error, index

# The directory containing the project (views, templates, static)
project_dir = "./{project_name}"

# Project conf environment. Dev=Development, Prod=Production
project_config_env = "Dev"

# The project configuration relative to $project_name.module.class
project_config = "{project_name}.config.%s" % (project_config_env)

# MarcoPolo.init returns the flask app instance
app = MarcoPolo.init(app=Flask(__name__),
                            config=project_config,
                            project_dir=project_dir)

if __name__ == "__main__":
    app.run()
