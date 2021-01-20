import re
from src.texting import send_message
from src.convos import CONVERSATIONS, load_convos
from src.scripts import load_line
from src.convos import bot_classes
from src.subBots.spacy_nlp import nlp
from collections import defaultdict


class Bot(*bot_classes):
    def __init__(self):
        self.CONVERSATIONS = CONVERSATIONS
        self.expected_state = None
        self.force_state = None
        self.temp = defaultdict(lambda: None)
        print(f"bot initialized with {len(self.CONVERSATIONS)} conversations")

    def reload_convos(self):
        print('reloading conversations')
        self.CONVERSATIONS = load_convos()

        print(f'{len(self.CONVERSATIONS)} convos loaded')

    def parse(self, user_input):
        functions = {
            "reload": "reload_convos",
        }
        if user_input[0] == ':':
            return getattr(self, functions[user_input[1:]])()

        user_input = re.sub(r"[^\w\s]+", '', user_input).lower()

        if self.force_state:
            _, exp_s = self._load_convo_path(self.force_state)
            self._chat_function(exp_s, user_input)
            return

        doc_input = nlp(user_input)
        # scores = dict()
        scores = []

        if len(user_input.split(" ")) > 3:
            cleaned = " ".join([
                t.text if t.dep_ != "ROOT" else t.pos_ for t in doc_input
            ])
            doc_input = nlp(cleaned)
        print(f"parsing '{doc_input}'")

        if self.expected_state:
            if isinstance(self.expected_state, str):
                self.expected_state = [self.expected_state, ]
            for state in self.expected_state:
                exp_c, exp_s = self._load_convo_path(state)
                sample_score, _ = self._compare_samples(doc_input, exp_s)
                if sample_score:
                    if sample_score >= 0.70:
                        self._chat_function(exp_s, user_input)
                        return
                    else:
                        scores.append({
                            'convo': exp_c['name'],
                            'state': exp_s,
                            'score': sample_score
                        })
            self.expected_state = None

        for convo in self.CONVERSATIONS:
            if not convo['entry']:
                continue
            for state in convo.get('states'):
                sample_score, _ = self._compare_samples(doc_input, state)
                if state.get('entry'):
                    scores.append({
                        'convo': convo['name'],
                        'state': state,
                        'score': sample_score
                    })

        if scores:
            convo_n, state = next(
                (d['convo'], d['state']) for d in scores
                if d['score'] == max((m['score'] for m in scores))
            )
            # _, state = self._load_convo_path(f"{convo_n}/{state_n}")
            print(f'executing func name: {state["function"]}')
            if state:
                self._chat_function(state, user_input)
        return scores

    @staticmethod
    def _compare_samples(doc_input, state):
        sim_sum = 0
        applied_samples = 0
        for sample in state.get("samples"):
            doc_sample = nlp(sample)
            similarity = doc_input.similarity(doc_sample)
            if 0.3 < similarity:
                sim_sum += similarity
                applied_samples += 1
        if applied_samples:
            score = sim_sum / applied_samples
            return score, state

    def _load_convo_path(self, path):
        print(f"loading path: {path}")
        convo_n, state_n = path.split('/')
        convo = next(
            c for c in self.CONVERSATIONS if c['name'] == convo_n
        )
        state = next(
            s for s in convo['states'] if s['name'] == state_n
        )
        return convo, state

    def _chat_function(self, state, user_input):
        kwargs = state.get('kwargs', dict())
        try:
            getattr(self, state['function'])(user_input, **kwargs)
        except TypeError as e:
            getattr(self, state['function'])(**kwargs)

    def greeting(self):
        send_message(load_line('greetings'))


def test_bot():
    def main():
        while True:
            user_input = input('?: ')
            if user_input != 'exit':
                my_bot.parse(user_input)
            else:
                break

    from threading import Thread

    t = Thread(target=main)
    t.start()


my_bot = Bot()

if __name__ == '__main__':
    pass
