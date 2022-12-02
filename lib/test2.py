from time import sleep
from utils.utils import print_msg
from log import LOG

logger = LOG(__name__)


def run(count=10):
    logger.info(f"Running {__name__} for {count}")
    for i in range(count):
        print_msg(f"Running {__name__}.run for {i}")
        sleep(1)


if __name__ == "__main__":
    run()
