import json

dictionary = {"CC": "coordinating conjunction", "CD": "cardinal digit ",
              "DT": "determiner ", "EX": "existential there (like: “there is” … think of it like “there exists”) ",
              "FW": "foreign word ", "IN": "preposition/subordinating conjunction ",
              "JJ": "adjective – ‘big’ ", "JJR": "adjective, comparative – ‘bigger’ ",
              "JJS":"adjective, superlative – ‘biggest’ ", "MD": "modal – could, will ",
              "NN": "noun, singular ‘- desk’ ", "NNS": "noun plural – ‘desks’ ",
              "NNP": "proper noun, singular – ‘Harrison’ ", "NNPS": "proper noun, plural – ‘Americans’ ",
              "PDT": "predeterminer – ‘all the kids’ ", "POS": "possessive ending parent’s ",
              "PRP":"personal pronoun –  I, he, she ",
              "PRP$": "possessive pronoun – my, his, hers ", "RB": "adverb – very, silently, ",
              "RBR": "adverb, comparative – better ", "RBS": "adverb, superlative – best ",
              "RP": "phrasel verbs – give up ", "TO": "to go ‘to’ the store. ","UH": "interjection – errrrrrrrm ",
              "VB": "verb, base form – take ", "VBD": "verb, past tense – took ",
              "VBG": "verb, gerund/present participle – taking ", "VBN": "verb, past participle – taken ",
              "VBZ": "verb, 3rd person sing. present – takes ", "VBP": "verb, sing. present, non-3d – take ",
              "WDT": "wh-determiner – which ", "WP": "wh-pronoun – who, what ",
              "WP$": "possessive wh-pronoun, eg- whose ", "WRB": "wh-adverb, eg- where, when"}
# converting
full_dict = {}
# define values
key = dictionary.values()
val = dictionary.keys()
# with for create reverse dictionary
for a, b in zip(key, val):
    full_dict.update({a: b})
# write it down
with open("dictionary.json", "w", encoding="utf-8") as file:
    json.dump(full_dict, file, ensure_ascii=False, indent=5)
    print("bitti")

