"""
Testbuilder Engine class
"""

from testbuilder.conf import settings
from testbuilder.core.base.baseinterface import TBBaseInterface
from testbuilder.core.exceptions import ImproperlyConfigured

import importlib

def load_module(module):
    module_path, _, class_name = module.rpartition(".")
    module = importlib.import_module(module_path)

    return getattr(module, class_name, None)


class TBEngine:
    interfaces = {}
    middlewares = {}
    tests = {}

    def __init__(self):
        pass

    def load_interface(self, interface_name, interface_module):
        interface_path = ".".join([interface_module, "interface_entry"])
        interface_entry = load_module(interface_path)

        interface = load_module(interface_entry)

        if not issubclass(interface, TBBaseInterface):
            raise ImproperlyConfigured("Interface does not derive from TBBaseInterface")

        self.interfaces[interface_name] = interface

    def ready(self):
        """Checks the engine is ready to start executing test scripts

        * Checks Interfaces are not empty
        * Checks Middlewares are not empty
        * Checks Tests are not empty
        
        Returns:
            Boolean -- Is engine ready to start executing
        """

        ## Check interfaces are ready
        if not self.interfaces: # Is interfaces empty
            
            return False # Interface is empty

        ## Check tests are ready
        if not self.tests: # Is tests empty
            return False # Tests is empty

        # All tests passed
        return True

        
