import pandas as pd
import re


re_split = re.compile(r'(?<!\\)\/')


def parse_line(line):
    tagged_words = line.split()
    res = []
    for w in tagged_words:
        w_split = re_split.split(w)
        if len(w_split) != 2:
            continue
        res.append(w_split)

    return res


def read_tagged_file(file_name):
    with open(file_name, 'r') as f:
        lines = [parse_line(line) for line in f.readlines()]
    return lines

