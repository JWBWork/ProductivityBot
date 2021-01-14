import os
from random import choice
from pprint import pprint
from src.paths import SRC_DIR
from collections import defaultdict

scripts_dir = os.path.join(SRC_DIR, 'scripts')
scripts = defaultdict(list)
for file in os.listdir(scripts_dir):
    if '.txt' not in file:
        continue
    script_name = file.split('.')[0]
    with open(os.path.join(scripts_dir, file), 'r') as script_file:
        for line in script_file.readlines():
            line = line.rstrip('\n').replace(r'\n', '\n')
            scripts[script_name].append(line)


def load_line(script_name):
    return choice(scripts[script_name])
