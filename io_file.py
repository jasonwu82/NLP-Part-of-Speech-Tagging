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


def write_tagged_file(out_file_name, word_lines, tag_lines):
    with open(out_file_name, 'w') as f:
        for words, tags in zip(word_lines, tag_lines):
            word_tag = ['/'.join(wt) for wt in zip(words, tags)]
            f.write(' '.join(word_tag))
            f.write('\n')


if __name__ == "__main__":
    word_lines = [["I", "believe", 'you']]
    tag_lines = [["NP", "VP", "NP"]]
    write_tagged_file("test.out", word_lines, tag_lines)

