"""
The main console application
"""

from pathlib import Path

import typer
from typing_extensions import Annotated

from ytcw.database.database import Database
from ytcw.load_channels.load import load
from ytcw.site_generator.generator import generate
from ytcw.site_generator.site_data import SiteData
from ytcw.video_downloader.downloader import Downloader


class Application:
    @staticmethod
    def run(
        database: Annotated[
            Path,
            typer.Argument(
                help="Path to SQLite file",
                show_default=False,
                exists=False,
                file_okay=True,
                dir_okay=False,
                writable=True,
                readable=True,
                resolve_path=True,
            ),
        ],
        channels: Annotated[
            Path,
            typer.Argument(
                help="Path to the channels file (YAML or JSON)",
                show_default=False,
                exists=True,
                file_okay=True,
                dir_okay=False,
                writable=False,
                readable=True,
                resolve_path=True,
            ),
        ],
        output: Annotated[
            Path,
            typer.Argument(
                help="Path to the output directory where the generated page will be saved",
                show_default=False,
                exists=False,
                file_okay=False,
                dir_okay=True,
                writable=True,
                readable=False,
                resolve_path=True,
            ),
        ],
        download: Annotated[
            bool, typer.Option(help="Launch yt-dlp to download new information")
        ] = True,
        generate_site: Annotated[
            bool,
            typer.Option(help="Generate a static web page from the video information"),
        ] = True,
        check_thumbnail: Annotated[
            bool,
            typer.Option(help="Check if thumbnail exists"),
        ] = True,
        ydl_max_downloads: Annotated[
            int, typer.Option(help="Maximum number of downloads per tab", min=1)
        ] = 20,
        ydl_max_video_age: Annotated[
            int, typer.Option(help="Maximum age of the video in days", min=1)
        ] = 7,
        site_bootstrap: Annotated[
            bool, typer.Option(help="Use Bootstrap in the generated website")
        ] = True,
        site_max_video_age: Annotated[
            int,
            typer.Option(
                help="Maximum age of the video in days that will be displayed on the site",
                min=1,
            ),
        ] = 7,
    ) -> None:
        """
        App main entry point
        """

        try:
            Database(database)

            _channels = load(channels)

            if download:
                downloader = Downloader(
                    _channels, ydl_max_downloads, ydl_max_video_age, check_thumbnail
                )
                downloader.start()

            if generate_site:
                site_data = SiteData()
                site_data.cfg["ydl_max_downloads"] = ydl_max_downloads
                site_data.cfg["ydl_max_video_age"] = ydl_max_video_age
                site_data.cfg["site_max_video_age"] = site_max_video_age
                site_data.channels = _channels

                generate(site_bootstrap, output, site_data)
        except KeyboardInterrupt:
            raise typer.Abort()


def main():
    typer.run(Application.run)


if __name__ == "__main__":
    main()
