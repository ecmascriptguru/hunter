from celery import shared_task
from .models import Article, ARTICLE_STATE, Bucket, BUCKET_STATE


DEFAULT_META = {
    'total': 0,
    'current': 0
}


@shared_task(bind=True)
def extract_authors(self, bucket_id, article_ids):
    bucket = Bucket.objects.get(pk=bucket_id)
    bucket.state = BUCKET_STATE.in_progress
    bucket.save()

    DEFAULT_META.update({'total': len(article_ids)})
    
    self.update_state(state="PROGRESS", meta=DEFAULT_META)
    if not isinstance(article_ids, list):
        return DEFAULT_META
    
    for id in article_ids:
        article = Article.objects.get(pk=id)
        article.state = ARTICLE_STATE.in_progress
        article.save()

        # TODO: Should extract author
        article.state = ARTICLE_STATE.default
        article.save()
        DEFAULT_META.update({'current': DEFAULT_META.get('current') + 1})
        self.update_state(state="PROGRESS", meta=DEFAULT_META)
    
    self.update_state(state="COMPLETE", meta=DEFAULT_META)
    bucket.state = BUCKET_STATE.default
    bucket.job_uuid = None
    bucket.save()
    
    return DEFAULT_META