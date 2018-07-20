import importlib

def load_module(module):
    module_path, _, class_name = module.rpartition(".")
    module = importlib.import_module(module_path)

    return getattr(module, class_name, None)