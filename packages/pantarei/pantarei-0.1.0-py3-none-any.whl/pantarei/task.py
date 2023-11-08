from .helpers import actual_kwargs, all_actual_kwargs

class Task:

    def __init__(self, func, cache=None, done=None, clear=None):
        # We assume that done and cache receive only the kwargs of the function
        # If we assume the kwargs are the full signature, then the function is not
        # needed anymore and this simplifies the interface. Check if we may need it.
        self.func = func
        self.cache = cache
        self._done = done
        self._clear = clear
        self.__name__ = func.__name__
        self.artifacts = None
    
    def __call__(self, *args, **kwargs):
        kwargs = actual_kwargs(self.func, *args, **kwargs)
        if self.done(**kwargs):
            return self.cache.read(self.func, **kwargs)
        else:
            results = self.func(**kwargs)
            print('WRITING CACHE', results)
            self.cache.write(results, self.func, **kwargs)

    def fully_qualified_name(self, **kwargs):
        """Unique name of task"""
        from hashlib import md5
        hash_args = md5(str(kwargs).encode()).hexdigest()
        func_name = self.func.__name__
        return f'{func_name}-{hash_args}'

    def name(self):
        """Name of task"""
        return self.__name__
    
    def clear(self, *args, **kwargs):
        all_kwargs = all_actual_kwargs(self.func, *args, **kwargs)        
        # kwargs = actual_kwargs(self.func, *args, **kwargs)
        self.cache.clear(self.func, **kwargs)
        if self._clear is not None:
            self._clear(**all_kwargs)

    def done(self, *args, **kwargs):
        all_kwargs = all_actual_kwargs(self.func, *args, **kwargs)        
        if self._done is None:
            print('TASK IN CACHE', self.cache.found(self.func, **kwargs), kwargs)
            return self.cache.found(self.func, **kwargs)
        else:
            print('DONE?', all_kwargs)
            return self._done(**all_kwargs) and self.cache.found(self.func, **kwargs)

