import inspect
import dill
import subprocess

from .scheduler import Scheduler, _auto_detect_scheduler
from .helpers import mkdir, serialize_kwargs

class Job:

    def __init__(self, task, scheduler=None, cores=1, wall_time=None,
                 **kwargs):
        self.task = task
        self.scheduler = scheduler
        self.cores = cores
        self.wall_time = wall_time
        # Arguments for task (as keyword arguments only)
        if kwargs is None:
            self.kwargs = {}
        
        # This will autodetect a scheduler on localhost
        if self.scheduler is None:
            if _auto_detect_scheduler() is not None:
                self.scheduler = Scheduler()
    
    def name(self):
        """General name of job (independent of arguments)"""
        return self.task.name(**self.kwargs)

    def fully_qualified_name(self):
        """Unique name of job"""
        return self.task.fully_qualified_name(**self.kwargs)
    
    def clear(self, **kwargs):
        if hasattr(self.task, 'clear'):
            self.task.clear(self.task, **kwargs)
        # TODO: job should clear its own artifacts

    def done(self, **kwargs):
        # TODO: add condition on job execution
        if hasattr(self.task, 'done'):
            print('JOB DONE', self.task.done(**kwargs))
            return self.task.done(**kwargs)
        print('JOB DONE++ False')
        return False
    
    def __call__(self, **kwargs):
        # If no arguments are passed than we assume they were passed
        # to the constructor
        if len(kwargs) > 0:
            self.kwargs = kwargs
            
        if self.done(**self.kwargs):
            return self.task(**kwargs)
        else:
            self._submit()
            
        # We reset the arguments if they were passed to __call__
        if len(kwargs) > 0:
            self.kwargs = {}

    def _submit(self):

        if self.scheduler is None:
            command = 'python -'
            header = ''
        else:
            # self.scheduler.wait(self.fully_qualified_name())
            if self.scheduler.queued(self.fully_qualified_name()):
                print('JOB IS IN QUEUE', self.fully_qualified_name())
                return
            command = self.scheduler.command
            header = self.scheduler.header(job_name=self.fully_qualified_name())

        dirname = self.task.artifacts
        if dirname is None:
            import os
            dirname = os.path.join('.dill', self.fully_qualified_name())
        mkdir(dirname)
        session_pkl = os.path.join(dirname, 'session.pkl')

        stacks = inspect.stack()
        s = stacks[-1]
        kwargs = serialize_kwargs(self.kwargs)
        code = f"dill.load_module('{session_pkl}')"
        # print('DUMP stack', inspect.getmodule(s.frame.f_code), s)
        # dill.dump_module(session_pkl, module=inspect.getmodule(s.frame.f_code), refimported=True)
        var = s.frame.f_locals
        if '__pyfile' in var:            
            s = stacks[-2]
            garbage = var.pop('__pyfile')
            del garbage
        # print(s.frame.f_locals)
        # print('DUMP stack', inspect.getmodule(s.frame.f_code), s)
        dill.dump_module(session_pkl, module=inspect.getmodule(s.frame.f_code), refimported=True)
        # TODO: process the calling line to get the job object instead of hardcoding job
        script = f"""\
#!/usr/bin/env python
{header}
__name__ = '__main__'
import sys
import dill
sys.path.append('.')
{code}
job.task({kwargs})
"""
        # print(script)
        # print('---->ABOUT TO RUN!')
        subprocess.run(f"""{command} <<'EOF'
{script}
EOF""", shell=True)
        # print('----+DONE')
        
