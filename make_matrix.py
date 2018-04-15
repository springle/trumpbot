import numpy as np

""" Takes in the text file, and cleans it by dealing with punctuation and returns an array of
all the tokens in the order they are said during the speech.
"""
def return_token_array(text_file):
	f = open(text_file, 'r')
	bad_set = [" ", "", "\n", "\ufeff\n"]
	tokens = []
	line = f.readline()
	while line:

		tokens.extend(line.replace('...', '.').replace('.', ' . ').replace(',', ' ,').replace('"', ' " ').split(" "))
		line = f.readline()

	f.close()
	tokens = [token for token in tokens if token not in bad_set]
	return tokens

def make_transition_matrix(tokens):
	tokens = tokens[:20]
	ordered_tokens = np.unique(tokens)
	n = len(ordered_tokens)
	mat = np.zeros((n, n))
	for i in range(0, len(tokens) - 1):
		a, b = np.where(ordered_tokens == tokens[i])[0][0], np.where(ordered_tokens == tokens[i + 1])[0][0]
		mat[a][b] += 1
	normalize = np.sum(mat, axis=1)
	mat = mat / normalize[:, np.newaxis]
	return mat

def generate_random(mat):
	return None

if __name__ == '__main__':
	tokens = return_token_array('speeches.txt')
	make_transition_matrix(tokens)



