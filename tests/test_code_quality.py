import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'committracker')))

from committracker.plugins.code_quality import run_code_quality_analysis

@pytest.fixture
def repo_setup():
    with patch('committracker.plugins.code_quality.os.path.isdir', return_value=True), \
         patch('committracker.plugins.code_quality.Repo') as mock_repo:
        mock_repo.return_value.bare = False
        yield

@pytest.fixture
def subprocess_setup():
    with patch('committracker.plugins.code_quality.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout="Flake8 output", returncode=0)
        yield mock_run

def test_run_code_quality_analysis_success(repo_setup, subprocess_setup):
    repo_path = 'dummy/path/to/repo'
    result = run_code_quality_analysis(repo_path)
    assert result == "Flake8 output"

def test_run_code_quality_analysis_no_issues_found(repo_setup, subprocess_setup):
    subprocess_setup.return_value.stdout = ""
    repo_path = 'dummy/path/to/repo'
    result = run_code_quality_analysis(repo_path)
    assert result == "No issues found by Flake8."

from committracker.plugins.code_quality import display_code_quality

def test_display_code_quality_success(repo_setup, subprocess_setup):
    repo_path = 'dummy/path/to/repo'
    component = display_code_quality(repo_path)
    assert "Code Quality Analysis (Flake8)" in str(component)
    assert "Flake8 output" in str(component)

def test_display_code_quality_no_issues_found(repo_setup, subprocess_setup):
    subprocess_setup.return_value.stdout = ""
    repo_path = 'dummy/path/to/repo'
    component = display_code_quality(repo_path)
    assert "No issues found by Flake8." in str(component)
