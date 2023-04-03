from sdp.fast_db.bloom import BloomFilter


def test_bloom_filter(tmp_path):
    bloom_path = tmp_path / 'bloom.db'
    bloom_filter = BloomFilter(bloom_path, 100, 0.05)
    bloom_filter.add('Bob')
    bloom_filter.add('Alice')

    assert bloom_filter.contains('Bob')
    assert bloom_filter.contains('Alice')
    assert bloom_filter.contains('bob') is False
    assert bloom_filter.contains('alice') is False

    bloom_filter.close()
    bloom_filter = BloomFilter(bloom_path, 100, 0.05)

    assert bloom_filter.contains('Bob')
    assert bloom_filter.contains('Alice')
    assert bloom_filter.contains('bob') is False
    assert bloom_filter.contains('alice') is False

