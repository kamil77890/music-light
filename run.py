from app.app import Application

flask_app = Application().run()

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8001)
