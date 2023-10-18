import nltk
from nltk.stem import WordNetLemmatizer
import re

try:
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    nltk.download('wordnet')
    
lemmatizer = WordNetLemmatizer().lemmatize

def all_variant_in_dict(word, D, lemmatizer=lemmatizer, tags="nvars", delimiter=["-", "'"], results=None):
    results = results if results is not None else []
    if word in D:
        results.append(word)
    lower_word = word.lower()
    if lower_word != word and lower_word in D:
        results.append(word.lower())
    strip_word = word.strip(".")
    if strip_word != word and strip_word in D:
        results.append(strip_word)
    strip_lower_word = lower_word.strip(".")
    if strip_lower_word != lower_word and strip_lower_word in D:
        results.append(strip_lower_word)
    for t in tags:
        lem_word = lemmatizer(strip_lower_word, pos = t)
        if lem_word != strip_lower_word and lem_word in D:
            results.append(lem_word)
        cap_word = lem_word.capitalize()
        if cap_word != strip_word and cap_word in D:
            results.append(cap_word)
    for i,d in enumerate(delimiter):
        if d in word:
            words = word.split(d)
            for w in words:
                all_variant_in_dict(w, D, lemmatizer, results=results, delimiter=delimiter[i+1:])
    return list(dict.fromkeys(results))

def check_in_dict(word, D, lemmatizer=lemmatizer, tags="nvars"):
    if word in D:
        return True, word
    lower_word = word.lower()
    if lower_word in D:
        return True, lower_word
    word = word.strip(".")
    if word in D:
        return True, word
    lower_word = lower_word.strip(".")
    if lower_word in D:
        return True, lower_word
    for t in tags:
        lem_word = lemmatizer(lower_word, pos = t)
        if lem_word != lower_word and lem_word in D:
            return True, lem_word
        cap_word = lem_word.capitalize()
        if cap_word in D:
            return True, cap_word
    des = ["-", "'"]
    for d in des:
        if d in word:
            words = word.split(d)
            words_lemmatized = []
            for w in words:
                c, rw = check_in_dict(w, D, lemmatizer)
                if c:
                    words_lemmatized.append(rw)
                else:
                    return False, word
            return True, words_lemmatized
    return False, word

def normalize_text(t):
    t = re.sub(r"’", " '", t)
    t = re.sub(r"[^a-zA-Z'\-\.]", " ", t)
    t = re.sub(r"--+", " ", t)
    t = re.sub(r"n't\b", " not", t)
    t = re.sub(r"'re\b", " are", t)
    t = re.sub(r"'ve\b", " have", t)
    t = re.sub(r"'ll\b", " will", t)
    t = re.sub(r"'m\b", " am", t)
    t = re.sub(r"'s\b", "", t)
    t = re.sub(r"'", " ", t)
    t = re.sub(r"\s\s+", " ", t).strip()
    return t

def get_words_out_of_dict(text, D, lemmatizer=lemmatizer, min_length=2, tags="nvars"):
    words_out = []
    words_irregular = []
    words_all = normalize_text(text).split()
    for w in list(dict.fromkeys(words_all)):
        isin, word = check_in_dict(w, D, lemmatizer=lemmatizer, tags=tags)
        if not isin and len(word) >= min_length:
            words_out.append(word)
        elif (not is_simple_case_lemmatization(w, word)) and len(word) >= min_length:
            words_irregular.append(word)
    return words_out, words_irregular

def is_simple_case_lemmatization(word, lemma):
    word = word.lower()
    lemma = lemma.lower()
    if word == lemma or word == lemma + "s" or word == lemma + "es":
        return True
    if lemma.endswith("y") and word.endswith("ies"):
        return True
    if word == lemma + "ed":
        return True
    if lemma.endswith("e") and word == lemma + "d":
        return True
    if lemma.endswith("y") and word.endswith("ied"):
        return True
    if lemma and lemma + lemma[-1] + "ed" == word:
        return True
    if word == lemma + "ing":
        return True
    if lemma.endswith("e") and word == lemma[:-1] + "ing":
        return True
    if lemma.endswith("ie") and word == lemma[:-2] + "ying":
        return True
    if lemma and lemma + lemma[-1] + "ing" == word:
        return True
    if word == lemma + "er" or word == lemma + "est":
        return True
    if lemma.endswith("e") and (word == lemma[:-1] + "r" or word == lemma[:-1] + "st"):
        return True
    if lemma.endswith("y") and (word == lemma[:-1] + "ier" or word == lemma[:-1] + "iest"):
        return True
    if lemma and (lemma + lemma[-1] + "er" == word or lemma + lemma[-1] + "est" == word):
        return True
    return False