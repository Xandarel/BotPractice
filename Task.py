from bs4 import BeautifulSoup
import requests
import urllib3
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2
import nltk
from string import punctuation

nltk.download('punkt')
nltk.download('stopwords')

urllib3.disable_warnings()


class Task:
    def __init__(self, request_text: str, count=1000):
        self.res_text = []  # текст статей
        self.res_tokenize_text = []  # токенизированный текст
        self.morph = pymorphy2.MorphAnalyzer()
        self.stop_words = stopwords.words('russian')
        self.custom_stop_words = ['`', '\"', '\'', '-', '—', '\"\"', '``', '\'\'', '–']
        self.list_url = []  # список ссылок на статьи
        self.request_text = request_text    # запрос польователя
        self.main_url = 'https://ria.ru'    # основная ссылка риа новости
        self.service_url = '/services/search/getmore/?query='  # url на их внутренний сервис поиска. query параметр - текст запроса
        self.search_count = '&offset='  # страница поиска. На одной странице 10 ссылок
        self.search_count_int = count  # количество статей, укаанное пользователем. По-умолчанию 1000

    def _get_html(self, url: str):
        """
        функция достаёт html по url
        """
        ret = None
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
            r = requests.get(url, headers=headers, verify=False)
            ret = r.text
        except Exception as e:
            print(str(e))

        return ret

    def find_request_url(self):
        for i in tqdm(range(0, self.search_count_int, 10)):
            test_url = f'{self.main_url}{self.service_url}{self.request_text}{self.search_count}{i}'
            html = self._get_html(test_url)
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.find_all('a'):
                a_href = a.get("href")
                if a_href and a_href not in self.list_url and 'http' in a_href:
                    self.list_url.append(a_href)

    def get_text_from_article(self):
        for href in tqdm(self.list_url):
            news_soup = BeautifulSoup(self._get_html(href), 'html.parser')
            text = news_soup.find_all('div', {"class": "article__block", 'data-type': 'text'})
            self.res_text.append(' '.join(map(lambda x: x.text, text)))
            self.res_tokenize_text.append(' '.join(self.tokenize_and_lematize(self.res_text[-1])))

    def tokenize_and_lematize(self, text):
        words = [w for w in word_tokenize(text) if (w not in self.stop_words and w not in punctuation and w not in self.custom_stop_words)]
        words = [self.morph.parse(w)[0].normal_form for w in words]
        return words

