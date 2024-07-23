from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from ytcw.database.base import Base
from ytcw.database.video_info import VideoInfo


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self, file_path: Path) -> None:
        self.__engine = create_engine(f"sqlite+pysqlite:///{file_path}", echo=False)
        Base.metadata.create_all(self.__engine)

    def get_video_info_by_display_id(self, display_id: str):
        with Session(self.__engine) as session:
            stmt = select(VideoInfo).where(VideoInfo.display_id == display_id)
            return session.scalar(stmt)

    def insert_video_info_bulk(self, video_infos: list[VideoInfo]):
        with Session(self.__engine) as session:
            session.add_all(video_infos)
            session.commit()

    def get_all_video_info_filter_by_age(self, max_age: int):
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=max_age)

        with Session(self.__engine) as session:
            stmt = select(VideoInfo).where(VideoInfo.timestamp >= cutoff_time)
            return session.scalars(stmt).all()
