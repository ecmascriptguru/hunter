from django import template
from ..utils import get_celery_task_state


register = template.Library()


@register.filter('job_prepare_pecent')
def job_prepare_pecent(job):
    info = get_celery_task_state(job)
    if isinstance(info, dict):
        return int(info['prepare']['cur'] / info['prepare']['total'] * 100)
    return 0


@register.filter('job_candidates_pecent')
def job_candidates_pecent(job):
    info = get_celery_task_state(job)
    if isinstance(info, dict):
        return int(info['candidates']['cur'] / info['candidates']['total'] * 100)
    return 0


@register.filter('job_step_pecent')
def job_step_pecent(job):
    info = get_celery_task_state(job)
    if isinstance(info, dict):
        return int(info['step']['cur'] / info['step']['total'] * 100)
    return 0


@register.filter('job_pattern_pecent')
def job_pattern_pecent(job):
    info = get_celery_task_state(job)
    if isinstance(info, dict):
        return int(info['pattern']['cur'] / info['pattern']['total'] * 100)
    return 0


@register.filter('job_total_percent')
def job_total_percent(job):
    info = get_celery_task_state(job)
    if isinstance(info, dict):
        return int(info['candidates']['cur'] / max(1, len(job.targets.all())) * 100)
    return 0