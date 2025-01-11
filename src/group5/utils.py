# Since these classes don't use database, they are not models and shouldn't be in models.py.

class Definition:
    def __init__(self, definition, example=None):
        self.definition = definition
        self.example = example

    def hasExample(self):
        return self.example is not None

    def to_dict(self):
        return {"definition": self.definition, "example": self.example}


class Meaning:
    DIFINITIONS_LIMIT = 3
    def __init__(self, partOfSpeech):
        self.partOfSpeech = partOfSpeech
        self.definitions = []

    def addDefinition(self, definition):
        self.definitions.append(definition)

    def to_dict(self):
        return {
            "partOfSpeech": self.partOfSpeech,
            "definitions": [
                definition.to_dict()
                for definition in self.definitions[: Meaning.DIFINITIONS_LIMIT]
            ],
        }


class Phonetic:
    def __init__(self, text, audio_url=None):
        self.text = text
        self.audio_url = audio_url

    def to_dict(self):
        return {
            "text": self.text,
            "audio_url": self.audio_url
        }


class Word:
    SYNONYMS_LIMIT = 3
    ANTONYMS_LIMIT = 3

    def __init__(self, term):
        self.term = term
        self.us_phonetic = None
        self.uk_phonetic = None
        self.meanings = []
        self.synonyms = []
        self.antonyms = []

    def addMeaning(self, meaning):
        self.meanings.append(meaning)

    def setUSPhonetic(self, phonetic):
        self.us_phonetic = phonetic

    def setUKPhonetic(self, phonetic):
        self.uk_phonetic = phonetic

    def to_dict(self):
        return {
            "term": self.term,
            "us_phonetic": self.us_phonetic.to_dict() if self.us_phonetic is not None else None,
            "uk_phonetic": self.uk_phonetic.to_dict() if self.uk_phonetic is not None else None,
            "meanings": [meaning.to_dict() for meaning in self.meanings],
            "synonyms": self.synonyms[: Word.SYNONYMS_LIMIT],
            "antonyms": self.antonyms[: Word.ANTONYMS_LIMIT],
        }
