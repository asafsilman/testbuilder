"""
Testbuilder Engine class
"""

from testbuilder.conf import settings
from testbuilder.core.base.baseinterface import TBBaseInterface
from testbuilder.core.base.basemiddleware import TBBaseMiddleware
from testbuilder.core.base.baseobjectmap import TBBaseObjectMapParser
from testbuilder.core.base.basetestloader import TBBaseTestLoader
from testbuilder.core.exceptions import ImproperlyConfigured

from testbuilder.utils.module_loader import load_module

class TBEngine:
    def __init__(self):
        self.interfaces = {}
        self.middlewares = {}
        self.objectmap_parsers = {}
        self.testloaders = {}
        self.profiles = {}

    def load_interface(self, interface_name, interface_module) -> None:
        interface_path = ".".join([interface_module, "interface_entry"])
        interface_entry = load_module(interface_path)

        interface = load_module(interface_entry)

        if not issubclass(interface, TBBaseInterface):
            raise ImproperlyConfigured("Interface does not derive from TBBaseInterface")

        self.interfaces[interface_name] = interface

    def load_middleware(self, middleware_name, middleware_module) -> None:
        middleware_path = ".".join([middleware_module, "middleware_entry"])
        middleware_entry = load_module(middleware_path)

        middleware = load_module(middleware_entry)

        if not issubclass(middleware, TBBaseMiddleware):
            raise ImproperlyConfigured("Middleware does not derive from TBBaseMiddleware")

        self.middlewares[middleware_name] = middleware

    def load_objectmap_parser(self, parser_name, parser_module) -> None:
        parser_path = ".".join([parser_module, "objectmap_parser_entry"])
        parser_entry = load_module(parser_path)

        parser = load_module(parser_entry)()

        if not isinstance(parser, TBBaseObjectMapParser):
            raise ImproperlyConfigured("Objectmap parser is not of instance TBBaseObjectMapParser")

        self.objectmap_parsers[parser_name]=parser

    def load_testloader(self, loader_name, loader_module) -> None:
        loader_path = ".".join([loader_module, "loader_entry"])
        loader_entry = load_module(loader_path)

        loader = load_module(loader_entry)()

        if not isinstance(loader, TBBaseTestLoader):
            raise ImproperlyConfigured("TestLoader is not of instance TBBaseTestLoader")

        self.testloaders[loader_name]=loader

    def load_profile(self, profile_name, profile) -> None:
        self.profiles[profile_name] = profile

    def create_tests(self, test_location, loader_name, profile_name):
        if loader_name not in self.testloaders:
            raise ImproperlyConfigured(f"No testloader installed named {loader_name}")
        if profile_name not in self.profiles:
            raise ImproperlyConfigured(f"No profile installed named {profile_name}")
        
        # Returns a list of tests from file
        tests = self.testloaders[loader_name].load_tests(test_location)

        for test in tests:
            profile = self.profiles[profile_name]

            ## Step 1. Load middlewares
            if "middlewares" in profile:
                for middleware_name in profile["middlewares"]:
                    middleware = self.middlewares[middleware_name]
                    test.load_middleware(middleware)

            ## Step 2. Load interfaces
            for interface_name, interface in self.interfaces.items():
                test.load_interface(interface, interface_name)

            ## Step 3. Load objectmap
            for objectmap_name in settings["OBJECT_MAPS"]:
                obj_parser_name, obj_location = settings["OBJECT_MAPS"][objectmap_name]

                if obj_parser_name not in self.objectmap_parsers:
                    raise ImproperlyConfigured(f"ObjectMap Parser {obj_parser_name} is not installed")

                obj_parser = self.objectmap_parsers[obj_parser_name]
                object_map = obj_parser.parse(objectmap_name, obj_location)

                test.load_object_map(object_map, objectmap_name)

        return tests

    def ready(self) -> None:
        """Checks the engine is ready to start executing test scripts

        * Checks Interfaces are not empty
        * Checks Middlewares are not empty
        * Checks Objectmap Parsers are not empty
        * Checks TestLoaders are not empty
        
        Returns:
            Boolean -- Is engine ready to start executing
        """

        ## Check interfaces are ready
        if not self.interfaces: # Is interfaces empty
            return False # Interface is empty

        ## Check objectmap parsers are not empty
        if not self.objectmap_parsers:
            return False

        ## Check testloaders are not empty
        if not self.testloaders:
            return False

        # All tests passed
        return True
