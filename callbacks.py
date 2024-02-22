from dash import Input, Output, State, html, dcc
import plotly.graph_objs as go
import pandas as pd
import shutil
from importlib.metadata import entry_points
import os


def load_plugins():
    plugins = {
        ep.name: ep.load() for ep in entry_points(group="commit_tracker.plugins")
    }
    return plugins


plugins = load_plugins()


def register_callbacks(app):
    @app.callback(
        [
            Output("graph-commits-over-time", "figure"),
            Output("stats-output", "children"),
        ],
        [
            Input("submit-val", "n_clicks"),
        ],
        [
            State("input-repo", "value"),
        ],
    )
    def update_output(n_clicks, value):
        if n_clicks is None or not value:
            return go.Figure(), "Please enter a repository URL."

        repo_path = value
        is_cloned = False

        try:
            if not os.path.exists(value):
                print(f"Attempting to clone repository: {value}")
                repo_path = plugins["clone_remote_repo"](value)
                if not repo_path:
                    raise Exception("Failed to clone repository.")
                is_cloned = True

            print(f"Extracting git stats for: {repo_path}")
            stats = plugins["extract_git_stats"](repo_path)
        except Exception as e:
            print(f"Error during repository processing: {e}")
            return go.Figure(), str(e)
        finally:
            if is_cloned:
                print(f"Removing cloned repository: {repo_path}")
                shutil.rmtree(repo_path, ignore_errors=True)

        # datas
        df = pd.DataFrame({"Commit Date": stats["commit_dates"]})
        df["Commit Date"] = pd.to_datetime(df["Commit Date"], utc=True).dt.tz_localize(
            None
        )
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
        [
            Input("submit-val", "n_clicks"),
        ],
        [
            State("input-repo", "value"),
        ],
    )
    def update_branches_info(n_clicks, value):
        if n_clicks is None or not value:
            return "Please enter a repository URL."

        try:
            repo_path = value
            if not os.path.exists(value):
                print(f"Attempting to clone repository for branch info: {value}")
                repo_path = plugins["clone_remote_repo"](value)
                if not repo_path:
                    raise Exception("Failed to clone repository for branches info.")

            print(f"Extracting branches info for: {repo_path}")
            branches_info = plugins["extract_branches_info_new"](repo_path)
        except Exception as e:
            print(f"Error during branches info extraction: {e}")
            return f"Error: {e}"

        children = [html.H4("Branches Information:")]
        for branch, commits in branches_info.items():
            children.append(html.P(f"{branch}: {commits} commits"))
        return children
