from fetch_meditation.JFTLanguage import JFTLanguage
from fetch_meditation.EnglishJFT import EnglishJFT
from fetch_meditation.GermanJFT import GermanJFT
from fetch_meditation.JapaneseJFT import JapaneseJFT
from fetch_meditation.PortugueseJFT import PortugueseJFT
from fetch_meditation.RussianJFT import RussianJFT


class JFT:
    def __init__(self, settings):
        self.settings = settings

    def fetch(self):
        pass

    def get_language(self):
        pass

    @staticmethod
    def get_instance(settings):
        return {
            JFTLanguage.English: EnglishJFT,
            JFTLanguage.German: GermanJFT,
            JFTLanguage.Japanese: JapaneseJFT,
            JFTLanguage.Portuguese: PortugueseJFT,
            JFTLanguage.Russian: RussianJFT,
        }[settings.language](settings)
