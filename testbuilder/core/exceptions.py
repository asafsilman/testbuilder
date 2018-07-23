"""Testbuilder exceptions"""

class StepException(Exception):
    """There is an issue with the current step"""
    pass

class ImproperlyConfigured(Exception):
    """There is an issue with the configuration"""
    pass

class ObjectMapException(Exception):
    """There is an issue related to the object map"""
    pass
