from lib import test2
from lib import test1
from log import LOG

import pdb
pdb.set_trace()

logger = LOG("main")
logger.configure_log_directory()

for test in [test1, test2]:
    logger.add_file_handler(test.__name__)
    test.run()





