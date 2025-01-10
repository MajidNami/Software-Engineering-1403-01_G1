import requests
from .utils import *


class DictionaryAPI:
    API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    def __make_word(self, data: dict) -> Word:
        word = Word(data['word'])

        for meaning in data['meanings']:
            meaning_obj = Meaning(meaning['partOfSpeech'])

            for definition in meaning['definitions']:
                if ('example' not in definition):
                    definition_obj = Definition(definition['definition'])
                else :
                    definition_obj = Definition(definition['definition'], definition['example'])
                meaning_obj.addDefinition(definition_obj)

            for synonym in meaning['synonyms']:
                meaning_obj.addSynonym(synonym)

            for antonym in meaning['antonyms']:
                meaning_obj.addAntonym(antonym)

            word.addMeaning(meaning_obj)

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
        print(f"Term: {word.term}")

        for meaning in word.meanings:
            print(f"Part of speech: {meaning.partOfSpeech}")

            for definition in meaning.definitions:
                print(f"Definition: {definition.definition}")
                if definition.hasExample():
                    print(f"Example: {definition.example}")

            print(f"Synonyms: {', '.join(meaning.synonyms)}")
            print(f"Antonyms: {', '.join(meaning.antonyms)}")
    else:
        print("Word not found")