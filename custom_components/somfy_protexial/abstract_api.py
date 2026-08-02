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

    def requires_admin(self) -> bool:
        return False

    def is_page_authenticated(self, page) -> bool:
        """
        Check if page needs an authenticated session.
        Supports old Protexial and newer Protexiom variants.
        """

        pages = []

        for name in (
            "STATUS",
            "DEFAULT",
            "LIST_ELEMENTS",
            "LIST_ELEMENTS_ALT",
            "LIST_ELEMENTS_PRINT",
            "LIST_ELEMENTS_NOLANG",
            "LIST_ELEMENTS_ALT_NOLANG",
        ):
            if hasattr(Page, name):
                pages.append(getattr(Page, name))

        return page in pages

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

    @abstractmethod
    def get_reset_battery_err_payload(self):
        pass

    @abstractmethod
    def get_reset_alarm_err_payload(self):
        pass

    @abstractmethod
    def get_reset_link_err_payload(self):
        pass
