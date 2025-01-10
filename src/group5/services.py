import requests
from .utils import *


class DictionaryAPI:
    API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    instance = None

    def getInstance():
        if DictionaryAPI.instance is None:
            DictionaryAPI.instance = DictionaryAPI()
        return DictionaryAPI.instance

    def __set_phoentics(self, word: Word, phonetics: list):
        for phonetic in phonetics:
            if "text" not in phonetic:
                phonetic_obj = Phonetic("")
            else:
                phonetic_obj = Phonetic(phonetic["text"])

            # us format: */<term>-us.mp3
            # uk format: */<term>-uk.mp3
            if "audio" in phonetic:
                phonetic_obj.audio_url = phonetic["audio"]
                if phonetic["audio"].endswith("us.mp3"):
                    word.us_phonetic = phonetic_obj
                elif phonetic["audio"].endswith("uk.mp3"):
                    word.uk_phonetic = phonetic_obj

    def __set_definitions(self, meaning: Meaning, definitions: list):
        for definition in definitions:
            if ('example' not in definition):
                definition_obj = Definition(definition['definition'])
            else :
                definition_obj = Definition(definition['definition'], definition['example'])
            meaning.addDefinition(definition_obj)

    def __set_meanings(self, word: Word, meanings: list):
        for meaning in meanings:
            meaning_obj = Meaning(meaning['partOfSpeech'])

            if 'definitions' in meaning:
                self.__set_definitions(meaning_obj, meaning['definitions'])

            for synonym in meaning['synonyms']:
                meaning_obj.addSynonym(synonym)

            for antonym in meaning['antonyms']:
                meaning_obj.addAntonym(antonym)

            word.addMeaning(meaning_obj)

    def __make_word(self, data: dict) -> Word:
        word = Word(data['word'])

        if 'phonetics' in data:
            self.__set_phoentics(word, data['phonetics'])

        if 'meanings' in data:
            self.__set_meanings(word, data['meanings'])

        return word

    def fetch_word(self, term: str) -> Word:
        response = requests.get(self.API_URL + term)

        if response.status_code != 200:
            return None

        return self.__make_word(response.json()[0])


if __name__ == "__main__":
    api = DictionaryAPI()
    word = api.fetch_word("lord")

    if word is not None:
        print(word.to_dict())
    else:
        print("Word not found")
