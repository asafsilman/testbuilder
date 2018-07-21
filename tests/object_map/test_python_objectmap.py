from testbuilder.objectmap.python.python_objectmap import PythonObjectMapParse
from testbuilder.core.base.baseobjectmap import TBBaseObjectMap

import unittest

class TestPythonObjectMapParse(unittest.TestCase):
    def setUp(self):
        self.object_map_path = "testbuilder.objectmap.static.objectmap"
        self.parser = PythonObjectMapParse()

    def test_parse(self):
        object_map = self.parser.parse("test", self.object_map_path)

        self.assertIsInstance(object_map, TBBaseObjectMap)
        self.assertTrue(object_map.ready())
