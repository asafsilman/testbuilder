from testbuilder.core.base.baseinterface import TBBaseInterface, action_word

import unittest

@action_word
def sample_action(self, step_context):
    pass

class TestTBBaseInterface(unittest.TestCase):
    def setUp(self):
        self.test_interface = TBBaseInterface()
        setattr(self.test_interface, "sample_action", sample_action)


    def test_get_list_of_action_words(self):
        interface_action_words = self.test_interface.get_list_of_action_words()

        self.assertEqual(len(interface_action_words), 1)
        self.assertIn("sample_action", interface_action_words)
