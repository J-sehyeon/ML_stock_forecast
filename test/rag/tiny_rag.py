import gensim.downloader
from gensim.models import KeyedVectors

import numpy as np
from scipy.spatial.distance import cdist

# downloading encoder
# word_encoder = gensim.downloader.load('glove-twitter-25')
# word_encoder.save("word_encoder.kv")

# load encoder      / 속도가 매우 빨라짐
word_encoder = KeyedVectors.load("test/rag/word_encoder.kv")

# getting the embedding for a word
apple_v = word_encoder['apple']

print(apple_v)

# defining a function for embedding an entire document to a single mean vector
def embed_sequence(sequence):
    vects = word_encoder[sequence.split(' ')]
    return np.mean(vects, axis=0)

seq = embed_sequence('its a sunny day today')
print(seq)

# Calculating distance between two embedding vectors uses manhattan distance
def calc_distance(emb1, emb2):
    return cdist(np.expand_dims(emb1, axis=0), np.expand_dims(emb2, axis=0), metric='cityblock')[0, 0]

print("similar phrases:")
print(calc_distance(
    embed_sequence('sunny day today'),
    embed_sequence('rainy morning presently')
))

print("different phrases:")
print(calc_distance(
    embed_sequence('sunny day today'),
    embed_sequence('perhaps reality is painful')
))

"""Defining documents
for simplicities sake I only included words the embedder knows. You could just
parse out all the words the embedder doesn't know, though. After all, the retreival
is done on a mean of all embeddings, so a missing word or two is of little consequence
"""
documents = {"menu": "ratatouille is a stew thats twelve dollars and fifty cents also gazpacho is a salad "
                    "thats thirteen dollars and ninety eight cents also hummus is a dip thats eight dollars and seventy five cents "
                    "also meat sauce is a pasta dish thats twelve dollars also penne marinera is a pasta dish thats eleven dollars "
                    "also shrimp and linguini is a pasta dish thats fifteen dollars",
             "events": "on thursday we have karaoke and on tuesdays we have trivia",
             "allergins": "the only item on the menu common allergen is hummus which contain pine nuts",
             "info": "the resteraunt was founded by two brothers in two thousand and three"}

# defining a function that retreives the most relevent document
def retreive_relevent(prompt, documents=documents):
    min_dist = 1000000000
    r_docname = ""
    r_doc = ""

    for docname, doc in documents.items():
        dist = calc_distance(
            embed_sequence(prompt),
            embed_sequence(doc)
            )
        
        if dist < min_dist:
            min_dist = dist
            r_docname = docname
            r_doc = doc
    
    return r_docname, r_doc

prompt = "what pasta dishes do you have"
print(f'finding relevent doc for "{prompt}"')
print(retreive_relevent(prompt))
print('----')
prompt = 'what events do you guys do'           # "guys"라는 단어를 위의 파스타 질문에 넣을 경우 잘못된 문서를 출력하는 문제점이 존재한다. 
print(f'finding relevent doc for "{prompt}"')   # 이런 사소한 점들이 이 분야의 현실이다.
print(retreive_relevent(prompt))

# Defining retreival and augmentation 
# creating a function that does retreival and augmentaion, 
# this can be passed straight to the model
def retreive_and_augment(prompt, documents=documents):
    docname, doc = retreive_relevent(prompt, documents)
    return f"Answer the customers prompt based on the following documents:\n==== document: {docname} ====\n{doc}\n====\n\nprompt: {prompt}\nresponse:"

prompt = 'what events do you guys do'
print(f'prompt for "{prompt}":\n')
print(retreive_and_augment(prompt))


# Using RAG with OpenAI's gpt model
from openai import OpenAI
model = OpenAI()
prompts = ['what pasta dishes do you have', 'what events do you guys do', 'oh cool what is karaoke']

for prompt in prompts:
    ra_prompt = retreive_and_augment(prompt)
    response = model.responses.create(
        model='gpt-5-nano',
        input=ra_prompt,
    ).output_text

    print(f'prompt: "{prompt}"')
    print(f'response: {response}')
