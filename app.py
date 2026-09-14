import os

from backend.server import run


if __name__ == "__main__":
    run(port=int(os.getenv("PORT", "8000")))
