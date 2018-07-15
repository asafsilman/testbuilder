import unittest
from testbuilder.core.engine import TBEngine
from testbuilder.core.base.baseinterface import TBBaseInterface

class TestTBEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TBEngine()

    def test_load_interface(self):
        interface_name = "basic_interface"
        interface_module = "testbuilder.contrib.basic"

        self.engine.load_interface(interface_name, interface_module)
        self.assertTrue(
            issubclass(self.engine.interfaces[interface_name], TBBaseInterface),
            "Registered interface is not of subclass TBBaseInterface"
        )