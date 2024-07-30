"""
Defines the models for the application database
"""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class VideoInfo(Base):
    """
    Represents a video information

    Attributes:
        id (int): Unique identifier for the video information
        created_at (datetime): Datetime when the video information was added to the database
        uploader_id (str): Channel 'handle', unique and short channel identifier
        channel_id (str): Channel unique identifier (long, random)
        channel (str): Channel name
        timestamp (datetime): Datetime when the video is released
        fulltitle (str): Video title
        display_id (str): Unique and short video identifier
        webpage_url (str): Url to the video
        thumbnail (str): Url to the thumbnail
        duration (int): Video duration in seconds
        duration_string (str): Video duration, formatted
        language (str): Language of the video/targeted audience
    """

    __tablename__ = "video_info"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())

    uploader_id: Mapped[str]
    channel_id: Mapped[str]
    channel: Mapped[str]
    timestamp: Mapped[datetime]
    fulltitle: Mapped[str]
    display_id: Mapped[str] = mapped_column(unique=True)
    webpage_url: Mapped[str]
    thumbnail: Mapped[str]
    duration: Mapped[int]
    duration_string: Mapped[str]
    language: Mapped[str | None]

    def __repr__(self) -> str:
        return (
            f"VideoInfo(id={self.id!r}, uploader_id={self.uploader_id!r}, channel_id={self.channel_id!r}, "
            f"channel={self.channel!r}, timestamp={self.timestamp!r}, fulltitle={self.fulltitle!r}, "
            f"display_id={self.display_id!r}, webpage_url={self.webpage_url!r}, thumbnail={self.thumbnail!r}, "
            f"duration={self.duration!r}, duration_string={self.duration_string!r}, created_at={self.created_at!r}), "
            f"language={self.language}"
        )
