import os
import sys

import hydra
from database.database import Database
from load_channels.load import load
from omegaconf import DictConfig
from site_generator.generator import bootstrap, generate, tailwind
from video_downloader.downloader import Downloader


class Application:
    @staticmethod
    @hydra.main(version_base=None, config_path="configs", config_name="config")
    def run(cfg: DictConfig) -> None:
        Database()

        channels = load(cfg["ydl"]["channels-file"])

        if not cfg["app"]["disable-ydl"]:
            downloader = Downloader(channels, cfg["ydl"])
            downloader.start()

        if not cfg["app"]["disable-html"]:
            video_infos = Database().get_all_video_info()
            video_infos = sorted(video_infos, key=lambda x: x.timestamp, reverse=True)

            if cfg["app"]["experimental-use-bootstrap"]:
                generate(video_infos, bootstrap)
            else:
                generate(video_infos, tailwind)


if __name__ == "__main__":
    try:
        Application.run()
    except KeyboardInterrupt:
        print("\nInterrupted")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
