import os
import re
import sys

import nltk
from nltk.corpus import stopwords
from PyDictionary import PyDictionary


def open_all_files(root_dir):
    files_text = []
    for dir in os.listdir(root_dir):
        tmp_file = open(root_dir + dir)
        tmp_txt = tmp_file.readlines()
        files_text += tmp_txt
        print(dir)
    return files_text


def filter_texts(files):
    texts = []
    for line in files:
        if re.match("<font.*>.*", line) or re.match(".*</font.*>", line):
            # print("######################")
            x = re.sub("(<font.*>)(.*)(</font.*>)", r"\2", line)
            x = re.sub("(<font.*>)(.*)", r"\2", x)
            x = re.sub("(.*)(</font.*>)", r"\1", x)
            texts.append(x)
            # print(x)
            # print(line)
            # print("######################")

    return texts


def tokenize_it(filtered_texts):
    words = []
    for i in filtered_texts:
        words += nltk.tokenize.word_tokenize(i)
    return words


def extract_features(filtered_texts):
    dic = {}
    for sentence in filtered_texts:
        for word in nltk.tokenize.word_tokenize(sentence):
            lower = word.lower()
            dic[lower] = dic.get(lower, 0) + 1

    return dic


def extract_useful(features):
    stop_words = set(stopwords.words('english'))
    filtered_features = list(features.keys())
    filtered_features2 = [i for i in filtered_features if i.isalpha() and not (i in stop_words)]
    return filtered_features2


def extract_useful_stem(filtered_features2, features):
    new_dic = {}
    porter = nltk.wordnet.WordNetLemmatizer()
    for word in filtered_features2:
        new_dic[porter.lemmatize(word)] = new_dic.get(porter.lemmatize(word), 0) + features[word]
    return new_dic


def read_dic(dic_dir):
    lines = open(dic_dir).readlines()
    words = [i.split()[0] for i in lines]
    words_counts = {i.split()[0]: int(i.split()[1]) for i in lines}
    return words, words_counts


def extract_difficulty(sorted_features, dic):
    dic_list = [i[0] for i in dic]
    word_index = []
    for word, count in sorted_features:
        try:
            index = dic_list.index(word)
            word_index.append((word, index))
        except ValueError:
            continue
    return word_index


def filter_difficults(word_difficulty, dic_size, hardship):
    steps = dic_size / 10
    result = [(i[0], int(i[1] / steps) + 1) for i in word_difficulty if i[1] / steps >= (hardship - 1)]
    return result


def write_dif(output, output_dir):
    pydic = PyDictionary()
    t = open(output_dir, "w")
    for (word, hardship) in output:
        t.write(word + "\t" + str(hardship) + "\n")
        t.write("Meaning: https://dictionary.cambridge.org/dictionary/english/" + word + "\n ")
        pydic_res = pydic.meaning(word)
        if pydic_res:
            for pos in pydic_res.keys():
                t.write("\t" + pos + "\n")
                for meaning in pydic_res[pos]:
                    t.write("\t\t" + meaning + "\n")
        t.write("#######################\n")
    t.close()


if __name__ == "__main__":
    root_dir = "dataset/"
    dic_dir = "en_50k_2.txt"
    output_dir = "output.txt"
    hardship = 1
    try:
        root_dir = sys.argv[1]
        dic_dir = sys.argv[2]
        output_dir = sys.argv[3]
        hardship = int(sys.argv[4])
    except:
        pass

    files = open_all_files(root_dir)
    filtered_texts = filter_texts(files)
    features = extract_features(filtered_texts)
    useful_features = extract_useful(features)
    useful_features = extract_useful_stem(useful_features, features)
    sorted_features = sorted(useful_features.items(), key=lambda x: -1 * x[1])
    dic, dic_count = read_dic(dic_dir)
    useful_dic = extract_useful_stem(dic, dic_count)
    sorted_dic = sorted(useful_dic.items(), key=lambda x: -1 * x[1])
    word_difficulty = extract_difficulty(sorted_features, sorted_dic)
    filtered_words = filter_difficults(word_difficulty, len(sorted_dic), hardship)
    write_dif(sorted(filtered_words, key=lambda x: -1 * x[1]), output_dir)
    print("done")
