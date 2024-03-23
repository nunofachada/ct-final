import pytest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'committracker')))

from committracker.plugins.git_statistics import extract_git_stats, display_git_statistics


@pytest.fixture
def git_repo_mock():
    # Mock the Repo object to simulate a repository with commits, each having a specific number of insertions and deletions.
    with patch('committracker.plugins.git_statistics.Repo') as mock_repo:
        mock_commit = MagicMock()
        # Simulate commit dates and statistics for line changes.
        mock_commit.committed_datetime = datetime.now() - timedelta(days=1)
        mock_commit.stats.total = {"insertions": 10, "deletions": 5}

        mock_commit_2 = MagicMock()
        mock_commit_2.committed_datetime = datetime.now() - timedelta(days=2)
        mock_commit_2.stats.total = {"insertions": 20, "deletions": 10}

        # Return a list of simulated commits from iter_commits.
        mock_repo.return_value.iter_commits.return_value = [mock_commit, mock_commit_2]
        yield mock_repo


def test_extract_git_stats_success(git_repo_mock):
    # Test the successful extraction of git statistics, verifying the total commits, commit dates, and average lines changed per commit.
    repo_path = 'dummy/path/to/repo'
    stats = extract_git_stats(repo_path)
    assert stats["total_commits"] == 2
    assert len(stats["commit_dates"]) == 2
    assert stats["average_lines_per_commit"] == 22.5


def test_display_git_statistics_success(git_repo_mock):
    # Verify the display of git statistics in a Dash component, checking for the presence of total commits and average lines changed per commit.
    repo_path = 'dummy/path/to/repo'
    component = display_git_statistics(repo_path)
    assert "Total Commits: 2" in str(component)
    assert "Average Lines per Commit: 22.50" in str(component)
