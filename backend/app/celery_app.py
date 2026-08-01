from celery import Celery

from app.config import settings

# Named `celery` (not `celery_app`) so the CLI can find it with just
# `-A app.celery_app`, since Celery looks for an `app`/`celery` attribute
# in the given module by default.
celery = Celery("clipgen", broker=settings.redis_url, backend=settings.redis_url)
celery.autodiscover_tasks(["app"])
