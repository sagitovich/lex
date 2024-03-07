import pymorphy2
from analysis.dict import context_dicts


morph = pymorphy2.MorphAnalyzer()


def check_words_in_dict(input_list_, dictionary_):
    for line in input_list_[2:len(input_list_):5]:
        words = line.split()
        for word in words:
            p = morph.parse(word)[0]
            for key in dictionary_:
                if any(p.normal_form == morph.parse(dict_word)[0].normal_form for dict_word in dictionary_[key]):
                    print(line)
                    break


# Пример использования:
dictionary = context_dicts

input_list = [...]

check_words_in_dict(input_list, dictionary)
