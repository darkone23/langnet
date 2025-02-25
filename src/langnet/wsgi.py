from langnet.flask_app.core import create_flask_app

app = create_flask_app()

if __name__ == "__main__":
    app.run()
