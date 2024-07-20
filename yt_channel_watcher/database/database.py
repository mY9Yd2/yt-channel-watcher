from database.base import Base
from database.video_info import VideoInfo
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.__engine = create_engine(
            "sqlite+pysqlite:///yt_channel_watcher.sqlite3", echo=False
        )
        Base.metadata.create_all(self.__engine)

    def get_video_info_by_display_id(self, display_id: str):
        with Session(self.__engine) as session:
            stmt = select(VideoInfo).where(VideoInfo.display_id == display_id)
            return session.scalar(stmt)

    def insert_video_info_bulk(self, video_infos: list[VideoInfo]):
        with Session(self.__engine) as session:
            session.add_all(video_infos)
            session.commit()

    def get_all_video_info(self):
        with Session(self.__engine) as session:
            stmt = select(VideoInfo)
            return session.scalars(stmt).all()
