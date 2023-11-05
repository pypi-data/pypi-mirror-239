from dotenv import load_dotenv
from pykuda.classes.service_type import ServiceType

load_dotenv()


class PyKuda(ServiceType):
    """
    PyKuda Class.
    """

    def __init__(self):
        response = self.check_envs_are_set()

        # If all credentials were properly set, response will
        # be a bool(True), else will be a string
        if not isinstance(response, bool):
            raise ValueError(response)
