import read_file
from grams import WordTagGram
from viterbi_algo import viterbi_algo


data = read_file.read_tagged_file("data/POS.train")

gram = WordTagGram()

for i in range(len(data)):
    #print(i)
    #print(data[i])
    gram.add_line(data[i])

gram.calculate_probs()

#viterbi_algo(["Traders", "said", 'the'], gram)
viterbi_algo(["I", "believe", 'you'], gram)

#test_data = read_file.read_tagged_file("data/POS.test")