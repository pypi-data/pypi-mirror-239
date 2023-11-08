import unittest
from pantarei import *

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_task_cache(self):
        import time
        def f(x):
            time.sleep(1)
            return x
        cache = Cache('/tmp/data')
        task = Task(f, cache=cache)
        task(x=1)
        self.assertTrue(task.done(x=1))
        ti = time.time()
        task(x=1)
        tf = time.time()
        self.assertLess(tf-ti, 0.9)
        task.clear(x=1)
        self.assertFalse(task.done(x=1))
        ti = time.time()
        task(x=1)
        tf = time.time()
        self.assertGreater(tf-ti, 0.9)

    @unittest.skip('not working')
    def test_job(self):
        def f(x):
            import time
            time.sleep(5)
            return x
        task = Task(f, cache=Cache('/tmp/data'))
        job = Job(task)
        job(x=1)
        
    def test_task_artifact(self):
        import os
        def f(x, y, path='/tmp/data_y{y}.txt'):
            with open(path.format(**locals()), 'w') as fh:
                fh.write(f'x={x}')
            return x
        def done(**kwargs):
            # This will work as long as there is a path argument
            path = kwargs['path'].format(**kwargs)
            return os.path.exists(path)
        def clear(**kwargs):
            from pantarei.helpers import rmd
            path = kwargs['path'].format(**kwargs)
            rmd(path)

        cache = Cache('/tmp/data')
        task = Task(f, cache=cache, done=done, clear=clear)
        task(x=1, y=0)
        self.assertTrue(task.done(x=1, y=0))
        task.clear(x=1, y=0)
        self.assertFalse(task.done(x=1, y=0))

    def tearDown(self):
        from pantarei.helpers import rmd
        rmd('/tmp/data')

if __name__ == '__main__':
    unittest.main()
    
