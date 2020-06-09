import nltk


def traverse(t):  # Not important for now
    try:
        t.label()
    except AttributeError:
        print(t, end=' ')
    else:
        # Now we know that t.node is defined
        print('(', t.label(), end=' ')
        for child in t:
            traverse(child)
        print(')', end=' ')


def ne_name(t):  # Get the name of the user from the message
    for child in t:
        if isinstance(child, nltk.tree.Tree):
            return " ".join([val[0] for val in child])


def ne_package(t):  # Get the package name from the message
    try:
        for child in t:
            if child[1] == "NNP":
                return child[0]
    except:
        for child in t:
            if isinstance(child, nltk.tree.Tree):
                return child[0][0]


def ne_data_package(t):  # Get the data package name from the message
    try:
        for child in t:
            if child[1] == "NNP":
                return child[0]
    except:
        for child in t:
            if isinstance(child, nltk.tree.Tree):
                return child[0][0]
    

def ne_voice_package(t):  # Get the voice package name from the message
    try:
        for child in t:
            if child[1] == "NNP":
                return child[0]
    except:
        for child in t:
            if isinstance(child, nltk.tree.Tree):
                return child[0][0]


def ne_low_signal_location(t):  # Get the location from the message
    for child in t:
        if isinstance(child, nltk.tree.Tree):
            return child[0][0]


def ne_change_package(t):  # Get the two package names from the message (This prints both)
    try:
        for child in t:
            if child[1] == "NNP":
                return child[0]
    except:
        for child in t:
            if isinstance(child, nltk.tree.Tree):
                return (child[0][0])


if __name__=="__main__":
    # Example sentences for testing
    sent1 = "My name is Minul Lamahewage"
    sent2 = "I want to activate D99 package"
    sent3 = "What can you tell me about the V199 package"
    sent4 = "I want to deactivate the V99 package"
    sent5 = "I had low signal in Jaffna"
    sent6 = "I want to change my package to D99"

    # Change the sentence here
    sent = "I want to activate D99 data package"
    # sent = sent2

    sent = nltk.word_tokenize(sent)  # Splits the sentence by word
    sent = nltk.pos_tag(sent)  # Tags each word by the part-of-speech

    tree = nltk.ne_chunk(sent, binary=True)  # Chunks them by "Named Entities" and makes a tree

    print(tree)  # Prints the entire tree, for reference

    # Here, run the required function on the tree
    # Ex: To get the name from "sent1", set "sent=sent1" and run "name(tree)" here
    print(ne_data_package(tree))

