import os
import shutil

from database.video_info import VideoInfo
from jinja2 import Environment, PackageLoader, select_autoescape


def generate(video_infos: list[VideoInfo]):
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    os.mkdir("dist")

    env = Environment(loader=PackageLoader(__name__), autoescape=select_autoescape())
    template = env.get_template("base.html")

    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(template.render(video_infos=video_infos))
