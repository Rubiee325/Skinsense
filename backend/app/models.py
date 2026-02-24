from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    lesions: Mapped[list["Lesion"]] = relationship("Lesion", back_populates="user")


class Lesion(Base):
    __tablename__ = "lesions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    body_site: Mapped[Optional[str]] = mapped_column(String(128))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship("User", back_populates="lesions")
    observations: Mapped[list["Observation"]] = relationship(
        "Observation", back_populates="lesion", cascade="all, delete-orphan"
    )


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lesion_id: Mapped[int] = mapped_column(ForeignKey("lesions.id"))
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    top_class: Mapped[Optional[str]] = mapped_column(String(64))
    top_prob: Mapped[Optional[float]] = mapped_column(Float)
    raw_metadata_json: Mapped[Optional[str]] = mapped_column(Text)

    lesion: Mapped[Lesion] = relationship("Lesion", back_populates="observations")
    images: Mapped[list["Image"]] = relationship(
        "Image", back_populates="observation", cascade="all, delete-orphan"
    )


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    observation_id: Mapped[int] = mapped_column(ForeignKey("observations.id"))
    file_path: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    observation: Mapped[Observation] = relationship("Observation", back_populates="images")