from testbuilder.core.base.baseobjectmap import TBBaseObjectMap, TBBasePage, Element
import unittest

class TestTBBaseObjectMap(unittest.TestCase):
    def setUp(self):
        elements_1 = {"test_element1": "sample://test"}
        elements_2 = {"test_element2": "test://sample"}
        
        self.page_1 = TBBasePage("page_1", elements_1)
        self.page_2 = TBBasePage("page_2", elements_2)

        self.object_map = TBBaseObjectMap(name="test")

        self.object_map.load_page(self.page_1)
        self.object_map.load_page(self.page_2)

    def test_get_from_object_map(self):
        self.object_map.switch_page("page_1")
        element1 = self.object_map.get_element("test_element1")
        
        self.object_map.switch_page("page_2")
        element2 = self.object_map.get_element("test_element2")

        self.assertIsInstance(element1, Element)
        self.assertIsInstance(element2, Element)

        self.assertEqual(element1.interface_prefix, "sample")
        self.assertEqual(element1.element, "//test")

        self.assertEqual(element2.interface_prefix, "test")
        self.assertEqual(element2.element, "//sample")

    def test_get_page_names(self):
        names = self.object_map.get_page_names()
        
        self.assertEqual(len(names), 2)
        self.assertIn("page_1", names)
        self.assertIn("page_2", names)

    def test_get_current_page(self):
        self.object_map.switch_page("page_1")

        self.assertEqual(self.object_map.get_current_page(), self.page_1)

        self.object_map.switch_page("page_2")
        self.assertEqual(self.object_map.get_current_page(), self.page_2)

    def test_object_map_name(self):
        self.assertEqual(self.object_map.name, "test")

    def test_ready(self):
        object_map_1 = TBBaseObjectMap("object_map_not_ready")

        self.assertFalse(object_map_1.ready())
        self.assertFalse(self.object_map.ready()) # current_page is not set

        self.object_map.switch_page("page_1")
        self.assertTrue(self.object_map.ready())

class TestTBBasePage(unittest.TestCase):
    def setUp(self):
        elements = {"test_element1": "sample://test"}
        self.page = TBBasePage("page_1", elements)

    def test_get_element(self):
        element = self.page.get_element("test_element1")

        self.assertIsInstance(element, Element)

        self.assertEqual(element.interface_prefix, "sample")
        self.assertEqual(element.element, "//test")

    def test_add_element(self):
        self.page.add_element("test_element2", "test://sample")
        element = self.page.get_element("test_element2")

        self.assertIsInstance(element, Element)

    def test_ready(self):
        page = TBBasePage("page_will_fail")

        self.assertFalse(page.ready())
        self.assertTrue(self.page.ready())

