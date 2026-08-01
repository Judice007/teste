import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Clip

router = APIRouter(prefix="/clips", tags=["clips"])


@router.get("/{clip_id}/download")
def download_clip(clip_id: uuid.UUID, db: Session = Depends(get_db)):
    clip = db.get(Clip, clip_id)
    if clip is None or not clip.video_path:
        raise HTTPException(status_code=404, detail="Clip not found")
    return FileResponse(clip.video_path, media_type="video/mp4", filename=f"{clip_id}.mp4")
