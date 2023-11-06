from fetch_meditation.SPADLanguage import SPADLanguage
from fetch_meditation.EnglishSPAD import EnglishSPAD


class SPAD:
    def __init__(self, settings):
        self.settings = settings

    def fetch(self):
        pass

    def get_language(self):
        pass

    @staticmethod
    def get_instance(settings):
        return {
            SPADLanguage.English: EnglishSPAD,
        }[settings.language](settings)
