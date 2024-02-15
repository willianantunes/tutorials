import logging.config

from watchdog_k8s import settings
from watchdog_k8s.handler import check_certificates_and_inform_on_slack_if_applicable
from watchdog_k8s.support import log_with_correlation_id


def main():
    logging.config.dictConfig(settings.LOGGING)
    try:
        with log_with_correlation_id():
            check_certificates_and_inform_on_slack_if_applicable(settings.CERTIFICATES_TO_BE_CHECKED.split(","))
    except BaseException as e:
        if not isinstance(e, SystemExit):
            logging.exception("Exception has been caught at the global exception handler")
        raise e


if __name__ == "__main__":
    main()
