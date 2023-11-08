import gzip
import pickle

def compress_and_save(obj, filename):
    with gzip.open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_and_decompress(filename):
    with gzip.open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj

