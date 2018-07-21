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

        parser = load_module(parser_entry)

        if not issubclass(parser, TBBaseObjectMapParser):
            raise ImproperlyConfigured("Objectmap parser does not derive from TBBaseObjectMapParser")

        self.objectmap_parsers[parser_name]=parser

    def load_testloader(self, loader_name, loader_module) -> None:
        loader_path = ".".join([loader_module, "loader_entry"])
        loader_entry = load_module(loader_path)

        loader = load_module(loader_entry)

        if not issubclass(loader, TBBaseTestLoader):
            raise ImproperlyConfigured("TestLoader does not derive from TBBaseTestLoader")

        self.testloaders[loader_name]=loader

    def load_profile(self, profile_name, profile) -> None:
        self.profiles[profile_name] = profile

    def create_test(self, test_location, loader, profile):
        pass

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
