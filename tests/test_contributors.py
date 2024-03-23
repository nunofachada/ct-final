import pytest
from unittest.mock import patch, MagicMock
from collections import Counter
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'committracker')))


from committracker.plugins.contributors import extract_contributors, display_contributors


@pytest.fixture
def git_repo_mock_contributors():
    with patch('committracker.plugins.contributors.Repo') as mock_repo:
        mock_commit_1 = MagicMock()
        mock_commit_1.author.name = 'John Doe'

        mock_commit_2 = MagicMock()
        mock_commit_2.author.name = 'Jane Doe'

        mock_commit_3 = MagicMock()
        mock_commit_3.author.name = 'John Doe'

        mock_repo.return_value.iter_commits.return_value = [mock_commit_1, mock_commit_2, mock_commit_3]

        yield mock_repo


def test_extract_contributors_success(git_repo_mock_contributors):
    repo_path = 'dummy/path/to/repo'
    expected_contributors = Counter({'John Doe': 2, 'Jane Doe': 1})
    contributors = extract_contributors(repo_path)
    assert contributors == expected_contributors


def test_display_contributors_success(git_repo_mock_contributors):
    repo_path = 'dummy/path/to/repo'
    component = display_contributors(repo_path)
    assert "John Doe: 2" in str(component)
    assert "Jane Doe: 1" in str(component)
