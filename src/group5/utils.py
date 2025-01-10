# Since these classes don't use database, they are not models and shouldn't be in models.py.

class Definition:
    definition = ""
    example = ""

    def __init__(self, definition, example=None):
        self.definition = definition
        self.example = example

    def hasExample(self):
        return self.example is not None
    
    def to_dict(self):
        return {
            "definition": self.definition,
            "example": self.example
        }

class Meaning:
    partOfSpeech = ""
    definitions = []
    synonyms = []
    antonyms = []

    def __init__(self, partOfSpeech):
        self.partOfSpeech = partOfSpeech

    def addDefinition(self, definition):
        self.definitions.append(definition)

    def addSynonym(self, synonym):
        self.synonyms.append(synonym)

    def addAntonym(self, antonym):
        self.antonyms.append(antonym)

    def hasSynonyms(self):
        return len(self.synonyms) > 0
    
    def hasAntonyms(self):
        return len(self.antonyms) > 0
    
    def to_dict(self):
        return {
            "partOfSpeech": self.partOfSpeech,
            "definitions": [definition.to_dict() for definition in self.definitions],
            "synonyms": self.synonyms,
            "antonyms": self.antonyms
        }
    

class Phonetic:
    text = ""
    audio_url = ""

    def __init__(self, text, audio_url=None):
        self.text = text
        self.audio_url = audio_url

    def to_dict(self):
        return {
            "text": self.text,
            "audio_url": self.audio_url
        }


class Word:
    term = ""
    us_phonetic = None
    uk_phonetic = None
    meanings = []

    def __init__(self, term):
        self.term = term

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
            "meanings": [meaning.to_dict() for meaning in self.meanings]
        }