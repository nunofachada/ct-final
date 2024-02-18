import dash_bootstrap_components as dbc
from dash import html, dcc


def create_layout(app):
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1("Commit Tracker 📊", className="text-center mb-4"), width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.H5(
                        "Explore Git Repositories with Ease: In-Depth Analytics and Visual Insights",
                        className="text-center mb-4",
                    ),
                    width=12,
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Label(
                            "Enter a Git repository path or URL and click Submit",
                            className="align-self-center",
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="input-repo",
                            type="text",
                            placeholder="Git repository local path or URL...",
                            style={"width": "100%", "border-radius": "5px"},
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        html.Button(
                            "Submit",
                            id="submit-val",
                            n_clicks=0,
                            className="btn btn-primary",
                            style={"border-radius": "5px"},
                        ),
                        width=3,
                        className="align-self-center",
                    ),
                ],
                align="center",
                className="my-2",
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[
                            dcc.Graph(id="graph-commits-over-time"),
                            html.Div(id="stats-output"),
                        ],
                    ),
                    width=12,
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Div("Commit Tracker 2024", className="text-center mt-4"),
                    width=12,
                )
            ),
        ],
        fluid=False,
        className="py-3 px-5",
    )
