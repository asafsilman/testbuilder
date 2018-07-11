"""
Invoke testbuilder commandline utility.

Example: python -m testbuilder <command>
"""
from testbuilder.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
