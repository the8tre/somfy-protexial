from custom_components.somfy_protexial.somfy_exception import SomfyError


class RetryableSomfyError(SomfyError):
    def __init__(self, message=None) -> None:
        self.message = message
        super().__init__(message)
