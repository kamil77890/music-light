from flask import Flask
from flask_cors import CORS
from app.config.stałe import Parameters

from app.endpoints import (
    download,
    home,
    songs,
    file_download,
    search,
    song_id,
    song_title,
    subtitles,
    video_url,
    register,
)
from app.endpoints import cloud as cloud_router


class Application:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": "*"}})

    def set_up(self) -> None:
        Parameters()

    def register_routers(self) -> None:
        print("Registering routers...")
        self.app.register_blueprint(home.router)
        self.app.register_blueprint(songs.router)
        self.app.register_blueprint(download.router)
        self.app.register_blueprint(file_download.router)
        self.app.register_blueprint(search.router)
        self.app.register_blueprint(song_id.router)
        self.app.register_blueprint(song_title.router)
        self.app.register_blueprint(subtitles.router)
        self.app.register_blueprint(video_url.router)
        self.app.register_blueprint(register.router)
        self.app.register_blueprint(cloud_router.router)

    def run(self) -> Flask:
        self.set_up()
        self.register_routers()
        return self.app


app = Application().run()
