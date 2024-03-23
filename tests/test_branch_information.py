# tests/test_branch_information.py
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Adiciona o diretório 'committracker' ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'committracker')))

from committracker.plugins.branch_information import extract_branches_info


@pytest.fixture
def git_branches_mock():
    with patch('committracker.plugins.branch_information.Repo') as mock_repo:
        # Simulando branches e a contagem de commits de forma adequada
        mock_main_branch = MagicMock()
        mock_develop_branch = MagicMock()

        # Configurando os nomes das branches diretamente
        mock_main_branch.name = 'main'
        mock_develop_branch.name = 'develop'

        # Simulando a contagem de commits para cada branch
        # O 'range' deve ser convertido em uma lista para simular os commits
        mock_repo.return_value.iter_commits.side_effect = [
            list(range(10)),  # Para 'main'
            list(range(5))  # Para 'develop'
        ]

        mock_repo.return_value.branches = [mock_main_branch, mock_develop_branch]

        yield mock_repo


def test_extract_branches_info_success(git_branches_mock):
    expected_output = {'main': 10, 'develop': 5}
    repo_path = 'dummy/path/to/repo'
    branches_info = extract_branches_info(repo_path)
    assert branches_info == expected_output
