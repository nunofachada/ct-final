import os
import sys
from collections import Counter
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "committracker"))
)

# Importing functions to be tested from the contributors module.
from committracker.plugins.contributors import (
    display_contributors,
    extract_contributors,
)


@pytest.fixture
def git_repo_mock_contributors():
    # Mocking the Repo object to simulate a repository with commits from different authors.
    with patch("committracker.plugins.contributors.Repo") as mock_repo:
        mock_commit_1 = MagicMock()
        mock_commit_1.author.name = "John Doe"

        mock_commit_2 = MagicMock()
        mock_commit_2.author.name = "Jane Doe"

        mock_commit_3 = MagicMock()
        mock_commit_3.author.name = "John Doe"

        # Simulating the return value of iter_commits with a predefined list of commits.
        mock_repo.return_value.iter_commits.return_value = [
            mock_commit_1,
            mock_commit_2,
            mock_commit_3,
        ]

        yield mock_repo


def test_extract_contributors_success(git_repo_mock_contributors):
    # Testing the successful extraction of contributor information from the mock repository.
    repo_path = "dummy/path/to/repo"
    expected_contributors = Counter({"John Doe": 2, "Jane Doe": 1})
    contributors = extract_contributors(repo_path)
    assert contributors == expected_contributors


def test_display_contributors_success(git_repo_mock_contributors):
    # Verifying the successful display of contributors in a Dash component.
    repo_path = "dummy/path/to/repo"
    component = display_contributors(repo_path)
    # Ensuring the component contains the correct contribution counts for each contributor.
    assert "John Doe: 2" in str(component)
    assert "Jane Doe: 1" in str(component)
