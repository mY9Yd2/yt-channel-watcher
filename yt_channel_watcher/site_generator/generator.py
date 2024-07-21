import os
import shutil
from typing import Any

from database.database import Database
from database.video_info import VideoInfo
from jinja2 import Environment, PackageLoader, select_autoescape


def generate(cfg: dict[str, Any]):
    video_infos = Database().get_all_video_info_filter_by_age(
        cfg["max-video-age-in-days"]
    )
    video_infos = sorted(video_infos, key=lambda x: x.timestamp, reverse=True)

    if cfg["experimental-use-bootstrap"]:
        _generate(video_infos, _bootstrap)
    else:
        _generate(video_infos, _tailwind)

    print(
        "Static HTML content has been successfully generated and placed in the 'dist/' directory."
    )


def _generate(video_infos: list[VideoInfo], template):
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    os.mkdir("dist")

    env = Environment(loader=PackageLoader(__name__), autoescape=select_autoescape())
    template(env, video_infos)


def _tailwind(env: Environment, video_infos: list[VideoInfo]):
    template = env.get_template("base.html")

    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(template.render(video_infos=video_infos))


def _bootstrap(env: Environment, video_infos: list[VideoInfo]):
    template = env.get_template("base_bootstrap.html")

    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(template.render(video_infos=video_infos))

    shutil.copytree(
        "yt_channel_watcher/site_generator/static", "dist/static", dirs_exist_ok=True
    )
