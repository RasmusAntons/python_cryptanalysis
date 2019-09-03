# keep a list of the N best things we have seen, discard anything else
class NBest(object):
    def __init__(self, N=1000):
        self.store = []
        self.N = N

    def add(self, item):
        self.store.append(item)
        self.store.sort(reverse=True)
        self.store = self.store[:self.N]

    def __getitem__(self, k):
        return self.store[k]

    def __len__(self):
        return len(self.store)
