import numpy as np
from pathlib import Path
# Experiment ideas: 1. Regular 2. Looks at the next n words rather than just the next word 3. Same as 2 but weights words farther less
experiment = 4

class TrumpBot:

    """ Takes in the text file, and cleans it by dealing with punctuation and returns an array of
    all the tokens in the order they are said during the speech.
    """
    def return_token_array(text_file):
            f = open(text_file, 'r')
            bad_set = [" ", "", "\n", "\ufeff\n"]
            tokens = []
            line = f.readline()
            while line:
                tokens.extend(line.replace('...', '.').replace('.', ' . ').replace(',', ' ,').replace(';', ' ; ').replace(':', ' : ').replace('"', ' " ').split(" "))
                line = f.readline()
            f.close()
            tokens = [token for token in tokens if token not in bad_set]
            return tokens

    """ Takes in a list of tokens, and creates a transition matrix out of this
    """
    def make_transition_matrix(tokens):
            ordered_tokens = np.unique(tokens)
            n = len(ordered_tokens)
            mat = np.zeros((n, n))
            for i in range(0, len(tokens) - 1):
                    a, b = np.where(ordered_tokens == tokens[i])[0][0], np.where(ordered_tokens == tokens[i + 1])[0][0]
                    mat[a][b] += 1
            normalize = np.sum(mat, axis=1)
            mat = mat / normalize[:, np.newaxis]
            np.save('ordered_tokens_{}'.format(experiment), ordered_tokens)
            np.save('transition_matrix_{}'.format(experiment), mat)
            return mat, ordered_tokens

    """ Takes in a list of tokens, and creates a transition matrix out of this looking at the next n wrods
    """
    def make_transition_matrix_n(tokens, k):
        ordered_tokens = np.unique(tokens)
        n = len(ordered_tokens)
        mat = np.zeros((n, n))
        for i in range(0, len(tokens) - k):
            for j in range(k):
                a, b = np.where(ordered_tokens == tokens[i])[0][0], np.where(ordered_tokens == tokens[i + j])[0][0]
                if experiment == 2:
                    mat[a][b] += 1
                elif experiment == 3:
                    mat[a][b] += (1/(j + 1))
        normalize = np.sum(mat, axis=1)
        mat = mat / normalize[:, np.newaxis]
        np.save('ordered_tokens_{}'.format(experiment), ordered_tokens)
        np.save('transition_matrix_{}'.format(experiment), mat)
        return mat, ordered_tokens

    """ Generates a random speech given the matrix, ordered_tokens, and number of sentences wanted
    """
    def generate_random(mat, ordered_tokens, num_sentences):
        curr_sentence = 0
        speech_tokens = []
        last_token = np.where(ordered_tokens == '.')[0][0]
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
                if tok not in [',', '.', ';', ':']:
                        speech += ' '
                speech += tok
        speech = speech[1:]
        return speech

    def generate_speech():
        tokens = TrumpBot.return_token_array('speeches.txt')
        if Path('transition_matrix_{}.npy'.format(experiment)).exists() and Path('ordered_tokens_{}.npy'.format(experiment)).exists():
            print('here')
            mat, ordered_tokens = np.load('transition_matrix_{}.npy'.format(experiment)), np.load('ordered_tokens_{}.npy'.format(experiment))
        else:
            if experiment == 1 or experiment == 4:
                mat, ordered_tokens = TrumpBot.make_transition_matrix(tokens)
            elif experiment == 2 or experiment == 3:
                mat, ordered_tokens = TrumpBot.make_transition_matrix_n(tokens, 3)
        speech = TrumpBot.generate_random(mat, ordered_tokens, 250)
        return speech


if __name__ == '__main__':
    print(TrumpBot.generate_speech())
