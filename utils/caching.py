from flask_caching import Cache

def setup_cache(app):
    cache = Cache(app.server, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache-directory',
        'CACHE_DEFAULT_TIMEOUT': 300
    })
    return cache
