import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class ProjectCreate(BaseModel):
    source_url: HttpUrl


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    stage: str
    status: str
    error: str | None


class ClipOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    start_seconds: float
    end_seconds: float
    reason: str | None
    video_path: str | None
    caption_srt_path: str | None


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source_url: str | None
    status: str
    created_at: datetime
    jobs: list[JobOut] = []
    clips: list[ClipOut] = []
