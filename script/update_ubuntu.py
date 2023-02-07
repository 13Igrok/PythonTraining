import apt

cache = apt.Cache()
cache.update()
cache.open(None)
cache.upgrade()