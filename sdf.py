from nltk.tree import *
import nltk

tree = Tree('S', [('There', 'EX'), ('is', 'VBZ'), ('no', 'DT'), ('signal', 'NN'), ('in', 'IN'), Tree('GPE', [('Colombo', 'NNP')])])

print(tree)

def prep_for_extract(message):  # Prepares the message for information extraction returning an nltk Tree
    sent = message
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)

    tree = nltk.ne_chunk(sent)
    print (type(tree))
    print (tree)
    return tree

new = prep_for_extract("activate data package")

print(new.leaves)