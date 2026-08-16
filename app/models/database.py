import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/jobs.db")

if DATABASE_URL.startswith("sqlite:///"):
    os.makedirs("data", exist_ok=True)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), default="")
    company: Mapped[str] = mapped_column(String(300), default="")
    location: Mapped[str] = mapped_column(String(300), default="")
    url: Mapped[str] = mapped_column(String(1500), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    match_score: Mapped[int] = mapped_column(Integer, default=0)
    skills_score: Mapped[int] = mapped_column(Integer, default=0)
    experience_score: Mapped[int] = mapped_column(Integer, default=0)
    role_score: Mapped[int] = mapped_column(Integer, default=0)
    location_score: Mapped[int] = mapped_column(Integer, default=0)
    matched_skills: Mapped[str] = mapped_column(Text, default="")
    missing_skills: Mapped[str] = mapped_column(Text, default="")
    recommendation: Mapped[str] = mapped_column(String(100), default="")
    reason: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(50), default="NEW", index=True)
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
