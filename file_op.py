import pickle


def save(thing, filename):
    with open(filename, 'wb') as savef:
        pickle.dump(thing, savef)


def read(filename):
    with open(filename, 'rb') as loadf:
        return pickle.load(loadf)
