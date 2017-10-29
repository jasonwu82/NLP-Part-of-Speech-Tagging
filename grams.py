from collections import Counter, defaultdict


NEW_LINE_TAG = '#'


class GivenCounts(object):
    def __init__(self):
        self.counts = defaultdict(Counter)
        self.probs = {}

    def add_grams(self, grams):
        """
        :param grams: [[word, tag], [word, tag]...] or [[tag_i-1, tag_i], [tag_i-1, tag_i]...]
        :return:
        """

        for key, count_key in grams:
            self.counts[key].update([count_key])

    def calc_probs(self):
        """
        :return: nothing, instead store probability in self.probs
        """
        for key, counter in self.counts.items():
            post_prob = {}
            total_counts = sum(counter.values())
            for post_key, post_count in counter.items():
                post_prob[post_key] = float(post_count)/total_counts
            self.probs[key] = post_prob

    def get_prob(self, post, given):
        return self.probs.get(given, {}).get(post, 0)

    def get_post_probs(self, given):
        """ return {'post': prob', }"""
        return self.probs.get(given, {})


class WordTagGram(object):
    def __init__(self):
        self.tag_gram = GivenCounts()
        # given tag, output word prob
        self.word_tag = GivenCounts()
        self.unique_tags = set()
        # for 1-gram, given word, output tag prob
        self.tag_word = GivenCounts()

    def add_line(self, line):
        """
        :param line: [[word, tag],...]
        :return:
        """
        # for word | tag
        self.word_tag.add_grams([reversed(l) for l in line])
        # for tag | word
        self.tag_word.add_grams(line)

        words, tags = zip(*line)
        # for tag_i | tag_i-1
        tags_prev = list(tags)
        tags_prev.insert(0, NEW_LINE_TAG)
        tags_prev.pop()
        self.tag_gram.add_grams(zip(tags_prev, tags))

        # for tag_counts
        self.unique_tags.update(tags)

    def calculate_probs(self):
        self.tag_gram.calc_probs()
        self.word_tag.calc_probs()
        self.tag_word.calc_probs()

    def prob_word_tag(self, word, tag):
        return self.word_tag.get_prob(word, tag)

    def prob_tag_prevtag(self, tag, given_tag):
        return self.tag_gram.get_prob(tag, given_tag)

    def probs_given_tag(self, given_tag):
        return self.tag_gram.get_post_probs(given_tag)

    def most_prob_tag_given_word(self, word):
        probs = self.tag_word.get_post_probs(word)
        if probs:
            return max(probs, key=lambda x: probs.get(x, 1))
        else:
            return NEW_LINE_TAG


if __name__ == "__main__":
    line = [['Traders', 'NNS'], ['said', 'VBD'], ['the', 'DT'], ['price', 'NN'], ['of', 'IN'], ['cocoa', 'NN'], ['--', ':'], ['mainstay', 'NN'], ['of', 'IN'], ['the', 'DT'], ['economies', 'NNS'], ['of', 'IN']]
    gc = GivenCounts()
    gc.add_grams([reversed(l) for l in line])
    print(gc.counts)
    print('\n')
    wtg = WordTagGram()
    wtg.add_line(line)
    print(wtg.word_tag.counts)
    print(wtg.tag_gram.counts)
    assert(1 == wtg.tag_gram.counts['#']['NNS'])
    assert (2 == wtg.tag_gram.counts['NN']['IN'])

    wtg.calculate_probs()
    assert(0.33 < wtg.prob_word_tag("mainstay", "NN") < 0.34)
    print(wtg.prob_word_tag("mainstay", "NN"))
    assert(wtg.probs_given_tag("NNS")["VBD"] == 0.5)
    print(wtg.probs_given_tag("NNS"))

    print(wtg.unique_tags)

    from viterbi_algo import viterbi_algo
    viterbi_algo(["Traders", "said", 'the'], wtg)
