"""Python objectmap parser"""

from testbuilder.utils.module_loader import load_module
from testbuilder.core.base.baseobjectmap import (
    TBBaseObjectMapParser, TBBaseObjectMap, TBBasePage
)

class PythonObjectMapParse(TBBaseObjectMapParser):
    def parse(self, object_map_name, object_map_location):
        object_map_module = ".".join([object_map_location, "OBJECT_MAP"])

        object_map = TBBaseObjectMap(object_map_name)
        python_object_map = load_module(object_map_module)
        
        for page_name in python_object_map:
            object_map.load_page(self.parse_page(page_name, python_object_map))

        return object_map

    def parse_page(self, page_name, object_map):
        page = TBBasePage(page_name)

        for element in object_map[page_name]:
            value = object_map[page_name][element]
            if element.startswith("_"):
                page.add_property(element[1:], value) # Ignore starting '-' character
            else:
                page.add_element(element, value)
        return page