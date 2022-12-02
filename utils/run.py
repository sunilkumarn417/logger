"""module executes tests."""
from log import LOG


def run_test(mod, name, logger=None):
    if not logger:
        logger = LOG("ci")
    try:
        mod.logger._logger.name = logger.logger_name(name)
        logger.add_file_handler(name)
        mod.run()
        return 0
    except Exception as err:
        logger.error(err)
        return 1
    finally:
        logger.remove_file_handler(name)
