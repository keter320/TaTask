from kivy.utils import get_color_from_hex


def hex_color(value: str):
    return get_color_from_hex(value)


BACKGROUND = hex_color("#2B2D3A")
SURFACE = hex_color("#363848")
ELEVATED_SURFACE = hex_color("#3F4159")
PRIMARY_PURPLE = hex_color("#9B6DFF")
SECONDARY_GREEN = hex_color("#4ECBA1")
SECONDARY_VIOLET = hex_color("#C084FC")
PRIORITY_HIGH = hex_color("#FF6B6B")
PRIORITY_MEDIUM = hex_color("#FFB347")
PRIORITY_LOW = hex_color("#4ECBA1")
TEXT_PRIMARY = hex_color("#F0EEFF")
TEXT_SECONDARY = hex_color("#9B99B5")
DIVIDER = hex_color("#454760")


PRIORITY_COLOR_MAP = {
    1: PRIORITY_HIGH,
    2: PRIORITY_MEDIUM,
    3: PRIORITY_LOW,
}
