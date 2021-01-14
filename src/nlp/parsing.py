from itertools import chain
from tabulate import tabulate
import spacy
from pprint import pprint
from itertools import chain
import json
import os

# nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('en_core_web_md')
# nlp = spacy.load('en_core_web_sm')

CONVERSATIONS = []
for file_names in os.listdir('./convos'):
    if '.json' in file_names:
        with open(f'./convos/{file_names}') as convo_file:
            CONVERSATIONS.append(json.load(convo_file))
# CONVO_STATES = list(chain(*[c["states"] for c in CONVERSATIONS]))
# pprint(CONVO_STATES)



def analyze(text):
    doc = nlp(text)
    token_dependencies = (
        (token.text, token.dep_, token.head.text, token.pos_)
        for token in doc
    )
    print('\n'+tabulate(
        token_dependencies,
        headers=[
            'Token',
            'Dependency Relation',
            'Parent Token',
            'POS'
        ]
    ))


def match_state(user_input):
    print(f"\nmatching {user_input}")
    doc_input = nlp(user_input)
    cleaned = " ".join([
        t.text if t.dep_ != "ROOT" else t.pos_ for t in doc_input
    ])
    doc_input = nlp(cleaned)
    print(doc_input.text)
    scores = dict()
    # states = [c for c in CONVERSATIONS]
    for convo in CONVERSATIONS:
        state_scores = dict()
        for state in convo.get('states'):
            sim_sum = 0
            applied_samples = 0
            for sample in state.get("samples"):
                doc_sample = nlp(sample)
                similarity = doc_input.similarity(doc_sample)
                if similarity > 0.4 and similarity != 1:
                    print(f"similarity: {sample} {similarity}")
                    sim_sum += similarity
                    applied_samples += 1
            if applied_samples:
                state_scores[state['name']] = sim_sum/applied_samples
        scores[convo["name"]] = state_scores
    print(f"\navg_similarity:")
    pprint(scores)


def parse_input_todo(text):
    doc = nlp(text)
    # parsing name of task
    parsed = [
        token for i, token in enumerate(doc)
        if token.pos_ != 'PRON'
        and token.ent_type_ == ''
        and "'" not in token.text
    ]

    # removes excess/'acting' verb idk
    verbs = [token for token in doc if token.pos_ == 'VERB']
    if len(verbs) > 1 and verbs[0] in parsed:
        parsed.remove(verbs[0])

    # remove words like 'to' from beginning and end
    if parsed[0].pos_ in ['PART', 'ADP']:
        parsed.remove(parsed[0])
    if parsed[-1].pos_ in ['PART', 'ADP']:
        parsed.remove(parsed[-1])

    # lemmatize and join parsed tokens
    parsed_string = " ".join(
        token.lemma_ if token.pos_ != 'DET'
        else token.text
        for token in parsed
    )
    return {
        'name': parsed_string,
        'entities': [{
            'text': ent.text,
            'type': ent.label_
        } for ent in doc.ents],
    }


def main():
    examples = [
        "I need to go shopping at 9am tomorrow",
        "next week I'm going to the doctor",
        "remind me to work on my project tomorrow",
        "I need to do laundry tomorrow"
    ]
    for example in examples:
        pprint(parse_input_todo(example))


if __name__ == '__main__':
    pass
    # main()

    # data = [
    #     "I need to go shopping at 9am tomorrow",
    #     "next week I'm going to the doctor",
    #     "remind me to work on my project tomorrow",
    #     "I need to do laundry tomorrow"
    # ]
    # for d in data:
    #     for i in data:
    #         print(f'{d[0:5]} {i[0:5]}: \n\t{match_state(d, i)}')

    # t = [
    #     "I'm working on the art site",
    #     "watching youtube",
    #     "nothing",
    #     "drawing"
    # ]
    # for s in t:
    #     analyze(s)

    match_state('working on freelancing')
