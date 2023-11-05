# from typing import List

# class Files:
#   def __init__(self, stemmer: Stemmer):
#     self._stemmer = stemmer

#   @property
#   def stemmer(self) -> Stemmer:
#     return self._stemmer
  
#   def readFile(self, filename: str) -> List[str]:
#     with open(filename, 'r') as file:
#       return self._splitWordsFile(file.read())
    

#   def _splitWordsFile(self, content: str) -> List[str]:
#     lf = self._getLineBreakChar(content)
#     return list(filter(lambda e: len(e) > 0, map(lambda v: self._stemmer.normalizeString(v), content.split(lf))))

#   def _getLineBreakChar(self, content: str) -> str:
#     index_of_lf = content.find('\n', 1)  # No need to check first-character
#     if index_of_lf == -1:
#       if '\r' in content:
#         return '\r'
#       return '\n'
#     if content[index_of_lf - 1] == '\r':
#       return '\r\n'
#     return '\n'
