import json
from bs4 import BeautifulSoup


class JFTEntry:
    def __init__(self, date, title, page, quote, source, content, thought, copyright):
        self.date = date
        self.title = title
        self.page = page
        self.quote = quote
        self.source = source
        self.content = content
        self.thought = thought
        self.copyright = copyright

    def to_json(self):
        return json.dumps(self.__dict__)

    def without_tags(self):
        def strip_tags(item):
            if isinstance(item, list):
                return [strip_tags(sub_item) for sub_item in item]
            else:
                soup = BeautifulSoup(item, 'html.parser')
                return soup.text

        return {key: strip_tags(value) for key, value in self.__dict__.items()}
