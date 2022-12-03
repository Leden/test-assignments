import logging

from celery import Task

logger = logging.getLogger(__name__)


class BaseTask(Task):
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = 60
    retry_backoff_max = 600
    retry_jitter = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Celery task {self.name} with {task_id} failed", exc_info=exc)
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)
