import os
from unittest import TestLoader, TextTestRunner

os.environ['UNIT_TEST'] = 'True'
tests = TestLoader().discover('tests')
result = TextTestRunner(verbosity=2).run(tests)
