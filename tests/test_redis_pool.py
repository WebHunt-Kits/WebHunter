from api.common.redis_pool import _process_redis_url


def test_process_redis_url():
    results = _process_redis_url('redis://:passwd1q23@192.168.124.26:6379/3')
    assert results == (True, {"passwd": "passwd1q23",
                              "host": "192.168.124.26", "port": 6379, "db": 3})
    
    results = _process_redis_url('redis://:@192.168.124.26:6379/0')
    assert results == (True, {"passwd": "",
                              "host": "192.168.124.26", "port": 6379, "db": 0})
    
    results = _process_redis_url('redis://123123123:@192.168.124.26:6379/')
    assert results == (False, None)
