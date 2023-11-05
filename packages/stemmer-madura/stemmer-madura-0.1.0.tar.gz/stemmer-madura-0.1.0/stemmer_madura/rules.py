import re

# Rule class
class Rule:
  def __init__(self, name, pattern, replacement, replacements, hasVariance, recover):
    self.name = name
    self.pattern = pattern
    self.replacement = replacement
    self.replacements = replacements
    self.hasVariance = hasVariance
    self.recover = recover

rules = [
  # Reduplication Removal
  Rule(
    'Reduplication Removal',
    re.compile('^.+\-(.+)$'),
    r'\1',
    [],
    False,
    False
  ),

  # Nah Suffix Removal
  # Sepertinya tidak baku, mungkin bentuk dari akhiran "na" (romana, kalambina)
  Rule(
    'Nah Suffix Removal',
    re.compile('^(.+)nah$'),
    r'\1',
    [],
    False,
    True
  ),

  # Plain Suffix Removal 1
  Rule(
    'Plain Suffix Removal 1',
    re.compile('^(.+)(ya|na|ni|an|ih|eh|en|ah)$'),
    r'\1',
    [],
    False,
    'both'
  ),

  # Plain Suffix Removal 2
  Rule(
    'Plain Suffix Removal 2',
    re.compile('^(.+)([aei])$'),
    r'\1',
    [],
    False,
    'both'
  ),

  # Aghi Suffix Removal
  Rule(
    'Aghi Suffix Removal',
    re.compile('^(.+)aghi$'),
    r'\1',
    [],
    False,
    False
  ),

  # Plain Prefix Removal 1
  Rule(
    'Plain Prefix Removal 1',
    re.compile('^([ae])(.+)$'),
    r'\2',
    [],
    False,
    False
  ),

  # Plain Prefix Removal 2
  Rule(
    'Plain Prefix Removal 2',
    re.compile('^(ta|ma|ka|sa|pa|pe)(.+)$'),
    r'\2',
    [],
    False,
    'both'
  ),

  # Plain Prefix Removal 3
  Rule(
    'Plain Prefix Removal 3',
    re.compile('^(par)([^aeuio].+)$'),
    r'\2',
    [],
    False,
    False
  ),

  # Ng Prefix Removal 1
  Rule(
    'Ng Prefix Removal 1',
    re.compile('^ng(.+)$'),
    r'\1',
    [],
    False,
    True
  ),

  # Ng Prefix Modification 2
  Rule(
    'Ng Prefix Modification 2',
    re.compile('^ng([aeio].+)$'),
    '',
    [r'k\1', r'g\1', r'gh\1'],
    True,
    False
  ),

  # M Prefix Modification
  Rule(
    'M Prefix Modification',
    re.compile('^m([aeou].+)$'),
    '',
    [r'b\1', r'p\1', r'bh\1'],
    True,
    False
  ),

  # NY Prefix Modification
  Rule(
    'NY Prefix Modification',
    re.compile('^ny([aeo].+)$'),
    '',
    [r's\1', r'c\1', r'j\1', r'jh\1'],
    True,
    False
  ),

  # N Prefix Modification
  Rule(
    'N Prefix Modification',
    re.compile('^n([aeo].+)$'),
    '',
    [r't\1', r'd\1', r'dh\1'],
    True,
    False
  ),

  # Plain Infix Removal
  Rule(
    'Plain Infix Removal',
    re.compile('^([^aiueo]{1,2})(al|ar|en|in|om|um)(.+)$'),
    r'\1\3',
    [],
    False,
    False
  )
]

