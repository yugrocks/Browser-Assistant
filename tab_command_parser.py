import nltk
from nltk import pos_tag, word_tokenize


#verbs that are to be pos tagged as VB always in a command
#to correct the error by nltk in pos tagging

all_time_verbs = {'type':'', 'enter':"", 'input':"", 'start':"", 'write':"",
                  'fill':"",'change':"", 'switch':"", 'turn':"",
                  'click':"", 'press':"", 'follow':""
                  , 'go':"", 'open':"", 'search':"", 'look':"","put":""}

grammar = r"""
NP: {<DT|JJ|NN.*>+}
CLAUSE: {<NP><VP>}
CMD: {<VB|VBP.*><IN>?<TO>?}
OBJ: {<NP|CLAUSE|NN>}
OBJ: {<OBJ>*<IN><OBJ>*}
"""
command_string = []
object_string = []
next = ['next', 'later', 'adjacent', 'succeeding', 'adjoining', 'following', 'subsequent']  # some synonyms of next
previous = ['previous', 'earlier', 'past', 'preceding', 'ex']  # some synonyms of previous
miscellaneous = {'first':0, 'second':1, 'third':2, 'fourth':3, 'fifth':4, 'sixth':5, 'seventh':6, 'eighth':7, 'ninth':8, 'tenth':9} #some tab numbers. may be useful


def pos_tag_sent(sentence):
    tokens = word_tokenize(sentence)
    pos_tags = pos_tag(tokens)
    pos_tags = [[word, tag] for (word, tag) in pos_tags]
    if pos_tags[0][0] in all_time_verbs:
        pos_tags[0][1] = 'VB'
    pos_tags = [(word, tag) for [word, tag] in pos_tags]
    return pos_tags


def retrieve_object_from_parsed_sentence(tree, container, first_command_taken = False):
    global command_string, object_string
    #here we consider that phraze as an object which is not a command phraze
    for subtree in tree: #children
        if type(subtree) is nltk.tree.Tree :
            if subtree.label() == "CMD" and not first_command_taken:
                retrieve_object_from_parsed_sentence(subtree, command_string,  first_command_taken =  first_command_taken)
                first_command_taken = True
            else:
                retrieve_object_from_parsed_sentence(subtree, object_string, first_command_taken)
        elif type(subtree) is tuple:
            container.append(subtree[0])

def get_the_objective(sentence):
    global command_string, object_string
    command_string = []
    object_string = []
    original_sent = sentence[0:len(sentence)]
    sentence = pos_tag_sent(sentence)
    cp = nltk.RegexpParser(grammar)
    parsed = cp.parse(sentence)
    retrieve_object_from_parsed_sentence(parsed, object_string)
    command = " ".join(command_string)
    print("command: "," ".join(command_string))
    object1 = " ".join(object_string)
    #now trim the object string to ignore words before the command string
    idx_cmd = original_sent.find(command)
    object1 = original_sent[idx_cmd+len(command):len(original_sent)]
    print("object: ",object1)
    return object1.strip()



def process_objective(objective):
    objective = objective.split()
    for token in objective:
        if token in next:
            return "+1"
        elif token in previous:
            return "-1"
        elif token in miscellaneous:
            return miscellaneous[token]
        print(token)
    return "+1"