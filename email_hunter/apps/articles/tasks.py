import time
from celery import shared_task
from ...core import Article as Hunter, ArticleException as HunterException
from ...core.spiders.browser import Chrome
from .models import Article, ARTICLE_STATE, Bucket, BUCKET_STATE


DEFAULT_META = {
    'total': 0,
    'current': 0
}

HTTPS_PROTOCOL_PREFIX = 'https://'
HTTP_PROTOCOL_PREFIX = 'http://'


def try_with_http_protocol(article, browser=None):
    if not article.url.startswith(HTTPS_PROTOCOL_PREFIX):
        return False
    
    if browser is None:
        browser = Chrome()

    url = HTTP_PROTOCOL_PREFIX + article.url[len(HTTPS_PROTOCOL_PREFIX):]
    hunter = Hunter(url)
    browser.get(url)
    time.sleep(1)
    # hunter.download()
    hunter.download(input_html=browser.page_source)

    result = False
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
            result = True
        else:
            if article.bucket.is_test_data:
                if article.authors.get('origin').lower() in hunter.text.lower() or\
                        article.authors.get('origin').lower() in hunter.html.lower():
                    article.state = ARTICLE_STATE.not_found
                else:
                    article.state = ARTICLE_STATE.no_author
            else:
                article.state = ARTICLE_STATE.not_found
    browser.quit()
    return result

@shared_task(bind=True)
def extract_authors(self, bucket_id, article_ids):
    bucket = Bucket.objects.get(pk=bucket_id)
    bucket.state = BUCKET_STATE.in_progress
    bucket.save()

    DEFAULT_META.update({'total': len(article_ids), 'current': 0})
    
    self.update_state(state="PROGRESS", meta=DEFAULT_META)
    if not isinstance(article_ids, list):
        return DEFAULT_META
    
    browser = Chrome()

    for id in article_ids:
        article = Article.objects.get(pk=id)
        article.state = ARTICLE_STATE.in_progress
        article.save()

        # TODO: Should extract author
        hunter = Hunter(article.url)
        browser.get(article.url)
        time.sleep(1)
        
        # hunter.download()
        hunter.download(input_html=browser.page_source)

        try:
            hunter.parse()
        except HunterException as e:
            print(str(e))
            if article.url.startswith(HTTPS_PROTOCOL_PREFIX):
                try_with_http_protocol(article, browser)
            else:
                article.state = ARTICLE_STATE.page_not_found
        except Exception as e:
            print(str(e))
            if article.url.startswith(HTTPS_PROTOCOL_PREFIX):
                try_with_http_protocol(article)
            else:
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
                        article.state = ARTICLE_STATE.no_author
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
    browser.quit()
    return DEFAULT_META