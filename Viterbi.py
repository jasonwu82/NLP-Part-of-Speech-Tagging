import io_file
from grams import WordTagGram
from viterbi_algo import viterbi_algo
import argparse
import time


def predict_lines_viterbi(lines, gram):
    #viterbi_algo(["East", "German", "emigres", "in", "Budapest", "said", "East"], gram)
    return [viterbi_algo(line, gram) for line in lines]


def predict_with_most_freq(lines, gram):
    return [[gram.most_prob_tag_given_word(w) for w in line] for line in lines]


def calc_accuracy(predicted_lines, true_tags_lines):
    correct = 0
    total = 0
    for i in range(len(predicted_lines)):
        correct += sum([1 if predicted_lines[i][j] == true_tags_lines[i][j] else 0 for j in range(len(predicted_lines[i]))])
        total += len(predicted_lines[i])
    return float(correct)/total


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("train")
    parser.add_argument("test")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    start_time = time.time()
    args = parse_args()
    data = io_file.read_tagged_file(args.train)

    gram = WordTagGram()

    for i in range(len(data)):
        gram.add_line(data[i])

    # calculate probability with added data using counting
    gram.calculate_probs()

    test_lines = io_file.read_tagged_file(args.test)
    test_words = [[word for word, tag in line] for line in test_lines]
    test_tags = [[tag for word, tag in line] for line in test_lines]
    predicted_tags = predict_lines_viterbi(test_words, gram)
    accuracy = calc_accuracy(predicted_tags, test_tags)
    print("viterbi accuracy: {0:.2f}".format(accuracy*100))

    io_file.write_tagged_file(args.test + ".out", test_words, predicted_tags)

    predicted_tags_naive = predict_with_most_freq(test_words, gram)
    accuracy = calc_accuracy(predicted_tags_naive, test_tags)
    print("naive using most frequent accuracy: {0:.2f}".format(accuracy*100))

    print("program last {0:.2f} seconds".format(time.time() - start_time))
