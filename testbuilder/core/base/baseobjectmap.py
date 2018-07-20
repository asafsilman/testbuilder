"""Base Testbuilder ObjectMap class"""
from testbuilder.core.exceptions import ObjectMapException

class TBBaseObjectMap:
    name=None
    page=None
    object_map={}

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.page = kwargs.get("page")
        self.object_map = kwargs.get("object_map", {})

    def ready(self):
        """Is the objectmap ready
        
        Returns:
            bool -- If the object map has loaded
        """

        return bool(self.object_map)

    def get_from_object_map(self, element_name):
        
        URI = self.object_map.get(element_name, None)

        if URI is None:
            raise ObjectMapException(f"Unable to find element {element_name} in project {self.name}, page {self.page}")

        interface_scheme,_,element = URI.partition(":")

        return (interface_scheme, element)
