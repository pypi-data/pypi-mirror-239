from .helpers import serialize_kwargs, rmd, mkdir
import inspect
import subprocess
import dill

def _auto_detect_scheduler():
    scheduler = 'slurm'
    try:
        subprocess.check_output('squeue', shell=True)
    except subprocess.CalledProcessError:
        scheduler = None
    return scheduler

class Scheduler:

    def __init__(self, host='localhost', queue='debug', path='data', verbose=False):
        self.host = host
        self._queue = queue
        self.path = path
        self.verbose = verbose
        self.command = 'sbatch'

    def wait(self, job_name=None, seconds=5):
        import os, subprocess, time

        while True:
            if job_name is None:
                must_wait = len(self.queue()) > 0
            else:
                must_wait = self.queued(job_name)
            if must_wait:
                if self.verbose:
                    print(f'waiting for {job_name}')
                time.sleep(seconds)
            else:
                break

    def queue(self):
        # print(subprocess.check_output('squeue -h', shell=True))
        output = subprocess.check_output('squeue -h -o %j', shell=True)
        queued_jobs = output.decode().split('\n')[:-1]
        return queued_jobs
        
    def queued(self, job_name):
        import re
        
        # We make sure job_name is a list
        if isinstance(job_name, str):
            job_name = [job_name]

        found = []
        for job in job_name:
            # Check if job_name is fully qualified
            # if re.match('.*-.*', job):
            _found = False
            for queued_job in self.queue():
                # We clear the match afterwards because it cannot be pickled by dill
                match = re.match(job, queued_job)
                if match:
                    _found = True
                    del match
                    break
                del match
            found.append(_found)

        return all(found)
        # return len(subprocess.check_output(f'squeue -n {job_name} -h', shell=True)) > 0
    
    def header(self, job_name):
        header = ""
        header += f"#SBATCH -J {job_name}\n"
        return header
