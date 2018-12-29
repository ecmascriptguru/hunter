from ...apps.targets.tasks import validate_targets
from .models import Job


def get_celery_task_state(job):
    if not isinstance(job, Job) or job.internal_uuid is None:
        return None
    else:
        task = validate_targets.AsyncResult(str(job.internal_uuid))
        return task.info