"""
Contains the database connection and related functions
"""

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Sequence

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from ytcw.database.models import Base, VideoInfo


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """
    Database access (singleton)
    """

    def __init__(self, file_path: Path) -> None:
        """
        Initialise the database

        Args:
            file_path (Path): Path to the database file
        """

        self.__engine = create_engine(f"sqlite+pysqlite:///{file_path}", echo=False)
        Base.metadata.create_all(self.__engine)

    def get_video_info_by_display_id(self, display_id: str) -> VideoInfo | None:
        """
        Query the video information by display id

        Args:
            display_id (str): Display id of the video information

        Returns:
            Returns video information if found, None otherwise
        """

        with Session(self.__engine) as session:
            stmt = select(VideoInfo).where(VideoInfo.display_id == display_id)
            return session.scalar(stmt)

    def insert_video_info_bulk(self, video_infos: list[VideoInfo]) -> None:
        """
        Insert a list of video information to the database

        Args:
            video_infos (list[VideoInfo]): List of video information
        """

        with Session(self.__engine) as session:
            session.add_all(video_infos)
            session.commit()

    def get_all_video_info_filter_by_age(self, max_age: int) -> Sequence[VideoInfo]:
        """
        Get all video information, filtered by the maximum age of the video

        Args:
            max_age (int): Maximum age of the video

        Returns:
            Returns a list of video information
        """

        cutoff_time = datetime.now(UTC) - timedelta(days=max_age)

        with Session(self.__engine) as session:
            stmt = select(VideoInfo).where(VideoInfo.timestamp >= cutoff_time)
            return session.scalars(stmt).all()
