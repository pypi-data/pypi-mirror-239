from dataclasses import dataclass
from typing import Any, Union
from fetch_meditation.jft_language import JftLanguage
from fetch_meditation.english_jft import EnglishJft
from fetch_meditation.german_jft import GermanJft
from fetch_meditation.japanese_jft import JapaneseJft
from fetch_meditation.portuguese_jft import PortugueseJft
from fetch_meditation.russian_jft import RussianJft


@dataclass
class Jft:
    settings: Any

    @property
    def language(self) -> JftLanguage:
        return self.settings.language

    @staticmethod
    def get_instance(settings: Any) -> Union[EnglishJft, GermanJft, JapaneseJft, PortugueseJft, RussianJft]:
        return {
            JftLanguage.English: EnglishJft,
            JftLanguage.German: GermanJft,
            JftLanguage.Japanese: JapaneseJft,
            JftLanguage.Portuguese: PortugueseJft,
            JftLanguage.Russian: RussianJft,
        }[settings.language](settings)
