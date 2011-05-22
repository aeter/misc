"""
A prototype of a bloom filter. 
"""
from hashlib import sha224, md5, sha1

LEN = 2000000 #The length of the filter
HASH_FUNCTIONS = [sha224, md5, sha1]

class BloomFilter(object):
    def __init__(self, size, hash_functions):
        self._size = size 
        self._bits = [0 for _ in range(self._size)]
        self._hash_functions = hash_functions

    def __str__(self):
        return ''.join(map(str, self._bits))

    def add(self, elem):
        """
        Adds to the bloom filter. Changes self._bits
        """
        indexes = [self._hash(fn, elem) for fn in self._hash_functions]
        for i in indexes:
            self._bits[i] = 1

    def has(self, elem):
        """
        Checks whether the element is in the filter
        """
        indexes = [self._hash(fn, elem) for fn in self._hash_functions]
        found = all(self._bits[i] for i in indexes)
        return found

    def _hash(self, hash_fn, elem):
        """
        Runs the hash function on the element and finds its index
        in the bits sequence. 
        Returns an int between 0 and self._size.
        """
        return int(hash_fn(elem).hexdigest(), 32) % self._size

def get_words():
    """
    Returns a list of unique words; works on UNIX-like systems.
    """
    with open("/usr/share/dict/words") as f:
        return f.readlines()

if __name__ == '__main__':
    bf = BloomFilter(size=LEN, hash_functions=HASH_FUNCTIONS)
    for word in get_words():
        bf.add(word.strip())
    print bf.has('Kangaroo')
    print bf.has('turtle')
    print bf.has('blast')

