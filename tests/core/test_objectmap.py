from testbuilder.core.base.baseobjectmap import TBBaseObjectMap
import unittest

class TestObjectMap(unittest.TestCase):
    def setUp(self):
        obj = {"Test_Element": "sample://test"}
        self.object_map = TBBaseObjectMap(
            name="test",
            page="test_page",
            object_map=obj
        )

    def test_get_from_object_map(self):
        interface, element = self.object_map.get_from_object_map("Test_Element")

        self.assertEqual(interface, "sample")
        self.assertEqual(element, "//test")

    def test_object_map_name(self):
        self.assertEqual(self.object_map.name, "test")

    def test_object_map_page(self):
        self.assertEqual(self.object_map.page, "test_page")

    def test_ready(self):
        object_map_1 = TBBaseObjectMap()

        self.assertFalse(object_map_1.ready())
        self.assertTrue(self.object_map.ready())
