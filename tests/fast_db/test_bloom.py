from sdp.fast_db.bloom import BloomFilter


def test_add_item():
    bloom_filter = BloomFilter(3, 10)

    bloom_filter.add_item('Henri')
    bloom_filter.add_item('François')
    bloom_filter.add_item('Jordi')
    bloom_filter.add_item('Florentin')

    assert bloom_filter.exists('Henri')
    assert bloom_filter.exists('François')
    assert bloom_filter.exists('Jordi')
    assert bloom_filter.exists('Florentin')
    assert bloom_filter.exists('Pierre') is False


