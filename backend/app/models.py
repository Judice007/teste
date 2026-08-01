import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base


class JobStage(str, enum.Enum):
    fetch_source = "fetch_source"
    transcribe = "transcribe"
    score_highlights = "score_highlights"
    render_clips = "render_clips"
    burn_captions = "burn_captions"
    done = "done"


class JobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_url = Column(String, nullable=True)
    source_file_path = Column(String, nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship(
        "Job", back_populates="project", cascade="all, delete-orphan",
        order_by="Job.created_at",
    )
    clips = relationship(
        "Clip", back_populates="project", cascade="all, delete-orphan",
        order_by="Clip.start_seconds",
    )


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    stage = Column(Enum(JobStage), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.pending, nullable=False)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="jobs")


class Clip(Base):
    __tablename__ = "clips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    start_seconds = Column(Float, nullable=False)
    end_seconds = Column(Float, nullable=False)
    reason = Column(Text, nullable=True)
    video_path = Column(String, nullable=True)
    caption_srt_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="clips")
