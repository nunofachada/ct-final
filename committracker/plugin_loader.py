from importlib import metadata


def load_plugins():
    plugins = metadata.entry_points(group="commit_tracker.plugins")
    return {plugin.name: plugin.load() for plugin in plugins}
