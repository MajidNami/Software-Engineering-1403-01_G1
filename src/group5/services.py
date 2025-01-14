import requests
from .utils import *
from .secret import THESARUS_API_KEY
from database.secret import *
from .database.query import *
from .abbreviations import POS_ABBREVIATIONS
import concurrent.futures



class DictionaryAPI:
    PHON_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"
    THESARUS_API_URL = "https://api.api-ninjas.com/v1/thesaurus?word={}"
    DB_CONNECTION = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

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
            if (definition[4] != None): # If there is an example
                definition_obj = Definition(definition[3], definition[4])
            else:
                definition_obj = Definition(definition[3])
            meaning.addDefinition(definition_obj)

    def __set_meanings(self, word: Word, meanings: list):
        pos_dict = {}
        for entry in meanings:
            pos = entry[2]
            if pos in POS_ABBREVIATIONS.keys():
                pos = POS_ABBREVIATIONS[pos]

            if pos not in pos_dict:
                pos_dict[pos] = []
            pos_dict[pos].append(entry)
            
        for pos in pos_dict.keys():
            meaning_obj = Meaning(pos)
            self.__set_definitions(meaning_obj, pos_dict[pos])
            word.addMeaning(meaning_obj)

    def __make_word(self, phon_data: dict, thesarus_data: dict, db_response: list) -> Word:
        word = Word(phon_data['word'])

        if 'phonetics' in phon_data:
            self.__set_phoentics(word, phon_data['phonetics'])

        if len(db_response) != 0:
            self.__set_meanings(word, db_response)

        if 'synonyms' in thesarus_data:
            word.synonyms = [synonym for synonym in thesarus_data['synonyms'] if synonym.strip() != ""]

        if 'antonyms' in thesarus_data:
            word.antonyms = [antonym for antonym in thesarus_data['antonyms'] if antonym.strip() != ""]

        return word

    def fetch_word(self, term: str) -> Word:
        term = term.lower()

        # Fetch data from APIs concurrently 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            db_future = executor.submit(fetch_word_db, self.DB_CONNECTION, term)
            phon_future = executor.submit(requests.get, self.PHON_API_URL.format(term))
            thesarus_future = executor.submit(
                requests.get,
                self.THESARUS_API_URL.format(term),
                headers={"X-Api-Key": THESARUS_API_KEY},
            )

            db_response = db_future.result()
            phon_response = phon_future.result()
            thesarus_response = thesarus_future.result()

        if phon_response.status_code != 200:
            return None

        return self.__make_word(phon_response.json()[0], thesarus_response.json(), db_response)


if __name__ == "__main__":
    api = DictionaryAPI()
    word = api.fetch_word("lord")

    if word is not None:
        print(word.to_dict())
    else:
        print("Word not found")
