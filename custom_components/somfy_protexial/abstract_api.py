from abc import ABC, abstractmethod

from .const import Page, Selector


class AbstractApi(ABC):
    pages = None
    selectors = None
    encoding = None

    def get_page(self, page: Page):
        return self.pages[page]

    def get_selector(self, selector: Selector):
        return self.selectors[selector]

    def get_encoding(self):
        return self.encoding

    @abstractmethod
    def get_login_payload(self, username, password, code):
        pass

    @abstractmethod
    def get_reset_session_payload(self):
        pass

    @abstractmethod
    def get_arm_payload(self, zone):
        pass

    @abstractmethod
    def get_disarm_payload(self):
        pass

    @abstractmethod
    def get_turn_light_on_payload(self):
        pass

    @abstractmethod
    def get_turn_light_off_payload(self):
        pass

    @abstractmethod
    def get_open_cover_payload(self):
        pass

    @abstractmethod
    def get_close_cover_payload(self):
        pass

    @abstractmethod
    def get_stop_cover_payload(self):
        pass
