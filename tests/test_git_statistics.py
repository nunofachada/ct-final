import pytest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'committracker')))

from committracker.plugins.git_statistics import extract_git_stats, display_git_statistics


@pytest.fixture
def git_repo_mock():
    with patch('committracker.plugins.git_statistics.Repo') as mock_repo:
        mock_commit = MagicMock()
        mock_commit.committed_datetime = datetime.now() - timedelta(days=1)
        mock_commit.stats.total = {"insertions": 10, "deletions": 5}
        mock_commit_2 = MagicMock()
        mock_commit_2.committed_datetime = datetime.now() - timedelta(days=2)
        mock_commit_2.stats.total = {"insertions": 20, "deletions": 10}

        mock_repo.return_value.iter_commits.return_value = [mock_commit, mock_commit_2]
        yield mock_repo


def test_extract_git_stats_success(git_repo_mock):
    repo_path = 'dummy/path/to/repo'
    stats = extract_git_stats(repo_path)
    assert stats["total_commits"] == 2
    assert len(stats["commit_dates"]) == 2
    assert stats["average_lines_per_commit"] == 22.5


def test_display_git_statistics_success(git_repo_mock):
    repo_path = 'dummy/path/to/repo'
    component = display_git_statistics(repo_path)
    assert "Total Commits: 2" in str(component)
    assert "Average Lines per Commit: 22.50" in str(component)
