import pickle

def savepickle(obj, path):
    with open(path, 'wb') as fp:
        pickle.dump(obj, fp)

def loadpickle(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)