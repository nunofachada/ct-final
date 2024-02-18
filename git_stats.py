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
    repo = Repo(repo_path)
    branches_info = {}
    for branch in repo.branches:
        commits_count = sum(1 for _ in repo.iter_commits(branch))
        branches_info[branch.name] = commits_count
    return branches_info
