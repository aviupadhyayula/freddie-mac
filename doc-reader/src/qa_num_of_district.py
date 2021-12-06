from transformers import pipeline
question_answering = pipeline("question-answering")


import pickle

# import sys
# sys.path.insert(1, '../src/')

from tree_spider import *
from utils import *

all_answeres = []
for i in (range(100)):
    ts = pickle.load(open('../data/scrapped/pickles_ts/' + str(i) + '.pkl', 'rb'))
    all_leaf_doc = []
    def find_leaf(node):
        if node.is_leaf:
            all_leaf_doc.append({
                'title': node.title,
                'text': node.text_content
            } )
        else:
            for child in node.children:
                find_leaf(child)
    find_leaf(ts.root_node)
    if len(all_leaf_doc) == 0:
        print('no leaf on:', i)
        continue

    context = '\n'.join([doc['text'] for doc in all_leaf_doc])

    question = "How many different zoning districts are there?"

    result = question_answering(question=question, context=context)
    print("Answer:", result['answer'])
    print("Score:", result['score'])
    all_answeres.append(result)