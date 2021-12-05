from tqdm import tqdm

def load_glove_embeddings():
    glove_filepath = '/Users/joeyhou/Developer/develop_resources/glove.6B/glove.6B.300d.txt'
    glove_file = open(glove_filepath, 'r')

    glove_dict = {}
    lines = glove_file.readlines()
    for line in tqdm(lines):
        vec = line.replace('\n', '').split()
        w = vec[0]
        vec = vec[1:]
        vec = [float(i) for i in vec]
        glove_dict[w] = vec

    return glove_dict