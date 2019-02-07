from celery import shared_task
from newspaper import Article as Hunter, ArticleException as HunterException
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
        hunter = Hunter(article.url)
        hunter.download()

        try:
            hunter.parse()
        except HunterException as e:
            article.state = ARTICLE_STATE.page_not_found
        except Exception as e:
            print(str(e))
            article.state = ARTICLE_STATE.has_error
        else:
            authors = hunter.authors
            if len(authors) > 0:
                article.authors['candidates'] = authors
                if len(authors) > 1:
                    article.state = ARTICLE_STATE.need_confirm
                else:
                    article.authors['found'] = authors[0]
                    article.state = ARTICLE_STATE.found
            else:
                if bucket.is_test_data:
                    if article.authors.get('origin').lower() in hunter.text.lower() or\
                            article.authors.get('origin').lower() in hunter.html.lower():
                        article.state = ARTICLE_STATE.not_found
                    else:
                        article.state = ARTICLE_STATE.page_not_found
                else:
                    article.state = ARTICLE_STATE.not_found
        finally:
            article.save()
            DEFAULT_META.update({'current': DEFAULT_META.get('current') + 1})
            self.update_state(state="PROGRESS", meta=DEFAULT_META)
    
    self.update_state(state="COMPLETE", meta=DEFAULT_META)
    bucket.state = BUCKET_STATE.default
    bucket.job_uuid = None
    bucket.save()

    return DEFAULT_META