import re
from newspaper import Article, ArticleException
from newspaper.extractors import ContentExtractor
from newspaper.configuration import Configuration


class AuthorHunterConfiguration(Configuration):
    def __init__(self, *args, **kwargs):
        super(AuthorHunterConfiguration, self).__init__(*args, **kwargs)
        self.browser_user_agent = 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        self.request_timeout = 20


class CustomContextExtractor(ContentExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_authors(self, doc):
        """Fetch the authors of the article, return as a list
        Only works for english articles
        """
        _digits = re.compile('\d')

        def contains_digits(d):
            return bool(_digits.search(d))

        def uniqify_list(lst):
            """Remove duplicates from provided list but maintain original order.
              Derived from http://www.peterbe.com/plog/uniqifiers-benchmark
            """
            seen = {}
            result = []
            for item in lst:
                if item.lower() in seen:
                    continue
                seen[item.lower()] = 1
                result.append(item.title())
            return result

        def parse_byline(search_str):
            """
            Takes a candidate line of html or text and
            extracts out the name(s) in list form:
            >>> parse_byline('<div>By: <strong>Lucas Ou-Yang</strong>,<strong>Alex Smith</strong></div>')
            ['Lucas Ou-Yang', 'Alex Smith']
            """
            # Remove HTML boilerplate
            search_str = re.sub('<[^<]+?>', '', search_str)

            # Remove original By statement
            search_str = re.sub('[bB][yY][\:\s]|[fF]rom[\:\s]', '', search_str)

            search_str = search_str.strip()

            # Chunk the line by non alphanumeric tokens (few name exceptions)
            # >>> re.split("[^\w\'\-\.]", "Tyler G. Jones, Lucas Ou, Dean O'Brian and Ronald")
            # ['Tyler', 'G.', 'Jones', '', 'Lucas', 'Ou', '', 'Dean', "O'Brian", 'and', 'Ronald']
            name_tokens = re.split("[^\w\'\-\.]", search_str)
            name_tokens = [s.strip() for s in name_tokens]

            _authors = []
            # List of first, last name tokens
            curname = []
            delimiters = ['and', ',', '']

            for token in name_tokens:
                if token in delimiters:
                    if len(curname) > 0:
                        _authors.append(' '.join(curname))
                        curname = []

                elif not contains_digits(token):
                    curname.append(token)

            # One last check at end
            valid_name = (len(curname) >= 2)
            if valid_name:
                _authors.append(' '.join(curname))

            return _authors

        # Try 1: Search popular author tags for authors

        ATTRS = ['name', 'rel', 'itemprop', 'class', 'id']
        VALS = ['author', 'byline', 'dc.creator', 'byl']
        matches = []
        authors = []

        for attr in ATTRS:
            for val in VALS:
                # found = doc.xpath('//*[@%s="%s"]' % (attr, val))
                found = self.parser.getElementsByTag(doc, attr=attr, value=val)
                matches.extend(found)

        for match in matches:
            content = ''
            if match.tag == 'meta':
                mm = match.xpath('@content')
                if len(mm) > 0:
                    content = mm[0]
            else:
                content = match.text or ''
            if len(content) > 0:
                authors.extend(parse_byline(content))

        return uniqify_list(authors)

        # TODO Method 2: Search raw html for a by-line
        # match = re.search('By[\: ].*\\n|From[\: ].*\\n', html)
        # try:
        #    # Don't let zone be too long
        #    line = match.group(0)[:100]
        #    authors = parse_byline(line)
        # except:
        #    return [] # Failed to find anything
        # return authors
from selenium.webdriver import Chrome
class AuthorHunter(Article):
    def __init__(self, *args, **kwargs):
        super(AuthorHunter, self).__init__(*args, **kwargs)
        self.config = AuthorHunterConfiguration()
        self.extractor = CustomContextExtractor(self.config)
