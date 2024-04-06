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

API = "api"
COORDINATOR = "coordinator"
DEVICE_INFO = "device_info"


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


class Page(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    PILOTAGE = "pilotage"
    STATUS = "status"
    ERROR = "error"
    ELEMENTS = "elements"
    PRINT = "print"
    VERSION = "version"
    DEFAULT = "default"


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
