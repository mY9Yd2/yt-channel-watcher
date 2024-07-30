"""
This module provides functions to generate static HTML content for a site using either Bootstrap or Tailwind CSS for styling
"""

import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from jinja2 import Environment, PackageLoader, select_autoescape

from ytcw.database.database import Database
from ytcw.site_generator.duration_formatter import duration_to_machine_readable
from ytcw.site_generator.site_data import SiteData


def generate(site_bootstrap: bool, output: Path, site_data: SiteData) -> None:
    """
    Generate static HTML content and save it to the specified output directory

    Args:
        site_bootstrap (bool): If True, use Bootstrap templates; otherwise, use Tailwind CSS templates
        output (Path): The directory where the generated HTML content will be saved
        site_data (SiteData): The data required for site generation
    """

    video_infos = Database().get_all_video_info_filter_by_age(
        site_data.cfg["site_max_video_age"]
    )
    site_data.video_infos = sorted(video_infos, key=lambda x: x.timestamp, reverse=True)
    site_data.page["generated_on"] = datetime.now(UTC)

    if site_bootstrap:
        _generate(output, site_data, _bootstrap)
    else:
        _generate(output, site_data, _tailwind)

    print(
        "Static HTML content has been successfully generated and placed in the desired output directory."
    )


def _generate(
    output: Path,
    site_data: SiteData,
    template: Callable[[Environment, Path, SiteData], None],
) -> None:
    """
    Helper function to generate HTML content using the provided template.

    Args:
        output (Path): The directory where the generated HTML content will be saved
        site_data (SiteData): The data required for site generation
        template (Callable[[Environment, Path, SiteData], None]): The template function to use for generating HTML
    """

    if output.exists():
        shutil.rmtree(output)
    output.mkdir()

    env = Environment(loader=PackageLoader(__name__), autoescape=select_autoescape())
    env.filters["duration_to_machine_readable"] = duration_to_machine_readable
    template(env, output, site_data)


def _tailwind(env: Environment, output: Path, site_data: SiteData):
    """
    Generate HTML content using Tailwind CSS for styling

    Args:
        env (Environment): The Jinja environment for template rendering
        output (Path): The directory where the generated HTML content will be saved
        site_data (SiteData): The data required for site generation
    """

    template = env.get_template("index_tailwind.html")

    output.joinpath("index.html").write_text(
        template.render(video_infos=site_data.video_infos)
    )


def _bootstrap(env: Environment, output: Path, site_data: SiteData) -> None:
    """
    Generate HTML content using Bootstrap for styling

    Args:
        env (Environment): The Jinja environment for template rendering
        output (Path): The directory where the generated HTML content will be saved
        site_data (SiteData): The data required for site generation
    """

    index_template = env.get_template("bootstrap/index.html")
    channels_template = env.get_template("bootstrap/channels.html")
    config_template = env.get_template("bootstrap/config.html")
    about_template = env.get_template("bootstrap/about.html")

    site_data.page["name"] = "index"
    output.joinpath("index.html").write_text(
        index_template.render(video_infos=site_data.video_infos, page=site_data.page)
    )

    site_data.page["name"] = "channels"
    output.joinpath("channels.html").write_text(
        channels_template.render(page=site_data.page, channels=site_data.channels)
    )

    site_data.page["name"] = "config"
    output.joinpath("config.html").write_text(
        config_template.render(page=site_data.page, cfg=site_data.cfg)
    )

    site_data.page["name"] = "about"
    output.joinpath("about.html").write_text(about_template.render(page=site_data.page))

    shutil.copyfile(
        Path(__file__).resolve().parent.joinpath("custom_headers", "_headers"),
        output.joinpath("_headers"),
    )

    shutil.copytree(
        Path(__file__).resolve().parent.joinpath("static"),
        output.joinpath("static"),
        dirs_exist_ok=True,
        copy_function=shutil.copyfile,
    )
