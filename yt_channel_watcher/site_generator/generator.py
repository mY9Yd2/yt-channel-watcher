import os
import shutil
from datetime import datetime, timezone
from typing import Any

from database.database import Database
from jinja2 import Environment, PackageLoader, select_autoescape
from site_generator.site_data import SiteData


def generate(cfg: dict[str, Any], site_data: SiteData):
    video_infos = Database().get_all_video_info_filter_by_age(
        cfg["max-video-age-in-days"]
    )
    video_infos = sorted(video_infos, key=lambda x: x.timestamp, reverse=True)

    site_data.data["video_infos"] = video_infos
    site_data.data["page"] = {"generated_on": datetime.now(timezone.utc)}

    if cfg["experimental-use-bootstrap"]:
        _generate(site_data, _bootstrap)
    else:
        _generate(site_data, _tailwind)

    print(
        "Static HTML content has been successfully generated and placed in the 'dist/' directory."
    )


def _generate(site_data: SiteData, template):
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    os.mkdir("dist")

    env = Environment(loader=PackageLoader(__name__), autoescape=select_autoescape())
    template(env, site_data)


def _tailwind(env: Environment, site_data: SiteData):
    template = env.get_template("index_tailwind.html")

    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(template.render(video_infos=site_data.data["video_infos"]))


def _bootstrap(env: Environment, site_data: SiteData):
    index_template = env.get_template("bootstrap/index.html")
    channels_template = env.get_template("bootstrap/channels.html")
    config_template = env.get_template("bootstrap/config.html")
    about_template = env.get_template("bootstrap/about.html")

    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(
            index_template.render(
                video_infos=site_data.data["video_infos"], page=site_data.data["page"]
            )
        )

    with open("dist/channels.html", "w", encoding="utf-8") as f:
        f.write(
            channels_template.render(
                page=site_data.data["page"], channels=site_data.data["channels"]
            )
        )

    with open("dist/config.html", "w", encoding="utf-8") as f:
        f.write(
            config_template.render(
                page=site_data.data["page"], cfg=site_data.data["cfg"]
            )
        )

    with open("dist/about.html", "w", encoding="utf-8") as f:
        f.write(about_template.render(page=site_data.data["page"]))

    shutil.copytree(
        "yt_channel_watcher/site_generator/static", "dist/static", dirs_exist_ok=True
    )
