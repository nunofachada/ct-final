# Available Functions and Documentation

Commit Tracker provides a set of functionalities to analyze Git repositories, offering insights through statistics and visualizations. This document details the available functions and their usage.

## extract_contributors

Extracts contributor data from a repository, showing the number of commits made by each contributor.

### Parameters

- repo_path: String. The path to the local Git repository.

### Returns

- Counter: A counter object where keys are author names and values are the number of commits made by each author.

### Usage

from committracker.plugins.contributors import extract_contributors

contributors = extract_contributors("/path/to/repo")

## display_contributors

Displays contributor data in a Dash component.

### Parameters

- repo_path: String. The path to the local Git repository.

### Returns

- Dash component containing the list of contributors and their commit counts.

### Usage

from committracker.plugins.contributors import display_contributors

component = display_contributors("/path/to/repo")

## extract_git_stats

Extracts various statistics from a local Git repository, such as total commits, commit dates, and average lines changed per commit.

### Parameters

- repo_path: String. The path to the local Git repository.

### Returns

- Dictionary: A dictionary containing various statistics about the repository.

### Usage

from committracker.plugins.git_statistics import extract_git_stats

stats = extract_git_stats("/path/to/repo")

## display_git_statistics

Displays Git statistics in a Dash component.

### Parameters

- repo_path: String. The path to the local Git repository.

### Returns

- Dash component containing the Git statistics visualization.

### Usage

from committracker.plugins.git_statistics import display_git_statistics

component = display_git_statistics("/path/to/repo")

## display_commit_graph

Generates and displays a graph of commits over time.

### Parameters

- repo_path: String. The path to the local Git repository.

### Returns

- Dash component containing the commit graph.

### Usage

from committracker.plugins.commit_graph import display_commit_graph

component = display_commit_graph("/path/to/repo")

For more detailed examples and additional functionalities, please refer to the User Guide and API Reference sections.
