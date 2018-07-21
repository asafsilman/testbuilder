from testbuilder.objectmap.python.python_objectmap import PythonObjectMapParse
from testbuilder.core.base.baseobjectmap import TBBaseObjectMap

import unittest

class TestPythonObjectMapParse(unittest.TestCase):
    def setUp(self):
        object_map_path = "testbuilder.objectmap.static.objectmap"
        self.parser = PythonObjectMapParse("test", object_map_path)

    def test_parse(self):
        object_map = self.parser.parse()

        self.assertIsInstance(object_map, TBBaseObjectMap)
        self.assertTrue(object_map.ready())
