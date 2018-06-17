from nltk import PorterStemmer
from lazy import lazy
import string
from typing import List, Set
from nltk.corpus import stopwords 
import nltk
from itertools import product

try:
    stopwords = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stopwords = set(stopwords.words('english'))

class EnglishAnalyzer:
    """ A tokenizer that removes stop words, puncuation and uses Stemming """
    DEFAULT_MAX_TOKEN_LENGTH = 255

    @lazy
    def stemmer(self):
        return PorterStemmer()
    
    @staticmethod
    def EnglishPosessiveFilter(tokens: List[str]) -> List[str]:
        def without_posessive(token: str) -> str:
            for combination in product({'\'', '\u2019', '\uFF07'}, {'s', 'S'}):
                token = token.replace(''.join(combination), '')
            return token
        return [without_posessive(token) for token in tokens]

    @staticmethod
    def StopFilter(tokens,stopwords=stopwords):
        return [token for token in tokens if token not in stopwords]

    def tokenize(self, text : str) -> List[str]:
        tokens = text.split()
        return self.apply_filters(tokens)
    
    def StemmerFilter(self, tokens, stemExclusionSet=set()) -> Set[str]:
        return {self.stemmer.stem(token) for token in tokens if token not in stemExclusionSet} + stemExclusionSet

    def apply_filters(self,tokens : List[str]) -> List[str]:
        tokens = EnglishAnalyzer.EnglishPosessiveFilter(tokens)
        tokens = [token.lower() for token in tokens] # LowerFilter
        tokens = [token for token in tokens if token not in string.punctuation]  # PunctuationFilter
        tokens = EnglishAnalyzer.StopFilter(tokens)
        tokens = list(self.StemmerFilter(tokens))
        return tokens
