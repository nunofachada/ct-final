from dash import Output, Input, State, callback, html
from .utils import clone_remote_repo
from .plugin_loader import load_plugins

def register_callbacks(app):
    @app.callback(
        Output('plugin-output-area', 'children'),
        [Input('load-repo-button', 'n_clicks')],
        [State('repo-input', 'value'), State('plugin-selector', 'value')]
    )
    def update_plugin_output(n_clicks, repo_url, selected_plugins):
        if n_clicks is None or n_clicks < 1:
            return []
        if not repo_url or not selected_plugins:
            return [html.Div("Please enter a repository URL and select at least one plugin.")]

        repo_path = clone_remote_repo(repo_url)
        if repo_path is None:
            return [html.Div("Failed to clone the repository.")]

        plugins = load_plugins()
        plugin_outputs = []
        for plugin_name in selected_plugins:
            plugin_function = plugins.get(plugin_name)
            if plugin_function:
                plugin_output = plugin_function(repo_path)
                plugin_outputs.append(plugin_output)

        return plugin_outputs
