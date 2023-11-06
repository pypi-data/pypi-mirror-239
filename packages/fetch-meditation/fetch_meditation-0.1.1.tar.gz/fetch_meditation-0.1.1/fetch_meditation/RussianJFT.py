from bs4 import BeautifulSoup
from fetch_meditation.utilities.HttpUtility import HttpUtility
from fetch_meditation.JFTEntry import JFTEntry


class RussianJFT:
    def __init__(self, settings):
        self.settings = settings

    def get_language(self):
        return self.settings.language

    def fetch(self):
        url = 'https://na-russia.org/eg'
        data = HttpUtility.http_get(url)
        soup = BeautifulSoup(data, 'html.parser')
        jftKeys = ['date', 'title', 'quote',
                   'source', 'content', 'thought', 'page']

        result = {
            'date': '',
            'quote': '',
            'source': '',
            'thought': '',
            'content': [],
            'title': '',
            'page': '',
            'copyright': ''
        }

        tables = soup.find_all('table')
        if len(tables) > 0:
            firstTable = tables[0]
            td_list = firstTable.find_all('td')
            for i, td in enumerate(td_list):
                if jftKeys[i] == 'content':
                    innerHTML = ''.join(str(child) for child in td.contents)
                    result['content'] = [line.strip()
                                         for line in innerHTML.split('<br/>') if line.strip()]
                else:
                    result[jftKeys[i]] = td.get_text().strip()

        return JFTEntry(
            result['date'],
            result['title'],
            result['page'],
            result['quote'],
            result['source'],
            result['content'],
            result['thought'],
            result['copyright']
        )
