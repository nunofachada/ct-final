from committracker.plugin_loader import load_plugins
from committracker import app


def main():

    plugins = load_plugins()
    print("Initializing Commit Tracker...")

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
