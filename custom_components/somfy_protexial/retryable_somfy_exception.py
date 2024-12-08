from custom_components.somfy_protexial.somfy_exception import SomfyException


class RetryableSomfyException(SomfyException):
    def __init__(self, message=None) -> None:
        self.message = message
        super().__init__(message)
