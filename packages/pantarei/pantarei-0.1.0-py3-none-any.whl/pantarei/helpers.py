import inspect

def actual_kwargs(func, *args, **kwargs):
    """Return all the arguments of a function as keyword arguments."""
    import inspect
    signature = inspect.signature(func)
    arg_names = tuple(param.name
                      for param in signature.parameters.values()
                      if param.default is param.empty)
    # TODO: check if we passed a keyword argument we the same value as default
    # Default keyword arguments
    #actual_args = {param.name: param.default
    #               for param in signature.parameters.values()
    #               if param.default is not param.empty}
    actual_args = {}
    actual_args.update({name: arg for name, arg in zip(arg_names, args)})
    actual_args.update(kwargs)
    return actual_args

def all_actual_kwargs(func, *args, **kwargs):
    """Return all the arguments of a function as keyword arguments."""
    import inspect
    signature = inspect.signature(func)
    arg_names = tuple(param.name
                      for param in signature.parameters.values()
                      if param.default is param.empty)
    # TODO: check if we passed a keyword argument we the same value as default
    # Default keyword arguments
    actual_args = {param.name: param.default
                  for param in signature.parameters.values()
                  if param.default is not param.empty}
    # actual_args = {}
    actual_args.update({name: arg for name, arg in zip(arg_names, args)})
    actual_args.update(kwargs)
    return actual_args

def mkdir(dirname):
    """
    Create a directory `dirname` or a list `dirname` of directories,
    silently ignoring existing directories.

    This is just a wrapper to `os.makedirs`. All intermediate
    subdirectories are created as needed.
    """
    import os
    if dirname is None:
        return
    if isinstance(dirname, str):
        dirs = [dirname]
    else:
        dirs = dirname

    for dd in dirs:
        try:
            os.makedirs(dd)
        except OSError:
            pass

def rmd(files):
    """Totally silent wrapper to shutil.rmtree."""
    import shutil
    try:
        shutil.rmtree(files)
    except:
        pass

def serialize_kwargs(kwargs):
    args = []
    for key in kwargs:
        if isinstance(kwargs[key], str):
            args.append(f'{key}="{kwargs[key]}"')
        else:
            args.append(f'{key}={kwargs[key]}')
    return ','.join(args)
