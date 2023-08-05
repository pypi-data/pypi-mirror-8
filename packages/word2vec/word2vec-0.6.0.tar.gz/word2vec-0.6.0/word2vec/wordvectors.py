import numpy as np
try:
    from sklearn.externals import joblib
except:
    joblib = None

from word2vec.utils import unitvec


class WordVectors(object):

    def __init__(self, vocab, vectors=None, l2norm=None, save_memory=True):
        """
        Initialize a WordVectors class based on vocabulary and vectors

        This initializer precomputes the l2norm of the vectors

        Parameters
        ----------
        vocab : np.array
            1d array with the vocabulary
        vectors : np.array
            2d array with the vectors calculated by word2vec
        l2norm : np.array
            2d array with the calulated l2norm of the vectors
        save_memory : boolean
            wheter or not save the original vectors in `self.vectors`
        """
        if vectors is None and l2norm is None:
            raise Exception('Need vectors OR l2norm arguments')

        self.vocab = vocab

        if l2norm is None:
            if not save_memory:
                self.vectors = vectors
            self.l2norm = np.vstack(unitvec(vec) for vec in vectors)
        else:
            self.l2norm = l2norm

    def ix(self, word):
        """
        Returns the index on self.vocab and self.l2norm for `word`
        """
        temp = np.where(self.vocab == word)[0]
        if temp.size == 0:
            raise KeyError('Word not in vocabulary')
        else:
            return temp[0]

    def get_vector(self, word):
        """
        Returns the (l2norm) vector for `word` in the vocabulary
        """
        idx = self.ix(word)
        return self.l2norm[idx]

    def __getitem__(self, word):
        return self.get_vector(word)

    def cosine(self, word, n=10):
        """
        Cosine similarity.

        metric = dot(l2norm_of_vectors, l2norm_of_target_vector)
        Uses a precomputed l2norm of the vectors

        Parameters
        ----------
        word : string
        n : int, optional (default 10)
            number of neighbors to return
        """
        metrics = np.dot(self.l2norm, self[word].T)
        best = np.argsort(metrics)[::-1][1:n+1]
        best_metrics = metrics[best]
        return best, best_metrics

    def analogy(self, pos, neg, n=10):
        """
        Analogy similarity.

        Parameters
        ----------
        pos : list
        neg : list

        Returns
        -------
        List of tuples, each tuple is  (word, similarity)


        Example
        -------
            `king - man + woman = queen` will be:
            `pos=['king', 'woman'], neg=['man']`
        """
        words = pos + neg

        pos = [(word, 1.0) for word in pos]
        neg = [(word, -1.0) for word in neg]

        mean = []
        for word, direction in pos + neg:
            mean.append(direction * unitvec(self.get_vector(word)))
        mean = np.array(mean).mean(axis=0)

        metrics = np.dot(self.l2norm, mean)
        best = metrics.argsort()[::-1][:n]
        best_metrics = metrics[best]
        return best, best_metrics

    def generate_response(self, indexes, metrics, n=10, exclude=None):
        if exclude is None:
            exclude = []
        elif isinstance(exclude, basestring):
            exclude = [exclude]
        return [(word, sim) for word, sim in zip(self.vocab[indexes], metrics) if word not in exclude][:n]

    def to_mmap(self, fname):
        if not joblib:
            raise Exception("sklearn needed to save as mmap")

        joblib.dump(self, fname)

    @classmethod
    def from_binary(cls, fname, save_memory=True):
        """
        Create a WordVectors class based on a word2vec binary file

        Parameters
        ----------
        fname : path to file
        save_memory : boolean

        Returns
        -------
        WordVectors class
        """
        with open(fname) as fin:
            header = fin.readline()
            vocab_size, vector_size = map(int, header.split())
            vocab = []

            vectors = np.empty((vocab_size, vector_size), dtype=np.float)
            binary_len = np.dtype(np.float32).itemsize * vector_size
            for line_number in xrange(vocab_size):
                # mixed text and binary: read text first, then binary
                word = ''
                while True:
                    ch = fin.read(1)
                    if ch == ' ':
                        break
                    word += ch
                vocab.append(word)

                vector = np.fromstring(fin.read(binary_len), np.float32)
                vectors[line_number] = vector
                fin.read(1)  # newline
        vocab = np.array(vocab)

        return cls(vocab=vocab, vectors=vectors, save_memory=save_memory)

    @classmethod
    def from_text(cls, fname, save_memory=True):
        """
        Create a WordVectors class based on a word2vec text file

        Parameters
        ----------
        fname : path to file
        save_memory : boolean

        Returns
        -------
        WordVectors class
        """
        with open(fname) as f:
            parts = f.readline().strip().split(' ')
            shape = int(parts[0]), int(parts[1])

        vocab = np.genfromtxt(fname, dtype=object, delimiter=' ', usecols=0, skip_header=1)

        cols = np.arange(1, shape[1] + 1)
        vectors = np.genfromtxt(fname, dtype=float, delimiter=' ', usecols=cols, skip_header=1)

        return cls(vocab=vocab, vectors=vectors, save_memory=save_memory)

    @classmethod
    def from_mmap(cls, fname):
        """
        Create a WordVectors class from a memory map

        Parameters
        ----------
        fname : path to file
        save_memory : boolean

        Returns
        -------
        WordVectors class
        """
        memmaped = joblib.load(fname, mmap_mode='r+')
        return cls(vocab=memmaped.vocab, l2norm=memmaped.l2norm)
