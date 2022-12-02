from lib import test2
from lib import test1
from log import LOG
from utils.utils import generate_unique_name
from utils.run import run_test

logger = LOG("ci")
logger.configure_log_directory()
tests = list()


for test in [test1, test2, test1, test2, test1, test2]:
    test_name = test.__name__
    if test_name in tests:
        test_name = generate_unique_name(test_name, tests)
    test.__name__ = test_name
    tests.append(test_name)
    run_test(test, test_name, logger)
