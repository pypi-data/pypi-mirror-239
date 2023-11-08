import spacy

def split_sentences(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return [sent.text for sent in doc.sents]