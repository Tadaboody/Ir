from nltk import PorterStemmer
from lazy import lazy
import string
from typing import List, Set, Iterable
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
        """" Removes possesives in english (mike's -> mike)"""

        def without_posessive(token: str) -> str:
            """Possesive filter for a single token"""
            for combination in product({'\'', '\u2019', '\uFF07'}, {'s', 'S'}):
                posessive_str = ''.join(combination)
                token = token.replace(posessive_str, '')
            return token

        return [without_posessive(token) for token in tokens]

    @staticmethod
    def StopFilter(tokens,stopwords=stopwords):
        return [token for token in tokens if token not in stopwords]

    def tokenize(self, text : str) -> List[str]:
        tokens = text.split()
        return self.apply_filters(tokens)
    
    def StemmerFilter(self, tokens, stemExclusionSet=set()) -> Set[str]:
        return {self.stemmer.stem(token) for token in tokens if token not in stemExclusionSet} | stemExclusionSet
    
    def PunctuationFilter(self,tokens : Iterable[str]) -> Iterable[str]:
        def without_punctuation(token :str) -> str:
            return [char for char in token if char not in string.punctuation]
        return [without_punctuation(token) for token in tokens]

    def apply_filters(self,tokens : List[str]) -> List[str]:
        tokens = EnglishAnalyzer.EnglishPosessiveFilter(tokens)
        tokens = [token.lower() for token in tokens] # LowerFilter
        tokens = [token for token in tokens if token not in string.punctuation]  # PunctuationFilter
        tokens = EnglishAnalyzer.StopFilter(tokens)
        tokens = list(self.StemmerFilter(tokens))
        return tokens
