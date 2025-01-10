# Since these classes don't use database, they are not models and shouldn't be in models.py.

class Definition:
    definition = ""
    example = ""

    def __init__(self, definition, example=None):
        self.definition = definition
        self.example = example

    def hasExample(self):
        return self.example is not None

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
    


class Word:
    term = ""
    meanings = []

    def __init__(self, term):
        self.term = term

    def addMeaning(self, meaning):
        self.meanings.append(meaning)
