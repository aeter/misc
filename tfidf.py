"""
A prototype of tf-idf.

Copyright 2011 Adrian Nackov
Released under BSD Licence (3 clause):
http://www.opensource.org/licenses/bsd-license.php
"""

from math import log10

def tf_idf(doc, all_docs, term):
  '''
  Input:
    all_docs: a list of docs, such as [["Once", "upon"...], ["There", "was"]]
    term: a phrase (term), such as "upon" or "was", etc.
    doc - a list of phrases, such as ["Once", "upon", "a", "time"]

    Also doc should be one of the documents in all_docs.
  '''
  assert(doc in all_docs, "The document is not from the corpus")
  return tf(term, doc) * idf(term, all_docs)

def idf(term, all_docs):
  '''
  Input:
    docs: a list of docs, such as [["Once", "upon"...], ["There", "was"]]
    term: a phrase (term), such as "upon" or "was", etc.
  '''
  return log10(len(docs) /
               1 + len(doc for doc in docs if term in doc))

def tf(term, doc):
  '''
  Input:
    doc - a list of phrases, such as ["Once", "upon", "a", "time"]
    term - a phrase like the ones in doc, such as "a" or "time", etc.
  '''
  return doc.count(term) / len(doc)

