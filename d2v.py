import sys
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from readDocument import getText


def cosine_similarity(A, B):
    return np.dot(A, B)/(np.linalg.norm(A)*np.linalg.norm(B))


filenames = sys.argv[1:]
documents = list(map(getText, filenames))
train_text = [TaggedDocument(words=word_tokenize(
    doc), tags=[str(i)]) for i, doc in enumerate(documents)]


model = Doc2Vec(vector_size=500, window=2, epochs=20, min_count=1)
model.build_vocab(train_text)
model.train(train_text, total_examples=model.corpus_count, epochs=50)

test_text = list(map(word_tokenize, documents))

vecs = list(map(model.infer_vector, test_text))

total_files = len(filenames)
similarity_matrix = np.zeros((total_files, total_files))

for i in range(total_files):
    for j in range(total_files):
        similarity_matrix[i, j] = cosine_similarity(vecs[i], vecs[j])

print(f"\nSimilarity = \n{similarity_matrix}")
