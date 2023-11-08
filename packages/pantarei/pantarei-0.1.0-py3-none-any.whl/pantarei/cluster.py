from .helpers import serialize_kwargs, rmd, mkdir
import inspect
import subprocess
import dill


class Cluster:

    def __init__(self, host='localhost', scheduler=None, queue='debug', path='data', verbose=True):
        self.host = host
        self.queue = queue
        self.path = path
        self.scheduler = scheduler
        self.verbose = verbose    

    def wait(self, job=None, seconds=5):
        import os, subprocess, time
        while True:
            if job is None:
                must_wait = len(self.queue) > 0
            else:
                must_wait = self.queued(job)
            if must_wait:
                print(f'waiting for {job}')
                time.sleep(seconds)
            else:
                break

    def queue(self):
        return subprocess.check_output('squeue -h', shell=True)
        
    def queued(self, job):
        # if job is not None:
        #     names = ','.join([j.name for j in jobs])
        print(job.name)
        return subprocess.check_output(f'squeue -j {job.name()} -h', shell=True) != 0
        
    def submit(self, job, **kwargs):
        self.wait(job)
        
        if self.scheduler == "slurm":
            command = "sbatch"
            header = ""
            header += "#SBATCH -n {job.name}\n"

        if self.scheduler is None:
            command = 'python -'
            header = ''

        if job.artifacts is None:
            import os
            from hashlib import md5
            hash_args = md5(str(kwargs).encode()).hexdigest()
            dirname = os.path.join(self.path, job.task.__name__, hash_args)
            mkdir(dirname)
            session_pkl = os.path.join(dirname, 'session.pkl')
            # import tempfile
            # dirname = tempfile.mkdtemp(dir='.dill/')
            # session_pkl = os.path.join(dirname, 'session.pkl')
        else:
            dirname = job.artifacts
            mkdir(dirname)
            session_pkl = os.path.join(dirname, 'session.pkl')

        stacks = inspect.stack()
        # for i in range(len(stacks)):
        #     s = stacks[i]
        #     print(i, '*', s.filename)
        #     print(s.code_context)
        #     print(dill.source.getsource(s.frame.f_code))
        s = stacks[-1].frame.f_code
        kwargs = serialize_kwargs(kwargs)
        dill.dump_module(session_pkl, module=inspect.getmodule(s), refimported=True)
        # TODO: process the calling line to get the job object instead of hardcoding
        script = f"""\
#!/usr/bin/env python
{header}
__name__ = '__main__'
import sys
import dill
sys.path.append('.')
dill.load_module('{session_pkl}')
# This calls the function
# results = {job.task.__name__}({kwargs})
results = job.task({kwargs})
"""
        # TODO: we should return the results (pickling it)
        if self.verbose:
            print(script)
        subprocess.run(f"""{command} <<'EOF'
{script}
EOF""", shell=True)

        # TODO: write to cache
        # self.cache.write(results, self.func, **kwargs)

