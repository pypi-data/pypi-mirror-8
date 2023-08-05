from __future__ import absolute_import
import requests
import dateutil.parser
from bs4 import BeautifulSoup
from amazon_scraper import review_url, extract_review_id, process_rating, strip_html_tags, dict_acceptable, retry, rate_limit, user_agent


class Review(object):
    def __init__(self, api, Id=None, URL=None):
        if Id and not URL:
            if 'amazon' in Id:
                raise ValueError('URL passed as ID')

            URL = review_url(Id)

        if not URL:
            raise ValueError('Invalid review page parameters')

        self.api = api
        self._URL = URL
        self._soup = None

    @property
    @retry()
    def soup(self):
        if not self._soup:
            rate_limit(self.api)
            r = requests.get(self._URL, headers={'User-Agent':user_agent}, verify=False)
            r.raise_for_status()
            #self._soup = BeautifulSoup(r.text, 'html.parser')
            self._soup = BeautifulSoup(r.text, 'html5lib')
        return self._soup

    @property
    def id(self):
        anchor = self.soup.find('a', attrs={'name':True}, text=False)
        id = unicode(anchor['name'])
        return id

    @property
    def asin(self):
        tag = self.soup.find('abbr', class_='asin')
        asin = unicode(tag.string)
        return asin

    @property
    def url(self):
        return review_url(self.id)

    @property
    def title(self):
        tag = self.soup.find('span', class_='summary')
        title = unicode(tag.string)
        return title.strip()

    @property
    def rating(self):
        """The rating of the product normalised to 1.0
        """
        for li in self.soup.find_all('li', class_='rating'):
            string = li.stripped_strings.next().lower()
            if 'overall:' not in string:
                continue

            img = li.find('img')
            rating = unicode(img['title'])
            return process_rating(rating)

    @property
    def date(self):
        abbr = self.soup.find('abbr', class_='dtreviewed')
        string = unicode(abbr['title'])
        # 2011-11-07T05:50:41Z
        date = dateutil.parser.parse(string)
        return date

    @property
    def author(self):
        # http://www.amazon.com/review/R3MF0NIRI3BT1E
        # http://www.amazon.com/review/RI3ARYEHW5DT5
        # http://www.amazon.com/review/R2OD03CRAU7EDV
        vcard = self.soup.find('span', class_='reviewer vcard')
        if vcard:
            tag = vcard.find(class_='fn')
            if tag:
                author = unicode(tag.string)
                return author
        return None

    @property
    def text(self):
        tag = self.soup.find('span', class_='description')
        return strip_html_tags(unicode(tag))

    def to_dict(self):
        d = {
            k:getattr(self, k)
            for k in dir(self)
            if dict_acceptable(self, k, blacklist=['soup', '_URL', '_soup'])
        }
        return d
