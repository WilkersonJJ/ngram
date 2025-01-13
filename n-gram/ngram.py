import re
import nltk
import random
#nltk.download('punkt')
START = "[START]"
END = "[END]"

def read_file():
    with open("sample.txt", "r", encoding='utf-8') as f:
        rawtext = f.read()
    f.close()
    return rawtext

def clean_and_split_text(text):
    text = re.sub('[?!—.":;,()”“-]+', '', text)
    text = text.lower()
    text = text.split()
    return text

def get_unique_words(text):
    word_list = []
    word_list.append(START)
    word_list.append(END)
    for word in text:
        if word not in word_list:
            word_list.append(word)
    return word_list

def create_dict(words):
    word_dict = {}
    i = 0
    for word in words:
        word_dict[word] = i
        i += 1
    return word_dict

def prepare_sentences(paragraph):
    sentences = nltk.sent_tokenize(paragraph)
    new_sentences = []
    for sent in sentences:
        sent = clean_and_split_text(sent)
        sent.insert(0, START)
        sent.append(END)
        new_sentences.append(sent)
    return new_sentences

def get_word_index(word, dictionary):
    return dictionary[word]

def get_word_from_index(index, dictionary):
    for word, i in dictionary.items():
        if i == index:
            return word

def calculate_coccurence(sentences, matrix, dictionary):
    for sent in sentences:
        for i in range(len(sent) - 1):
            first_word = sent[i]
            second_word = sent[i+1]
            first_i = get_word_index(first_word, dictionary)
            second_i = get_word_index(second_word, dictionary)
            matrix[first_i][second_i] += 1

def choose_word(prev_word, matrix, word_dict):
    index = get_word_index(prev_word, word_dict)
    possible_words = []
    for i in range(len(matrix[index])):
        value = matrix[index][i]
        if value > 0:
            for j in range(value):
                possible_words.append(get_word_from_index(i, word_dict))
    return random.choice(possible_words)
        

unique_words = get_unique_words(clean_and_split_text(read_file()))
word_dict = create_dict(unique_words)
length = len(unique_words)
matrix = [[0 for _ in range(length)] for _ in range(length)]
sentences = prepare_sentences(read_file())
calculate_coccurence(sentences, matrix, word_dict)

word = START
sentence = ""
for i in range(100):
    word = choose_word(word, matrix, word_dict)
    if word == END:
        sentence += ". "
        word = choose_word(START, matrix, word_dict)
    else:
        sentence += " "
    sentence += word

print(sentence)






