from git import Repo
import tempfile
import shutil
from collections import Counter


def clone_remote_repo(url):
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(url, temp_dir)
        return temp_dir
    except Exception:
        shutil.rmtree(temp_dir)
        return None


def categorize_commit_type(commit_message):
    lower_msg = commit_message.lower()
    if "fix" in lower_msg or "bug" in lower_msg:
        return "Bug Fix"
    elif "feature" in lower_msg or "add" in lower_msg:
        return "Feature"
    elif "doc" in lower_msg or "readme" in lower_msg:
        return "Documentation"
    else:
        return "Other"


def extract_git_stats(repo_path):
    """
    Extracts a comprehensive set of statistics from a Git repository located at repo_path.

    This function aggregates data on total commits, contributors, commit dates, commit types (categorized as Bug Fix, Feature, Documentation, or Other), and average lines added or deleted per commit.

    Args:
        repo_path (str): The filesystem path to the Git repository.

    Returns:
        dict: A dictionary containing various statistics about the repository, including:
              - total_commits (int): The total number of commits.
              - contributors (Counter): A collection of contributors and their commit counts.
              - commit_dates (list): A list of commit dates.
              - commit_types (Counter): The counts of different types of commits.
              - average_lines_per_commit (float): The average number of lines added or deleted per commit.
    """
    repo = Repo(repo_path)
    commits = list(repo.iter_commits())

    contributors = Counter(commit.author.name for commit in commits)
    commit_dates = [commit.committed_datetime for commit in commits]
    commit_types = Counter(categorize_commit_type(commit.message) for commit in commits)

    total_lines_added = 0
    total_lines_deleted = 0
    for commit in commits:
        stats = commit.stats.total
        total_lines_added += stats["insertions"]
        total_lines_deleted += stats["deletions"]

    average_lines_per_commit = (
        (total_lines_added + total_lines_deleted) / len(commits) if commits else 0
    )

    return {
        "total_commits": len(commits),
        "contributors": contributors,
        "commit_dates": commit_dates,
        "commit_types": commit_types,
        "average_lines_per_commit": average_lines_per_commit,
    }


def extract_branches_info_new(repo_path):
    """
    Extracts information about each branch in a Git repository, including the total number of commits per branch.

    Args:
        repo_path (str): The filesystem path to the Git repository.

    Returns:
        dict: A dictionary where keys are branch names and values are the total number of commits in each branch.
    """
    repo = Repo(repo_path)
    branches_info = {}
    for branch in repo.branches:
        commits_count = sum(1 for _ in repo.iter_commits(branch))
        branches_info[branch.name] = commits_count
    return branches_info
