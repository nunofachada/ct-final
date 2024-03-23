from collections import Counter

from dash import html
from git import Repo


# Extracts contributor data from a repository
def extract_contributors(repo_path):
    """
    Extracts a count of commits made by each contributor in a Git repository.

    This function iterates over all commits in the specified repository, collecting commit author names
    and counting occurrences to identify the contribution level of each participant.

    Args:
        repo_path (str): The file system path to the local Git repository.

    Returns:
        collections.Counter: A Counter object mapping contributors' names to their commit counts.
        Returns a dictionary with an 'error' key if an exception occurs, detailing the error message.
    """

    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())
        contributors = Counter(commit.author.name for commit in commits)
        return contributors
    except Exception as e:
        return {"error": str(e)}


# Display contributors in a Dash component
def display_contributors(repo_path):
    """
    Creates a Dash HTML component to display the list of contributors and their commit counts for a Git repository.

    This function fetches contributors' data using `extract_contributors` and then constructs an HTML list
    to visually represent each contributor's commitment to the repository. If an error occurs during data
    extraction, an error message is displayed within the component.

    Args:
        repo_path (str): The file system path to the local Git repository.

    Returns:
        dash.html.Div: A Dash HTML component containing the list of contributors and their commit counts.
                       If there's an error in extracting contributors' data, the component will display the error message.
    """

    contributors_data = extract_contributors(repo_path)
    if "error" in contributors_data:
        return html.Div(f"Error: {contributors_data['error']}")

    contributors_list = html.Ul(
        [
            html.Li(f"{contributor}: {count}")
            for contributor, count in contributors_data.items()
        ]
    )

    return html.Div([html.H5("Contributors"), contributors_list], className="mt-4")
