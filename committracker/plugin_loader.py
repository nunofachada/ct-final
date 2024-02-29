from importlib import metadata


def load_plugins():
    plugins = metadata.entry_points(group="committracker.plugins")
    return {plugin.name: plugin.load() for plugin in plugins}
