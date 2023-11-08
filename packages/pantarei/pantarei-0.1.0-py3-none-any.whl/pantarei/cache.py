import os
import pickle
from .helpers import actual_kwargs, mkdir, rmd

class Cache:

    def __init__(self, path):
        self.path = path

    def _storage_path(self, func_name, kwargs):
        import os
        from hashlib import md5
        hash_args = md5(str(kwargs).encode()).hexdigest()
        # print('CACHE HASH', hash_args, kwargs)
        path = os.path.join(self.path, func_name, hash_args)
        mkdir(path)
        return path
    
    def write(self, results, func, **kwargs):
        """Return the function cache results"""
        path = self._storage_path(func.__name__, kwargs)        
        with open(os.path.join(path, 'results.pkl'), 'wb') as fh:
            pickle.dump(results, fh)
        # print('WWW', os.path.join(path, 'results.pkl'))
        
    def read(self, func, **kwargs):
        """Return the function cache results"""
        path = self._storage_path(func.__name__, kwargs)
        with open(os.path.join(path, 'results.pkl'), 'rb') as fh:
            results = pickle.load(fh)
        return results

    def found(self, func, **kwargs):
        """Found in cache"""
        path = self._storage_path(func.__name__, kwargs)
        return os.path.exists(os.path.join(path, 'results.pkl'))
    
    def clear(self, func, **kwargs):
        """Clear cache for func call"""
        path = self._storage_path(func.__name__, kwargs)
        rmd(path)
        
