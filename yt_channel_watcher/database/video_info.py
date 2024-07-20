from datetime import datetime

from database.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class VideoInfo(Base):
    __tablename__ = "video_info"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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

    def __repr__(self) -> str:
        return (
            f"VideoInfo(id={self.id!r}, uploader_id={self.uploader_id!r}, channel_id={self.channel_id!r}, "
            f"channel={self.channel!r}, timestamp={self.timestamp!r}, fulltitle={self.fulltitle!r}, "
            f"display_id={self.display_id!r}, webpage_url={self.webpage_url!r}, thumbnail={self.thumbnail!r}, "
            f"duration={self.duration!r}, duration_string={self.duration_string!r})"
        )
