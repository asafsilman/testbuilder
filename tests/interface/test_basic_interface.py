from testbuilder.interface.basic.interface import BasicInterface
from testbuilder.core.base.basestep import StepContext
from testbuilder.core.base.basetest import TBBaseTest
from testbuilder.core.base.baseobjectmap import (TBBaseObjectMap, TBBasePage)

import unittest

class TestBasicInterface(unittest.TestCase):
    def setUp(self):
        self.test = TBBaseTest()
        self.interface = BasicInterface()

    def test_object_map(self):
        # Prepare objectmap
        object_map = TBBaseObjectMap("test_object_map")
        page1 = TBBasePage("test_page", {"obj": "sample:test"})
        object_map.load_page(page1)

        # Prepare step context
        s_c = StepContext(self.test)
        s_c.step_argument_1 = "test_object_map"
        s_c.step_argument_2 = "test_page"

        self.test.load_object_map(object_map, "test_object_map")

        self.interface.ObjectMap(s_c)

        self.assertIsNotNone(s_c.object_map)
        self.assertEqual(s_c.object_map, object_map)
        self.assertEqual(s_c.object_map.get_current_page(), page1)
