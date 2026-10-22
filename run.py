import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=int(os.environ.get("FLASK_RUN_PORT", 8000)))
