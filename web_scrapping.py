from googlesearch import search
import urllib3
from bs4 import BeautifulSoup
import re

HEADER_FORMAT = "************************\n\n[Result {0}]\n       {1}\n[Website]\n       {2}\n\n************************\n"


def google_search(question_to_search):
    keywords = question_to_search['keyword']
    reg_keywords = "|".join([k for k in keywords])

    # API Documentation:
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    query = question_to_search['question']

    final_results = ""
    num_results = 1
    for url in search(query, stop=2):
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        soup = BeautifulSoup(r.data.decode('utf-8'), 'html.parser')

        final_results += HEADER_FORMAT.format(num_results, soup.title.string, url)
        for m in soup.find_all('meta'):
            if m.get('property') == 'og:description':
                final_results += "[DESCRIPTION]\n       {0}\n\n".format(m.get('content'))

        all_text = ""

        num_lines = 0
        # Source: https://stackoverflow.com/a/56328585
        for t in soup.find_all(text=True):
            blacklist = [
                'style',
                'script',
                'span',
                'a',
                'div',
                'head',
                'link',
                'meta'
            ]
            if t.parent.name not in blacklist:
                if re.search(reg_keywords, str(t), re.I) and re.search('^[A-Z0-9]', str(t)):
                    if len(str(t)) > 20:
                        num_lines += 1
                        all_text = "{0}{1}. {2}\n".format(all_text, str(num_lines), str(t))

        num_results += 1
        final_results = final_results + all_text + "\n"

    return final_results