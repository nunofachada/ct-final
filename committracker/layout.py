from dash import html, dcc
import dash_bootstrap_components as dbc
from .plugin_loader import load_plugins

def create_layout(app):
    plugins = load_plugins()
    plugin_options = [
        {'label': plugin.replace('_', ' ').title(), 'value': plugin}
        for plugin in plugins.keys()
    ]

    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="https://assets.streamlinehq.com/image/private/w_200,h_200,ar_1/f_auto/v1/icons/freebies-freemojis/objects/objects/bar-chart-f5c5npy7d6s2nmc8ttmgxd.png?_a=DAJFJtWIZAAC", height="30px", className="me-3")),
                        dbc.Col(dbc.NavbarBrand("Commit Tracker", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
            ],
            fluid=True,
        ),
        color="primary",
        dark=True,
        className="mb-3",
    )

    plugin_selector = dcc.Dropdown(
        id='plugin-selector',
        options=plugin_options,
        multi=True,
        placeholder='Select plugins...',
        className='mb-2'
    )

    repo_input = dbc.Input(
        id='repo-input',
        type='text',
        placeholder='Enter repository URL or path...',
        className='mb-2'
    )

    submit_button = dbc.Button(
        'Load Repository',
        id='load-repo-button',
        color="primary",
        className='mb-4'
    )

    plugin_output_area = html.Div(id='plugin-output-area')

    layout = html.Div([
        navbar,
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(plugin_selector, width=12, lg=8),
                    justify="center",
                ),
                dbc.Row(
                    dbc.Col(repo_input, width=12, lg=8),
                    justify="center",
                ),
                dbc.Row(
                    dbc.Col(submit_button, width=12, lg=8),
                    justify="center",
                ),
                dbc.Row(
                    dbc.Col(plugin_output_area, md=8),
                    justify="center",
                ),
            ],
            fluid=True,
        )
    ])

    return layout