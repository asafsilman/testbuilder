"""Loads instance of TBBaseEngine"""

from testbuilder.conf import settings
from testbuilder.core.engine import TBEngine
from testbuilder.utils.module_loader import load_module


def load_engine():
    """
    Create a TBEngine instance, load all settings from testbuilder settings

    Returns:
        TBEngine -- The loaded engine instance
    """
    engine=TBEngine()

    ## Step 1. Load Interfaces
    for interface_name in settings["INSTALLED_INTERFACES"]:
        interface_module = settings["INSTALLED_INTERFACES"][interface_name]

        engine.load_interface(interface_name, interface_module)

    ## Step 2. Load Middlwares
    for middleware_name in settings["INSTALLED_MIDDLEWARES"]:
        middleware_module = settings["INSTALLED_MIDDLEWARES"][middleware_name]

        engine.load_middleware(middleware_name, middleware_module)

    ## Step 3. Load ObjectMap Parsers
    for objmap_parser_name in settings["INSTALLED_OBJECTMAPS_PARSERS"]:
        objmap_parser_module = settings["INSTALLED_OBJECTMAPS_PARSERS"][objmap_parser_name]

        engine.load_objectmap_parser(objmap_parser_name, objmap_parser_module)

    ## Step 4. Load TestLoaders
    for testloader_name in settings["INSTALLED_TESTLOADERS"]:
        testloader_module = settings["INSTALLED_TESTLOADERS"][testloader_name]

        engine.load_testloader(testloader_name, testloader_module)

    ## Step 5. Load profiles
    for profile_name in settings["INSTALLED_PROFILES"]:
        profile = settings["INSTALLED_PROFILES"][profile_name]

        engine.load_profile(profile_name, profile)

    return engine