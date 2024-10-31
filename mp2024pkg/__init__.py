from mp2024pkg.core import show_list
from mp2024pkg.core import show_dict


def __dir__():
    keys = dict.fromkeys((globals().keys()))
    keys.pop("core")
    return list(keys)
