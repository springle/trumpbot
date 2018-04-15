import numpy as np
from pathlib import Path

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
	ordered_tokens = np.unique(tokens)
	n = len(ordered_tokens)
	mat = np.zeros((n, n))
	for i in range(0, len(tokens) - 1):
		a, b = np.where(ordered_tokens == tokens[i])[0][0], np.where(ordered_tokens == tokens[i + 1])[0][0]
		mat[a][b] += 1
	normalize = np.sum(mat, axis=1)
	mat = mat / normalize[:, np.newaxis]
	np.save('ordered_tokens', ordered_tokens)
	np.save('transition_matrix', mat)
	return mat, ordered_tokens

def generate_random(mat, ordered_tokens, num_sentences):
	curr_sentence = 0
	speech_tokens = []
	last_token = np.where(ordered_tokens == '.')[0][0]
	print("last token: {}".format(last_token))
	while curr_sentence < num_sentences:
		row = mat[last_token]
		indices = np.where(row != 0)[0]
		values = [row[index] for index in indices]
		picked = np.random.choice(indices, p=values)
		last_token = picked
		speech_tokens.append(ordered_tokens[picked])
		if ordered_tokens[picked] == '.':
			curr_sentence += 1
	speech = ''
	for tok in speech_tokens:
		if tok not in [',', '.']:
			speech += ' '
		speech += tok
	speech = speech[1:]

	return speech

if __name__ == '__main__':
	tokens = return_token_array('speeches.txt')
	if Path('transition_matrix.npy').exists() and Path('ordered_tokens.npy').exists():
		mat, ordered_tokens = np.load('transition_matrix.npy'), np.load('ordered_tokens.npy')
	else:
		mat, ordered_tokens = make_transition_matrix(tokens)
	# mat, ordered_tokens = make_transition_matrix(tokens)
	speech = generate_random(mat, ordered_tokens, 5)
	print(speech)



