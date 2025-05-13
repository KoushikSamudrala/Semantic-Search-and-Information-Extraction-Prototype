import spacy

# Load transformer-based spaCy model
nlp = spacy.load("en_core_web_trf")

def extract_entities_and_relations(text: str):
    """
    Extract named entities and simple subject-predicate-object relations.
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    relations = []
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ('relcl', 'prep'):
                subj = [w for w in token.head.lefts if w.dep_ in ('nsubj','nsubjpass')]
                obj = [w for w in token.rights if w.dep_ in ('dobj','pobj')]
                if subj and obj:
                    relations.append((subj[0].text, token.head.lemma_, obj[0].text))
    return entities, relations