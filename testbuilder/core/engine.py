"""
Testbuilder Engine class
"""

from testbuilder.conf import settings
from testbuilder.core.base.baseinterface import TBBaseInterface
from testbuilder.core.exceptions import ImproperlyConfigured

import importlib

class TBEngine:
    interfaces = {}

    def __init__(self):
        pass

    def load_interface(self, interface_name, interface_module_name):
        mod = importlib.import_module(interface_module_name)
        entry = getattr(mod, "interface_entry", None)

        if entry is None:
            desc = "Interface {interface_name} is improperly configured".format_map(interface_name=interface_name)
            raise ImproperlyConfigured(desc)

        mod_path, _, class_name = entry.rpartition(".")
        module = importlib.import_module(mod_path)

        interface = getattr(module, class_name, None)

        if interface is None:
            desc = "Interface {interface_name} is improperly configured no class names {class_name}".format_map(interface_name=interface_name, class_name=class_name)
            raise ImproperlyConfigured(desc)

        if not issubclass(interface, TBBaseInterface):
            raise ImproperlyConfigured("Interface does not derive from TBBaseInterface")

        self.interfaces[interface_name] = interface()

    def ready(self):
        pass

        
