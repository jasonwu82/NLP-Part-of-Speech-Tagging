import pandas as pd


def parse_line(line):
    tagged_words = line.split()
    res = [w.split('/') for w in tagged_words]
    return res


def read_tagged_file(file_name):
    with open(file_name, 'r') as f:
        lines = [parse_line(line) for line in f.readlines()]
    return lines

