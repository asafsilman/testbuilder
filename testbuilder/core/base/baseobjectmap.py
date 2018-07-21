"""Base Testbuilder ObjectMap class"""
from testbuilder.core.exceptions import ObjectMapException

class TBBaseObjectMap:
    def __init__(self, name):
        self.name = name
        self.current_page = None
        self.pages = {}

    def ready(self):
        """Is the objectmap ready
        
        Returns:
            bool -- If the object map has loaded
        """

        if not self.pages: # Is there atleast one page set
            return False

        # Are all pages ready
        for page in self.pages:
            if not self.pages[page].ready(): # A page is not ready
                return False
        
        return True

    def load_page(self, page, page_name=None):
        """Loads a objectmap Page to objectmap.

        If `page_name` is None the name is taken from the `page.name` attribute
        
        Arguments:
            page {TBBasePage} -- Page to add
        
        Keyword Arguments:
            page_name {str} -- The name of the page (default: {None})
        """

        if page_name is None:
            page_name = page.name
        self.pages[page_name] = page

    def get_page_names(self):
        return self.pages.keys()

    def get_current_page(self):
        return self.current_page

    def switch_page(self, page_name):
        if page_name in self.pages:
            self.current_page = self.pages[page_name]
        else:
            raise ObjectMapException(f"Page name {page_name} is not in objectmap")

    def get_element(self, element_name):
        """Gets an element from the current page in objectmap
        
        Arguments:
            element_name {str} -- The name of the element
        
        Raises:
            ObjectMapException -- Raised when current_page is not set
        
        Returns:
            Element -- The element from the objectmap
        """

        if self.current_page is None:
            raise ObjectMapException("There is no page set as current_page")
        return self.current_page.get_element(element_name)

class TBBasePage:
    def __init__(self, name, elements=None, properties=None):
        self.name = name

        self.elements = elements or {}
        self.properties = properties or {}

    def add_element(self, element_name, element_URI):
        """Add element mapping to page
        
        Arguments:
            element_name {str} -- The element name
            element_URI {str} -- Element URI, In the format `<InterfacePrefix>:<Element>`
        """

        self.elements[element_name] = element_URI

    def add_property(self, property_name, property_value):
        self.properties[property_name] = property_value

    def get_element(self, element_name):
        element_URI = self.elements.get(element_name)

        if element_URI is None:
            raise ObjectMapException(f"Unable to find element {element_name} in page {self.name}")

        return Element(element_name, element_URI)

    def ready(self):
        """Is the object map page ready
        
        Returns:
            bool -- page ready
        """

        return bool(self.elements)
    
class Element:
    def __init__(self, element_name, element_URI):
        """Loads a element from the objectmap
        
        Arguments:
            element_name {str} -- Name of the element from objectmap
            element_URI {str} -- Element URI, In the format `<InterfacePrefix>:<Element>`
        """

        self.element_name = element_name

        interface_prefix,_,element = element_URI.partition(":")
        
        self.element=element
        self.interface_prefix=interface_prefix

class TBBaseObjectMapParser:
    def parse(self, object_map_name, object_map_location) -> TBBaseObjectMap:
        """Overwrite this function"""
        raise NotImplementedError("This parser is not implemented yet")
