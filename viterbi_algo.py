from grams import NEW_LINE_TAG


def viterbi_algo(words, word_tag_gram):
    unique_tags = list(word_tag_gram.unique_tags)
    print(unique_tags)

    score = [{} for i in range(len(words))]
    back_path = [{} for i in range(len(words))]
    for tag in unique_tags:
        score[0][tag] = word_tag_gram.prob_word_tag(words[0], tag) * word_tag_gram.prob_tag_prevtag(tag, NEW_LINE_TAG)
    print(score)

    for i in range(1, len(words)):
        for tag in unique_tags:
            # argmax
            highest_prev_tag = None
            highest_score = 0
            for prev_tag in unique_tags:
                tmp_score = score[i-1][prev_tag] * word_tag_gram.prob_tag_prevtag(tag, prev_tag)
                if tmp_score >= highest_score:
                    highest_prev_tag = prev_tag
                    highest_score = tmp_score
            score[i][tag] = word_tag_gram.prob_word_tag(words[i], tag) * highest_score
            back_path[i][tag] = highest_prev_tag

    highest_tag = None
    highest_score = 0
    for tag in unique_tags:
        if score[-1][tag] >= highest_score:
            highest_tag = tag
            highest_score = score[-1][tag]

    print(score)
    print(back_path)
    path = [highest_tag]
    for i in range(len(back_path)-1, 0, -1):
        path.append(back_path[i][highest_tag])
        highest_tag = path[-1]
    path.reverse()
    print(path)
