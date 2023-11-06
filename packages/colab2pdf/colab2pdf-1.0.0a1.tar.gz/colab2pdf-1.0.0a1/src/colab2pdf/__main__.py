import sys

from .cli import run

if __name__ == "__main__":
    try:
        import google.colab
    except:
        raise RuntimeError("This script must be run in Google Colaboratory.")

    sys.exit(run())
