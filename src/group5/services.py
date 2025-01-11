import requests
from .utils import *
from .secret import THESARUS_API_KEY


class DictionaryAPI:
    DICT_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"
    THESARUS_API_URL = "https://api.api-ninjas.com/v1/thesaurus?word={}"

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

            word.addMeaning(meaning_obj)

    def __make_word(self, dict_data: dict, thesarus_data: dict) -> Word:
        word = Word(dict_data['word'])

        if 'phonetics' in dict_data:
            self.__set_phoentics(word, dict_data['phonetics'])

        if 'meanings' in dict_data:
            self.__set_meanings(word, dict_data['meanings'])

        if 'synonyms' in thesarus_data:
            word.synonyms = [synonym for synonym in thesarus_data['synonyms'] if synonym.strip() != ""]

        if 'antonyms' in thesarus_data:
            word.antonyms = [antonym for antonym in thesarus_data['antonyms'] if antonym.strip() != ""]

        return word

    def fetch_word(self, term: str) -> Word:
        term = term.lower()
        dict_respone = requests.get(self.DICT_API_URL.format(term))
        thesarus_response = requests.get(
            self.THESARUS_API_URL.format(term),
            headers={"X-Api-Key": THESARUS_API_KEY},
        )

        if dict_respone.status_code != 200:
            return None

        return self.__make_word(dict_respone.json()[0], thesarus_response.json())


if __name__ == "__main__":
    api = DictionaryAPI()
    word = api.fetch_word("lord")

    if word is not None:
        print(word.to_dict())
    else:
        print("Word not found")
