from .plugin_loader import load_plugins
from . import app


def main():

    plugins = load_plugins()
    print("Inicializando o Commit Tracker...")

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
