"""Small deterministic lexical helpers for candidate discovery.

These helpers deliberately stay below semantic selection.  They remove language
function words, discount terms that occur in nearly every document, and expose the
terms that actually matched so the active model/user can judge the candidates.
"""
from collections import Counter
import math
import re


# A compact language stop list, not a domain or intent denylist.  Domain words such
# as ``image``, ``article``, and ``workflow`` remain discoverable even when they are
# common in one operating area.
STOPWORDS = frozenset(
    """
    a an and are as at be been being but by can could did do does for from had has
    have he her here hers herself him himself his how i if in into is it its itself
    just me more most my myself no nor not of on once only or our ours ourselves out
    over own same she should so some such than that the their theirs them themselves
    then there these they this those through to too under until up very was we were
    what when where which while who whom why will with would you your yours yourself
    yourselves about above across after again against along already also although among
    around because before behind below beside besides between beyond during each few
    further here how however indeed its itself many meanwhile might more much neither
    nevertheless next often perhaps rather several since some sometime still though
    toward upon via whether yet
    """.split()
)


def raw_tokens(value):
    """Return lower-cased word tokens, retaining function words for phrase checks."""
    return re.findall(r"[a-z0-9]+", str(value or "").lower())


def tokens(value):
    """Return meaningful lexical tokens for bounded candidate scoring."""
    return [token for token in raw_tokens(value) if token not in STOPWORDS and len(token) >= 2]


def token_set(value):
    return set(tokens(value))


def phrase_tokens(value):
    """Return phrase tokens without substring matching or punctuation surprises."""
    return raw_tokens(value)


def contains_phrase(haystack, needle):
    phrase = phrase_tokens(needle)
    if not phrase:
        return False
    words = phrase_tokens(haystack)
    width = len(phrase)
    return any(words[index:index + width] == phrase for index in range(len(words) - width + 1))


def document_frequency(rows, fields):
    """Count in how many documents each meaningful token occurs."""
    result = Counter()
    for row in rows:
        terms = set()
        for field in fields:
            value = row.get(field, "") if isinstance(row, dict) else ""
            if isinstance(value, (list, tuple, set)):
                value = " ".join(str(item) for item in value)
            terms.update(tokens(value))
        result.update(terms)
    return result


def weighted_overlap(query_terms, document_terms, frequencies, document_count):
    """Return a deterministic inverse-document-frequency weighted overlap."""
    query_set = set(query_terms if not isinstance(query_terms, str) else tokens(query_terms))
    if isinstance(document_terms, str):
        document_set = set(tokens(document_terms))
    elif isinstance(document_terms, (list, tuple, set)):
        document_set = set(str(term).lower() for term in document_terms)
        # Generated indexes already hold word tokens, while authored lists may hold
        # phrases; normalize either form without treating a list's punctuation as text.
        if any(' ' in term or not re.fullmatch(r'[a-z0-9]+', term) for term in document_set):
            document_set = set(tokens(' '.join(document_set)))
    else:
        document_set = set(tokens(document_terms))
    matched = sorted(query_set & document_set)
    if not matched:
        return 0.0, []
    total = max(1, int(document_count))
    score = sum(1.0 + math.log((total + 1) / (frequencies.get(term, 0) + 1)) for term in matched)
    return round(score, 6), matched
