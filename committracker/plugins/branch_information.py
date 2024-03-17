from dash import html
from .git_statistics import extract_branches_info

def display_branch_information(repo_path):
    branches_info = extract_branches_info(repo_path)
    if "error" in branches_info:
        return html.Div(f"Error: {branches_info['error']}")

    branches_list = html.Ul([html.Li(f"{branch}: {commits} commits") for branch, commits in branches_info.items()])

    return html.Div([html.H4("Branches Information"), branches_list])
