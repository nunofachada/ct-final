from dash import html, dcc
import dash_bootstrap_components as dbc
from .plugin_loader import load_plugins

def create_layout(app):
    plugins = load_plugins()
    plugin_options = [{'label': plugin, 'value': plugin} for plugin in plugins.keys()]

    navbar = dbc.NavbarSimple(brand="Commit Tracker", brand_href="#", color="primary", dark=True)
    plugin_selector = dcc.Dropdown(id='plugin-selector', options=plugin_options, multi=True, placeholder='Select plugins...')
    repo_input = dbc.Input(id='repo-input', type='text', placeholder='Enter repository URL or path...')
    submit_button = dbc.Button('Load Repository', id='load-repo-button', n_clicks=0, className='ms-2')
    plugin_output_area = html.Div(id='plugin-output-area')

    content = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(plugin_selector, width=10, className="mb-2"),
                    dbc.Col(submit_button, width=2, className="mb-2")
                ],
                className="mb-2"
            ),
            dbc.Row(
                dbc.Col(repo_input, width=12, className="mb-2")
            ),
            dbc.Row(
                dbc.Col(plugin_output_area, width=12)
            )
        ],
        fluid=True,
        className="py-3 px-5"
    )

    return html.Div([navbar, content])
