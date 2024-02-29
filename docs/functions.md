# Available Functions and Documentation

Commit Tracker provides a set of functionalities to analyze Git repositories, offering insights through statistics and visualizations. This document details the available functions and their usage.

## clone_remote_repo

Clones a remote Git repository to a temporary directory for analysis.

### Parameters

- url: String. The URL of the Git repository to clone.

### Returns

- Path to the temporary directory containing the cloned repository.

### Usage

from committracker.git_stats import clone_remote_repo

repo_path = clone_remote_repo("https://github.com/user/repo.git")

## categorize_commit_type

Categorizes a commit message into predefined types such as Bug Fix, Feature, Documentation, or Other.

### Parameters

- commit_message: String. The commit message to categorize.

### Returns

- String. The category of the commit.

### Usage

from committracker.git_stats import categorize_commit_type

commit_type = categorize_commit_type("fix a critical bug")

## extract_git_stats

Extracts statistics from a local Git repository, including total commits, contributions by author, commit dates, and types of commits based on their messages.

### Parameters

- repo_path: String. The path to the local Git repository.

### Returns

- Dictionary. A dictionary containing various statistics about the repository.

### Usage

from committracker.git_stats import extract_git_stats

stats = extract_git_stats("/path/to/repo")

## extract_branches_info_new

Extracts information about the branches in a Git repository, including the number of commits per branch.

### Parameters

- repo_path: String. The path to the local Git repository.

### Returns

- Dictionary. A dictionary where keys are branch names and values are the number of commits on each branch.

### Usage

from committracker.git_stats import extract_branches_info_new

branches_info = extract_branches_info_new("/path/to/repo")

For more detailed examples and additional functionalities, please refer to the User Guide and API Reference sections.
