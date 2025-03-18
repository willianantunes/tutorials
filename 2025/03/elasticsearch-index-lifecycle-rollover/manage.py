import logging.config

from index_lifecycle_rollover import settings
from index_lifecycle_rollover.agents import elasticsearch
from index_lifecycle_rollover.support import log_with_correlation_id

if __name__ == "__main__":
    logging.config.dictConfig(settings.LOGGING)
    # Why this try-catch? It works as a global exception handler!
    # Thus, we can guarantee that 100% of the messages are logged as JSON.
    try:
        with log_with_correlation_id():
            elasticsearch.collect_metrics()
    except BaseException:
        logging.exception("Exception has been caught at the global exception handler")
