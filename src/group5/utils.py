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
    


class Word:
    term = ""
    meanings = []

    def __init__(self, term):
        self.term = term

    def addMeaning(self, meaning):
        self.meanings.append(meaning)

    def to_dict(self):
        return {
            "term": self.term,
            "meanings": [meaning.to_dict() for meaning in self.meanings]
        }