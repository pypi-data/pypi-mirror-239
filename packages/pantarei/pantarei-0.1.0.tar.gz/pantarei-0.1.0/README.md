# Pantarei

[![license](https://img.shields.io/pypi/l/atooms.svg)](https://en.wikipedia.org/wiki/GNU_General_Public_License)
[![pipeline status](https://framagit.org/coslo/pantarei/badges/main/pipeline.svg)](https://framagit.org/coslo/pantarei/-/commits/main)
[![coverage report](https://framagit.org/coslo/pantarei/badges/main/coverage.svg)](https://framagit.org/coslo/pantarei/-/commits/main)

A minimal and flexible workflow manager

## Features

- [X] submit jobs on local slurm scheduler
- [ ] handle task dependencies
- [ ] submit on remote cluster

## Quick start

Pantarei builds on three different execution units:
- **functions** are stateless, Python callables
- **tasks** are wrapped functions for shared-memory environments (single node)
- **jobs** are wrapped tasks for distributed-memory environments (HPC clusters)

To see it in action, say you have a Python function
```python
def f(x):
    import time
    time.sleep(2)
    return x
```

Wrap the function with a Task and call it with a range of arguments
```python
from pantarei import *

task = Task(f)
for x in [1, 2]:
    task(x=x)
```

The task's results are cached: a successive execution will just the results
```python
results = task(x=1)
```

We wrap the task with a Job and submit jobs to a local scheduler (like SLURM)
```python
job = Job(task)
for x in [3, 4]:
    job(x=x)
```

Once the jobs are done, we can get the results (which are cached too)
```python
job.scheduler.wait()
results = job(x=3)
```

## Documentation

Check out the [tutorial]() for more examples and the [public API]() for full details.

## Installation

From pypi
```
pip install pantarei
```

## Contributing

Contributions to the project are welcome. If you wish to contribute, check out [these guidelines]().

## Authors

- Daniele Coslovich

