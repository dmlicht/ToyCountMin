import zlib
DEFAULT_SIZE = 10000
DEFAULT_K = 2
LARGE_PRIME = 7919

class CountMinSketch(object):
    def __init__(self, k=DEFAULT_K, size=DEFAULT_SIZE):
        """k is the number of hash functions and tables used,
        size is the size of each table"""
        self.k = k
        self.size = size
        self.tables = [[0]*self.size for i in xrange(self.k)]
        self.hash_functions = self._init_hash_functions()

    def _init_hash_functions(self, k, size, large_prime=LARGE_PRIME):
        """create and return array of hash functions, 
        for now we will only use adler32 and crc32
        MUST DOUBLE CHECK: this method of generating hash functions
        is not especially prone to collisions"""
        hash_functions = []
        for i in xrange(1, k+1):
            hash_functions.append(self._create_func(size, i, large_prime))

    def _create_func(self, size, mult, large_prime):
        def inner(val_to_hash):
            return zlib.adler32(val_to_hash)*(large_prime^mult) % size
        return inner

    def update(self, key):
        """Increment counts for hashed position in each table"""
        for i in xrange(self.k):
            table_i_hashed_key = self.hash_functions[i](key)
            self.tables[i][table_i_hashed_key] += 1

    def query(self, key):
        """return minimum count of lookup in each hashed table"""
        counts = []
        for i in xrange(self.k):
            table_i_hashed_key = self.hash_functions[i](key)
            counts.append(self.tables[i][table_i_hashed_key])
        return min(counts)

class TestCountMinSketch:
    def test_default_initialization():
        cms = CountMinSketch()
        assert cms.k == DEFAULT_K
        assert cms.size == DEFAULT_SIZE

    def test_counting():
        cms = CountMinSketch()
        times = 5
        s = "rabble"
        for i in xrange(times):
            cms.update(s)
        assert cms.query(s) == 5
