# In finviz_scanner.py
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd


class FinvizScanner:
    def __init__(self, url):
        self.url = url

    def url_response(self, final_url):
        try:
            req = Request(url=final_url, headers={'user-agent': 'my-app'})
            response = urlopen(req)
            return BeautifulSoup(response, 'html.parser')
        except Exception as e:
            print("Error fetching URL:", e)
            return None

    def url_screener_pages(self):
        url_root = 'https://finviz.com/'
        html_ls = []
        final_url = self.url

        while True:
            html = self.url_response(final_url)
            if not html:
                break

            html_ls.append(html)

            td = html.find('td', {"class": "body-table screener_pagination"})
            a = td.select('a > svg')

            has_arrow_forward = any('arrowForward' in i.select('use')[
                                    0]['href'] for i in a)

            if not has_arrow_forward:
                break

            for x in a:
                a_tag = x.find_parent()['href']
                use = x.select('use')[0]['href']

                if 'Forward' in use:
                    final_url = url_root + a_tag
                    break

        return html_ls

    def get_tables(self):

        frames = []
        html_ls = self.url_screener_pages()
        for html in html_ls:
            tr = html.find(id="screener-table")

            table = tr.select('td > table > tr > td > table')[0]
            df = pd.read_html(str(table), header=0)[0]
            frames.append(df)
        df = pd.concat(frames)
        df['Change'] = df['Change'].str.strip('%').astype(float)
        return df
