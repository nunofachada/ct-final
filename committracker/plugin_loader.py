from importlib import import_module
import pkgutil

def load_plugins():
    plugins = {}
    for _, name, _ in pkgutil.iter_modules(['committracker/plugins']):
        if name != '__init__':
            module = import_module(f'committracker.plugins.{name}')
            function_name = f'display_{name}'
            try:
                plugins[name] = getattr(module, function_name)
            except AttributeError as e:
                print(f"Aviso: {e}")
    return plugins
