from log import LOG

logger = LOG(__name__)


def print_msg(msg=None):
    logger.info(msg)

def generate_unique_name(testname, test_list):
    """
    Generate unique log file name
    """
    if testname not in test_list:
        return testname

    testname = testname.split("-", 1)[0]
    test_count = len([testname for _test in test_list
                      if _test.startswith(testname)]) + 1
    return "{}-{}".format(testname, test_count)


