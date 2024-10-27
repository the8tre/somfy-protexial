from enum import Enum

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import EntityCategory

DOMAIN = "somfy_protexial"

CONF_API_TYPE = "api_type"
CONF_CODE = "code"
CONF_CODES = "codes"
CONF_MODES = "modes"
CONF_ARM_CODE = "arm_code"
CONF_NIGHT_ZONES = "night_zones"
CONF_HOME_ZONES = "home_zones"
CONF_MONITORED_ELEMENTS = "monitored_elements"

API = "api"
COORDINATOR = "coordinator"
DEVICE_INFO = "device_info"

CHALLENGE_REGEX = r"[A-F]{1}[1-5]{1}"


HTTP_TIMEOUT = 10


class SomfyError(str, Enum):
    WRONG_CODE = "(0x0B00)"
    MAX_LOGIN_ATTEMPS = "(0x0904)"
    WRONG_CREDENTIALS = "(0x0812)"
    SESSION_ALREADY_OPEN = "(0x0902)"
    NOT_AUTHORIZED = "(0x0903)"
    UNKNOWN_PARAMETER = "(0x1003)"


class Zone(Enum):
    NONE = 0
    A = 1
    B = 2
    C = 4
    ABC = 7


ALL_ZONES = ["0", "1", "2", "4", "3", "6", "5"]


class ApiType(str, Enum):
    PROTEXIAL = "protexial"
    PROTEXIOM = "protexiom"
    PROTEXIAL_IO = "protexial_io"


class Page(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    PILOTAGE = "pilotage"
    STATUS = "status"
    ERROR = "error"
    ELEMENTS = "elements"
    CHALLENGE_CARD = "challenge_card"
    VERSION = "version"
    DEFAULT = "default"


class Selector(str, Enum):
    CONTENT_TYPE = "content_type"
    LOGIN_CHALLENGE = "login_challenge"
    ERROR_CODE = "error_code"
    FOOTER = "footer"
    CHALLENGE_CARD = "challenge_card"


ELEMENT_TRANSLATIONS = {
    "typetrans": "☎️ Transmetteur téléphonique",
    "typekeyb": "⌨️ Clavier",
    "typesirenint": "🚨 Sirène intérieure",
    "typetecfumee": "💨 Détecteur de fumée",
    "typedm": "🏃 Détecteur de mouvement",
    "typeremotemulti": "Télécommande",
    "typesirenext": "🚨 Sirène extérieure",
    "typedo": "🚪 Détecteur d'ouverture",
    "typedovitre": "🪟 Détecteur d'ouverture vitre",
    "typebadgerfid": "🪪 Badge RFID",
}

ELEMENT_DESCRIPTORS = {
    "typetrans": {"sensors": ["battery"], "name": "Transmetteur téléphonique"},
    "typekeyb": {"sensors": ["battery"], "name": "Clavier"},
    "typesirenint": {"sensors": ["battery"], "name": "Sirène intérieure"},
    "typesirenext": {"sensors": ["battery"], "name": "Sirène extérieure"},
    "typetecfumee": {"sensors": ["battery", "smoke"], "name": "Détecteur de fumée"},
    "typedm": {"sensors": ["battery", "motion"], "name": "Détecteur de mouvement"},
    "typedo": {"sensors": ["battery", "opening"], "name": "Détecteur d'ouverture"},
    "typedovitre": {
        "sensors": ["battery", "window"],
        "name": "Détecteur d'ouverture vitre",
    },
}

ELEMENT_ENTITY = {
    "battery": {
        "type": "battery",
        "data_field": "elt_pile",
        "name": "Batterie",
        "device_class": BinarySensorDeviceClass.BATTERY,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "icon_on": "mdi:battery-alert",
        "icon_off": "mdi:battery",
        "on_if": False,
        "state_on": "Faible",
        "state_off": "ok",
    },
    "smoke": {
        "type": "smoke",
        "data_field": "elt_porte",
        "name": "Fumée",
        "device_class": BinarySensorDeviceClass.SMOKE,
        "icon_on": "mdi:smoke-detector-variant-alert",
        "icon_off": "mdi:smoke-detector-variant",
        "on_if": False,
        "state_on": "Détectée",
        "state_off": "Non détectée",
    },
    "motion": {
        "type": "motion",
        "data_field": "elt_porte",
        "name": "Mouvement",
        "device_class": BinarySensorDeviceClass.MOTION,
        "icon_on": "mdi:motion-sensor",
        "icon_off": "mdi:motion-sensor-off",
        "on_if": False,
        "state_on": "Détectée",
        "state_off": "Non détectée",
    },
    "opening": {
        "type": "opening",
        "data_field": "elt_porte",
        "name": "Ouverture",
        "device_class": BinarySensorDeviceClass.OPENING,
        "icon_on": "mdi:door-open",
        "icon_off": "mdi:door-closed",
        "on_if": False,
        "state_on": "Ouvert",
        "state_off": "Fermé",
    },
    "window": {
        "type": "window",
        "data_field": "elt_porte",
        "name": "Vitre",
        "device_class": BinarySensorDeviceClass.WINDOW,
        "icon_on": "mdi:window-open",
        "icon_off": "mdi:window-closed",
        "on_if": False,
        "state_on": "Ouvert",
        "state_off": "Fermé",
    },
}

BINARY_SENSORS = [
    {
        "id": "battery",
        "name": "Batterie",
        "device_class": BinarySensorDeviceClass.BATTERY,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "icon_on": "mdi:battery-alert",
        "icon_off": "mdi:battery",
        "on_if": "nok",
        "state_on": "Faible",
        "state_off": "ok",
    },
    {
        "id": "alarm",
        "name": "Mouvement détecté",
        "device_class": BinarySensorDeviceClass.MOTION,
        "icon_on": "mdi:motion-sensor",
        "icon_off": "mdi:motion-sensor-off",
        "on_if": "nok",
        "state_on": "Detecté",
        "state_off": "Non détecté",
    },
    {
        "id": "door",
        "name": "Porte ou fenêtre",
        "device_class": BinarySensorDeviceClass.DOOR,
        "icon_on": "mdi:door-open",
        "icon_off": "mdi:door-closed",
        "on_if": "nok",
        "state_on": "Ouvert",
        "state_off": "Fermé",
    },
    {
        "id": "box",
        "name": "Boitier",
        "device_class": BinarySensorDeviceClass.PROBLEM,
        "icon_on": "mdi:alert-circle",
        "icon_off": "mdi:check-circle",
        "on_if": "nok",
        "state_on": "ko",
        "state_off": "ok",
    },
    {
        "id": "radio",
        "name": "Communication radio",
        "device_class": BinarySensorDeviceClass.CONNECTIVITY,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "icon_on": "mdi:access-point",
        "icon_off": "mdi:access-point-off",
        "on_if": "ok",
        "state_on": "ok",
        "state_off": "ko",
    },
    {
        "id": "gsm",
        "name": "Communication gsm",
        "device_class": BinarySensorDeviceClass.CONNECTIVITY,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "icon_on": "mdi:cellphone",
        "icon_off": "mdi:cellphone-off",
        "on_if": "GSM connecté au réseau",
        "state_on": "ok",
        "state_off": "ko",
    },
    {
        "id": "camera",
        "name": "Caméra",
        "device_class": BinarySensorDeviceClass.CONNECTIVITY,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "icon_on": "mdi:webcam",
        "icon_off": "mdi:webcam-off",
        "on_if": "enabled",
        "state_on": "Connectée",
        "state_off": "Non connectée",
    },
]
