from dash import Input, Output, State
import plotly.graph_objs as go
from git_stats import (
    extract_git_stats,
    clone_remote_repo,
    extract_branches_info_new,
)  # Importando com o novo nome
import pandas as pd
import os
import shutil
from dash import html
from git import Repo


def register_callbacks(app):
    @app.callback(
        [
            Output("graph-commits-over-time", "figure"),
            Output("stats-output", "children"),
        ],
        [Input("submit-val", "n_clicks")],
        [State("input-repo", "value")],
    )
    def update_output(n_clicks, value):
        if n_clicks > 0 and not value:
            error_message = html.Div(
                "Please enter a repository path or URL before submitting.",
                style={
                    "color": "white",
                    "backgroundColor": "red",
                    "padding": "10px",
                    "border-radius": "5px",
                },
            )
            return go.Figure(), error_message

        if not value:
            return go.Figure(), None

        repo_path = value
        is_cloned = False
        if not os.path.exists(value):
            repo_path = clone_remote_repo(value)
            if not repo_path:
                return go.Figure(), "Failed to clone repository."
            is_cloned = True

        stats = extract_git_stats(repo_path)

        if is_cloned:
            shutil.rmtree(repo_path, onerror=lambda func, path, exc_info: None)

        if "error" in stats:
            return go.Figure(), stats["error"]

        # Commits Over Time Graph
        df = pd.DataFrame({"Commit Date": stats["commit_dates"]})
        df["Commit Date"] = pd.to_datetime(df["Commit Date"], utc=True)
        df_group = (
            df.groupby(df["Commit Date"].dt.date).size().reset_index(name="Commits")
        )
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df_group["Commit Date"],
                    y=df_group["Commits"],
                    mode="lines+markers",
                )
            ]
        )
        fig.update_layout(
            title="Commits Over Time",
            xaxis_title="Date",
            yaxis_title="Number of Commits",
        )

        # Estatísticas detalhadas
        stats_layout = html.Div(
            [
                html.H4("Detailed Statistics:"),
                html.P(f"Total Commits: {stats['total_commits']}"),
                html.P(
                    f"Average Lines per Commit: {stats['average_lines_per_commit']:.2f}"
                ),
                html.H5("Commits by Contributor:"),
                html.Ul(
                    [
                        html.Li(f"{contributor}: {commits}")
                        for contributor, commits in stats["contributors"].items()
                    ]
                ),
                html.H5("Commit Types:"),
                html.Ul(
                    [
                        html.Li(f"{commit_type}: {count}")
                        for commit_type, count in stats["commit_types"].items()
                    ]
                ),
            ]
        )

        return fig, stats_layout

    @app.callback(
        Output("branches-info", "children"),
        [Input("submit-val", "n_clicks")],
        [State("input-repo", "value")],
    )
    def update_branches_info(n_clicks, value):
        if n_clicks > 0:
            repo_path = value
            if not os.path.exists(repo_path):
                repo_path = clone_remote_repo(value)
            branches_info = extract_branches_info_new(repo_path)  # Renomeando aqui
            children = [html.H4("Branches Information:")]
            for branch, commits in branches_info.items():
                children.append(html.P(f"{branch}: {commits} commits"))
            return children
        return []
