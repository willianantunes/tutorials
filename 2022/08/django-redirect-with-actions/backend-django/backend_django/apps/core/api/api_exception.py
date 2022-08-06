from rest_framework.exceptions import APIException


class EmptyBodyException(APIException):
    status_code = 400
    default_detail = "You should send a body with a valid JSON"


class ContractNotRespectedException(APIException):
    status_code = 400
    default_detail = "It seems something is missing to accomplish the task"


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"
