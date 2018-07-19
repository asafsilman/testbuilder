import unittest
from testbuilder.core.engine import TBEngine
from testbuilder.core.base.baseinterface import TBBaseInterface
from testbuilder.core.base.basemiddleware import TBBaseMiddleware

class TestTBEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TBEngine()

    def test_load_interface(self):
        interface_name = "basic_interface"
        interface_module = "testbuilder.interface.basic"

        self.engine.load_interface(interface_name, interface_module)
        self.assertTrue(
            issubclass(self.engine.interfaces[interface_name], TBBaseInterface),
            "Registered interface is not of subclass TBBaseInterface"
        )

    def test_load_middleware(self):
        middleware_name = "basic_middleware"
        middleware_module = "testbuilder.middleware.basic"

        self.engine.load_middleware(middleware_name, middleware_module)
        self.assertTrue(
             issubclass(self.engine.middlewares[middleware_name], TBBaseMiddleware),
            "Registered middleware is not of subclass TBBaseMiddleware"
        )
