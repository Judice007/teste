import os
import uuid

from app.celery_app import celery
from app.config import settings
from app.db import SessionLocal
from app.models import Clip, Job, JobStage, JobStatus, Project
from app.pipeline.captions import burn_captions, write_srt
from app.pipeline.fetch_source import download_source
from app.pipeline.highlights import select_highlights
from app.pipeline.render import cut_and_reframe
from app.pipeline.transcribe import transcribe


def _log_stage(db, project_id, stage, status, error=None):
    db.add(Job(project_id=project_id, stage=stage, status=status, error=error))
    db.commit()


@celery.task(name="app.tasks.process_project")
def process_project(project_id: str) -> None:
    db = SessionLocal()
    project = None
    try:
        project = db.get(Project, uuid.UUID(project_id))
        if project is None:
            return

        project.status = JobStatus.running
        db.commit()

        project_dir = os.path.join(settings.storage_path, project_id)
        os.makedirs(project_dir, exist_ok=True)

        _log_stage(db, project.id, JobStage.fetch_source, JobStatus.running)
        source_path = project.source_file_path or download_source(project.source_url, project_dir)
        _log_stage(db, project.id, JobStage.fetch_source, JobStatus.completed)

        _log_stage(db, project.id, JobStage.transcribe, JobStatus.running)
        segments = transcribe(source_path)
        _log_stage(db, project.id, JobStage.transcribe, JobStatus.completed)

        _log_stage(db, project.id, JobStage.score_highlights, JobStatus.running)
        highlights = select_highlights(segments)
        _log_stage(db, project.id, JobStage.score_highlights, JobStatus.completed)

        _log_stage(db, project.id, JobStage.render_clips, JobStatus.running)
        for highlight in highlights:
            clip_id = uuid.uuid4()
            cut_path = os.path.join(project_dir, f"{clip_id}.mp4")
            cut_and_reframe(source_path, highlight["start"], highlight["end"], cut_path)

            srt_path = os.path.join(project_dir, f"{clip_id}.srt")
            write_srt(segments, highlight["start"], highlight["end"], srt_path)

            final_path = os.path.join(project_dir, f"{clip_id}_captioned.mp4")
            burn_captions(cut_path, srt_path, final_path)

            db.add(
                Clip(
                    id=clip_id,
                    project_id=project.id,
                    start_seconds=highlight["start"],
                    end_seconds=highlight["end"],
                    reason=highlight.get("reason"),
                    video_path=final_path,
                    caption_srt_path=srt_path,
                )
            )
        db.commit()
        _log_stage(db, project.id, JobStage.render_clips, JobStatus.completed)
        _log_stage(db, project.id, JobStage.burn_captions, JobStatus.completed)

        project.status = JobStatus.completed
        db.commit()
    except Exception as exc:
        db.rollback()
        if project is not None:
            _log_stage(db, project.id, JobStage.done, JobStatus.failed, error=str(exc))
            project.status = JobStatus.failed
            db.commit()
        raise
    finally:
        db.close()
