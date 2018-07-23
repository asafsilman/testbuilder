"""Base test class"""
import importlib

from testbuilder.core.exceptions import (
    StepException,
    ImproperlyConfigured
)
from testbuilder.core.base.basemiddleware import TBBaseMiddleware
from testbuilder.core.base.baseinterface import TBBaseInterface
from testbuilder.core.base.basestep import TBBaseStep, StepContext
from testbuilder.core.base.basefixtures import TBBaseFixture
from testbuilder.core.base.baseobjectmap import TBBaseObjectMap

MIDDLEWARE_MODE_BEFORE_STEP = 1
MIDDLEWARE_MODE_AFTER_STEP = 2

class TBBaseTest:
    """
    TestBuilder Base Test

    A TBBaseTest is container for a single testcase.
    
    A TBBaseTest is responsible for maintaing
    
    * Steps within a testcase
    * Maintaing the current step of the testcase
    * Step Middlewares
    """

    test_name=""
    
    test_iterations=0
    current_iteration=0

    first_step=None
    current_step=None

    middlewares = [] # an ordered collection of middlewares
    interfaces = {}
    object_maps = {}
    fixtures = {}

    additional_properties = {}

    def __init__(self, *args, **kwargs):
        self.test_name = kwargs.get("test_name", "")
        self.test_iterations = kwargs.get("iterations", 0)

    def load_additional_property(self, key, value):
        """Add a additional test property to testcase
        
        Arguments:
            key {str} -- Key name
            value {any} -- Value
        """

        self.additional_properties[key] = value

    def load_fixtures(self, fixture, fixture_name=None):
        """Load fixture to testcase
        
        Arguments:
            fixture {TBBaseFixture} -- Fixture instance
        
        Keyword Arguments:
            fixture_name {str} -- Optional name of fixture (default: {None})
        
        Raises:
            ImproperlyConfigured -- Raised if fixture is not of subclass TBBaseFixture
        """

        if not isinstance(fixture, TBBaseFixture):
            raise ImproperlyConfigured("Expected 'fixture' to be of class TBBaseFixture")
        
        if fixture_name is None:
            self.fixtures[fixture.fixture_name] = fixture
        else:
            self.fixtures[fixture_name] = fixture

    def load_steps(self, first_step) -> None:
        """Loads the first step for the test.
        
        Arguments:
            first_step {TBBaseStep} -- The first step in the testcase
        
        Raises:
            TypeError -- Raised if `first_step is not of type TBBaseStep`
            StepException -- Raised if the step isn't the first step
        """

        if not isinstance(first_step, TBBaseStep):
            raise TypeError("Excpected 'first_step' to by of type TBBaseStep")
        if not first_step.is_first_step():
            raise StepException("This is not the first step of the test")
        self.first_step = first_step
        self.current_step = self.first_step

    def load_middleware(self, middleware) -> None:
        """Creates and appends middleware to list of middleswares.

        Note that the order in which this function is called has a role in how the script may run.
        
        Arguments:
            middleware {TBBaseMiddleware} -- Class of TBMiddlware, **not instance of**
        """

        if not issubclass(middleware, TBBaseMiddleware):
            raise ImproperlyConfigured("Middleware is not of subclass TBBaseMiddleware")
        self.middlewares.append(middleware()) # Create and append middleware

    def load_interface(self, interface, interface_name) -> None:
        """Creates and registers a interface for the test
        
        Arguments:
            interface {TBBaseInterface} -- Class of TBBaseInterface, **not instance of**
            interface_name {String} -- Name of the interface
        """

        if not issubclass(interface, TBBaseInterface):
            raise ImproperlyConfigured("Interface is not of subclass TBBaseInterface")
        self.interfaces[interface_name] = interface() # Create and register interface

    def load_object_map(self, object_map, object_map_name) -> None:
        if not isinstance(object_map, TBBaseObjectMap):
            raise ImproperlyConfigured("Objectmap is not of instance TBBaseObjectMap")

        self.object_maps[object_map_name] = object_map

    def get_current_iteration(self) -> int:
        """Gets the current test iteration number
        
        Returns:
            int -- Current iteration
        """

        return self.current_iteration

    def run(self):
        if not self.ready():
            raise ImproperlyConfigured("Cannot start testcase because the test is not ready")
        
        step_context = StepContext(self)

        while self.current_step is not None: # End condition when no more steps
            # Step 1. Update context
            step_context.update_context(self.current_step, step_context)

            # Step 2. Run middlewares for `before_step`
            self.run_middlewares(step_context, MIDDLEWARE_MODE_BEFORE_STEP)

            # Step 3. Run Step
            self.execute_step(step_context)

            # Step 4. Run middleswares for `after_step`
            self.run_middlewares(step_context, MIDDLEWARE_MODE_AFTER_STEP)

            # Step 5. Update step
            self.current_step = step_context.next_step

    def run_middlewares(self, step_context, mode):
        if mode == MIDDLEWARE_MODE_BEFORE_STEP:
            for middleware in self.middlewares:
                middleware.before_step(step_context)
        elif mode == MIDDLEWARE_MODE_AFTER_STEP:
            for middleware in self.middlewares:
                middleware.after_step(step_context)

    def execute_step(self, step_context):
        action_interface = step_context.action_interface

        # If a step has a defined interface or not
        if action_interface is None:
            for interface in self.interfaces: # Go through each interface
                try:
                    self.interfaces[interface].dispatch(step_context)
                    break
                except ImproperlyConfigured: # Interface does not define action
                    continue
            else:
                raise ImproperlyConfigured(f"No interface found that defines {step_context.step_action}")
        else:
            if action_interface not in self.interfaces:
                raise ImproperlyConfigured(f"Interface {action_interface} is not installed")
            self.interfaces[action_interface].dispatch(step_context)

    def ready(self) -> bool:
        """Checks the tests is ready to start execution

        * Checks steps are loaded
        * Checks middlewares are not empty
        * Checks interfaces are not empty
        
        Returns:
            Boolean -- Is the test ready
        """

        ## Check step
        if self.first_step is None:
            return False

        ## Check middleware
        if self.middlewares:
            for middleware in self.middlewares: # check each middleware is ready
                if middleware.ready(): continue
                else: return False # an interface is not ready
        else: # no middlewares loaded
            return False

        ## Check interfaces
        if self.interfaces:
            for interface in self.interfaces:
                if self.interfaces[interface].ready(): # check each interface is ready
                    continue
                else:
                    return False # an interface is not ready
        else: # no middlewares loaded
            return False

        # All checks passed
        return True

    def __str__(self):
        return f"<TestCase '{self.test_name}'>"

    def __repr__(self):
        return f"<TestCase '{self.test_name}'>"