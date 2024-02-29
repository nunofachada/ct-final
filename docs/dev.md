# For Developers

If you are interested in contributing to the Commit Tracker project or wish to add new features, please follow the steps below to set up your development environment.

## Installing for Development

To set up your development environment for Commit Tracker, execute the following commands. This will install all necessary development dependencies.

git clone https://github.com/andrecosta99/ct-final.git
cd ct-final
python -m venv env
# On Unix or MacOS
source env/bin/activate
# On Windows
.\env\Scripts\activate
pip install -e .
pre-commit install

## Running Tests

Commit Tracker includes a suite of tests to ensure the quality and functionality of the code. To run these tests, use the following command:

pytest

To generate a coverage report and see which parts of your code are covered by tests, use:

pytest --cov=committracker --cov-report=html

This will create a coverage report in the `htmlcov` directory, which you can open with a web browser.
