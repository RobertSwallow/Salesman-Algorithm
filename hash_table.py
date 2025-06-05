class HashMap:
    def __init__(self, size=40):
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return key % len(self.table)

    def insert(self, key, value):
        bucket = self._hash(key)
        for i, (k, v) in enumerate(self.table[bucket]):
            if k == key:
                self.table[bucket][i] = (key, value)
                return
        self.table[bucket].append((key, value))

    def lookup(self, key):
        bucket = self._hash(key)
        for k, v in self.table[bucket]:
            if k == key:
                return v
        return None

