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
# {"Basic": "testbuilder.interfaces.basic"}
INSTALLED_INTERFACES = {}

INSTALLED_OBJECTMAPS = {}

##########################
# Application Settings
##########################

APP_DIRECTORY = ""
APP_NAME = ""
APP_LOGIN = {
    "username": "rmo_user",
    "password": "rmo_pass"
}

##########################
# Test Loader Setting
##########################
LOADER_SETTINGS = {
    "excel": {
        "loader": None
    },
    "yaml": {
        "loader": "testbuilder.loaders.yamlloader.loader.YAMLTestLoader",
        "middlewares": [
            ("basic", "testbuilder.middleware.basic")
        ]
    }
}
