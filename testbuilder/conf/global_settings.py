"""
Global configuration file with all default vaues
"""

# Collection of installed interfaces
# 
# Structure
# Key: Interface prefix
# Value: Interface location
# 
# Example
# "Basic": "testbuilder.interfaces.basic"
INSTALLED_INTERFACES = {}

# List of middlewares to use 
STEP_MIDDLEWARE = []

##########################
# Application Settings
##########################

APP_DIRECTORY = ""
APP_NAME = ""
APP_LOGIN = {
    "username": "rmo_user",
    "password": "rmo_pass"
}
