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
    def login(self, username, password, code):
        pass

    @abstractmethod
    def reset_session(self):
        pass

    @abstractmethod
    def arm(self, zone):
        pass

    @abstractmethod
    def disarm(self):
        pass

    @abstractmethod
    def turn_light_on(self):
        pass

    @abstractmethod
    def turn_light_off(self):
        pass

    @abstractmethod
    def open_cover(self):
        pass

    @abstractmethod
    def close_cover(self):
        pass

    @abstractmethod
    def stop_cover(self):
        pass

    @abstractmethod
    def reset_battery_status(self):
        pass

    @abstractmethod
    def reset_link_status(self):
        pass

    @abstractmethod
    def reset_alarm_status(self):
        pass
