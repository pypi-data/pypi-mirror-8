from enum import Enum


class RequestType(Enum):
    """ Enumeration of the service available methods. """
    UPDATE = 1
    CHECK_POLICIES = 2
