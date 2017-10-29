import read_file
from grams import WordTagGram
from viterbi_algo import viterbi_algo


def predict_lines(lines, gram):
    return [viterbi_algo(line, gram) for line in lines]


def calc_accuracy(predicted_lines, true_tags_lines):
    correct = 0
    total = 0
    for i in range(len(predicted_lines)):
        correct += sum([1 if predicted_lines[i][j] == true_tags_lines[i][j] else 0 for j in range(len(predicted_lines[i]))])
        total += len(predicted_lines[i])
    return float(correct)/total


data = read_file.read_tagged_file("data/POS.train.large")

gram = WordTagGram()

for i in range(len(data)):
    #print(i)
    #print(data[i])
    gram.add_line(data[i])

gram.calculate_probs()

#viterbi_algo(["Traders", "said", 'the'], gram)
viterbi_algo(["I", "believe", 'you'], gram)

test_lines = read_file.read_tagged_file("data/POS.test")
test_words = [[word for word, tag in line] for line in test_lines]
test_tags = [[tag for word, tag in line] for line in test_lines]
predicted_lines = predict_lines(test_words, gram)
accuracy = calc_accuracy(predicted_lines, test_tags)
print(accuracy)