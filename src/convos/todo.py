from src.convos.spacy_nlp import nlp
from src.texting import send_message


class ToDo:
    def parse_todo(self, text):
        doc = nlp(text)
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
        print({
            'name': parsed_string,
            'entities': [{
                'text': ent.text,
                'type': ent.label_
            } for ent in doc.ents],
        })

    def complete_task(self):
        send_message('NICE!')